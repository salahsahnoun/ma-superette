from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.conf import settings
from panier.cart import Panier
from produits.models import Produit
from .models import Commande, LigneCommande
from .forms import CommandeForm
from .notifications import notifier_nouvelle_commande

FRAIS_LIVRAISON = Decimal(getattr(settings, 'FRAIS_LIVRAISON', '3.00'))


class StockInsuffisant(Exception):
    def __init__(self, nom, stock):
        self.nom = nom
        self.stock = stock


def checkout(request):
    panier = Panier(request)
    if len(panier) == 0:
        messages.warning(request, 'Votre panier est vide.')
        return redirect('produits:liste')

    if request.method == 'POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            mode = form.cleaned_data['mode_livraison']
            frais = FRAIS_LIVRAISON if mode == 'livraison' else Decimal('0')
            sous_total = panier.total()

            try:
                with transaction.atomic():
                    commande = form.save(commit=False)
                    commande.sous_total = sous_total
                    commande.frais_livraison = frais
                    commande.total = sous_total + frais
                    if request.user.is_authenticated:
                        commande.user = request.user
                    commande.save()

                    for item in panier:
                        # Verrouillage pour éviter les conflits de stock
                        produit = Produit.objects.select_for_update().get(pk=item['produit'].pk)
                        if produit.stock < item['quantite']:
                            raise StockInsuffisant(produit.nom, produit.stock)

                        LigneCommande.objects.create(
                            commande=commande,
                            produit=produit,
                            nom_produit=produit.nom,
                            quantite=item['quantite'],
                            prix_unitaire=item['prix'],
                        )
                        produit.stock -= item['quantite']
                        produit.save(update_fields=['stock'])

            except StockInsuffisant as e:
                msg = f'Stock insuffisant pour "{e.nom}"'
                if e.stock > 0:
                    msg += f' (il reste {e.stock} en stock)'
                else:
                    msg += ' (rupture de stock)'
                msg += '. Veuillez ajuster votre panier.'
                messages.error(request, msg)
                return redirect('panier:detail')

            panier.vider()
            notifier_nouvelle_commande(commande)
            return redirect('commandes:confirmation', pk=commande.pk)
    else:
        form = CommandeForm()

    return render(request, 'commandes/checkout.html', {
        'form': form,
        'panier': panier,
        'frais_livraison': FRAIS_LIVRAISON,
    })


def confirmation(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    return render(request, 'commandes/confirmation.html', {'commande': commande})


STEPS = [
    ('en_attente', 'En attente',        'hourglass-split'),
    ('en_cours',   'En cours',          'gear'),
    ('prete',      'Prête',             'check-circle'),
    ('livree',     'Livrée',            'bag-check'),
]
STEP_INDEX = {'en_attente': 1, 'en_cours': 2, 'prete': 3, 'livree': 4, 'annulee': 0}


def suivi(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    return render(request, 'commandes/suivi.html', {
        'commande':   commande,
        'steps':      STEPS,
        'step_index': STEP_INDEX.get(commande.statut, 0),
    })
