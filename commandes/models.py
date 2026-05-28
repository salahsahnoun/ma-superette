from django.conf import settings
from django.db import models, transaction


class Commande(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours de traitement'),
        ('prete', 'Prête / En livraison'),
        ('livree', 'Livrée / Récupérée'),
        ('annulee', 'Annulée'),
    ]

    MODE_CHOICES = [
        ('livraison', 'Livraison à domicile'),
        ('retrait', 'Retrait en magasin'),
    ]

    # Compte client (optionnel — les commandes invité ont user=None)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='commandes',
        verbose_name="Compte client",
    )

    # Infos client
    nom = models.CharField(max_length=100, verbose_name="Nom complet")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    adresse = models.TextField(verbose_name="Adresse", blank=True)
    note = models.TextField(blank=True, verbose_name="Note")

    # Mode de récupération
    mode_livraison = models.CharField(
        max_length=20, choices=MODE_CHOICES, default='livraison',
        verbose_name="Mode de récupération"
    )
    heure_retrait = models.TimeField(
        null=True, blank=True,
        verbose_name="Heure de passage prévue"
    )

    # Tarif
    sous_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    frais_livraison = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-created']

    def __str__(self):
        return f"Commande #{self.pk} — {self.nom}"

    def save(self, *args, **kwargs):
        action_stock = None   # 'restaurer' | 'decrementer' | None
        if self.pk:
            try:
                ancien = Commande.objects.get(pk=self.pk)
                if ancien.statut != 'annulee' and self.statut == 'annulee':
                    action_stock = 'restaurer'     # commande annulée → stock libéré
                elif ancien.statut == 'annulee' and self.statut != 'annulee':
                    action_stock = 'decrementer'   # annulation levée → stock réservé
            except Commande.DoesNotExist:
                pass

        with transaction.atomic():
            super().save(*args, **kwargs)
            if action_stock == 'restaurer':
                self._ajuster_stock(+1)
            elif action_stock == 'decrementer':
                self._ajuster_stock(-1)

    def _ajuster_stock(self, signe):
        """signe = +1 pour restituer, -1 pour déduire."""
        from produits.models import Produit
        for ligne in self.lignes.all():
            if ligne.produit_id:
                Produit.objects.filter(pk=ligne.produit_id).update(
                    stock=models.F('stock') + signe * ligne.quantite
                )

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('commandes:suivi', args=[self.pk])

    def get_mode_display_icon(self):
        return '🚚' if self.mode_livraison == 'livraison' else '🏪'


class ConfigNotification(models.Model):
    """Singleton — paramètres de la notification WhatsApp admin."""
    whatsapp_phone  = models.CharField(
        max_length=30, blank=True,
        verbose_name="Numéro WhatsApp",
        help_text="Format international, ex : +213 6XX XXX XXX",
    )
    whatsapp_apikey = models.CharField(
        max_length=50, blank=True,
        verbose_name="Clé API CallMeBot",
        help_text="Obtenez-la sur callmebot.com",
    )
    actif = models.BooleanField(
        default=True,
        verbose_name="Notifications actives",
    )

    class Meta:
        verbose_name = "Configuration WhatsApp"
        verbose_name_plural = "Configuration WhatsApp"

    def __str__(self):
        return "Configuration WhatsApp"

    def save(self, *args, **kwargs):
        self.pk = 1          # singleton : toujours l'enregistrement #1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass                  # interdit la suppression

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, related_name='lignes', on_delete=models.CASCADE)
    produit = models.ForeignKey(
        'produits.Produit', on_delete=models.SET_NULL, null=True, blank=True
    )
    nom_produit = models.CharField(max_length=200)
    quantite = models.PositiveIntegerField()
    prix_unitaire = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = "Ligne de commande"
        verbose_name_plural = "Lignes de commande"

    def __str__(self):
        return f"{self.quantite}x {self.nom_produit}"

    def total_ligne(self):
        return self.prix_unitaire * self.quantite
