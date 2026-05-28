from django.db import models
from django.urls import reverse


class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icone = models.CharField(max_length=10, blank=True, default='📦')

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['nom']

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('produits:par_categorie', args=[self.slug])


class Slide(models.Model):
    titre      = models.CharField(max_length=120, verbose_name="Titre")
    sous_titre = models.CharField(max_length=250, blank=True, verbose_name="Sous-titre")
    badge      = models.CharField(max_length=50,  blank=True, verbose_name="Badge (ex : Nouveau, Promo)")
    image      = models.ImageField(upload_to='slides/', verbose_name="Image (1400×600 recommandé)")
    lien       = models.CharField(max_length=200, blank=True, verbose_name="Lien (URL ou chemin)")
    lien_texte = models.CharField(max_length=60,  blank=True, default="Découvrir", verbose_name="Texte du bouton")
    ordre      = models.PositiveSmallIntegerField(default=0, verbose_name="Ordre d'affichage")
    actif      = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        ordering = ['ordre', 'pk']
        verbose_name = "Slide carousel"
        verbose_name_plural = "Slides carousel"

    def __str__(self):
        return self.titre


class Produit(models.Model):
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='produits')
    nom = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='produits/', blank=True, null=True)
    disponible = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['nom']

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('produits:detail', args=[self.pk, self.slug])

    @property
    def en_stock(self):
        return self.stock > 0
