from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from produits.models import Produit
from .cart import Panier


@require_POST
def ajouter(request, produit_id):
    panier = Panier(request)
    produit = get_object_or_404(Produit, id=produit_id, disponible=True)
    quantite = int(request.POST.get('quantite', 1))
    panier.ajouter(produit, quantite)
    messages.success(request, f'"{produit.nom}" a été ajouté au panier.')
    next_url = request.POST.get('next', '')
    if next_url and next_url.startswith('/'):
        return redirect(next_url)
    return redirect('panier:detail')


def detail(request):
    panier = Panier(request)
    return render(request, 'panier/panier.html', {'panier': panier})


@require_POST
def modifier(request, produit_id):
    panier = Panier(request)
    produit = get_object_or_404(Produit, id=produit_id)
    quantite = int(request.POST.get('quantite', 1))
    if quantite > 0:
        panier.modifier(produit, quantite)
    else:
        panier.supprimer(produit)
        messages.info(request, f'"{produit.nom}" a été retiré du panier.')
    return redirect('panier:detail')


@require_POST
def supprimer(request, produit_id):
    panier = Panier(request)
    produit = get_object_or_404(Produit, id=produit_id)
    panier.supprimer(produit)
    messages.info(request, f'"{produit.nom}" a été retiré du panier.')
    return redirect('panier:detail')
