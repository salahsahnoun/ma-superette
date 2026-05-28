from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Produit, Categorie, Slide

PER_PAGE = 12


def _paginate(qs, request):
    paginator = Paginator(qs, PER_PAGE)
    return paginator.get_page(request.GET.get('page', 1))


def liste(request):
    q = request.GET.get('q', '').strip()
    qs = Produit.objects.filter(disponible=True).select_related('categorie')
    if q:
        qs = qs.filter(Q(nom__icontains=q) | Q(description__icontains=q))
    return render(request, 'produits/liste.html', {
        'produits':         _paginate(qs, request),
        'categorie_active': None,
        'q':                q,
        'slides':           Slide.objects.filter(actif=True),
    })


def par_categorie(request, slug):
    categorie = get_object_or_404(Categorie, slug=slug)
    q = request.GET.get('q', '').strip()
    qs = Produit.objects.filter(categorie=categorie, disponible=True).select_related('categorie')
    if q:
        qs = qs.filter(Q(nom__icontains=q) | Q(description__icontains=q))
    return render(request, 'produits/liste.html', {
        'produits':         _paginate(qs, request),
        'categorie_active': categorie,
        'q':                q,
    })


def detail(request, pk, slug):
    produit = get_object_or_404(Produit, pk=pk, slug=slug, disponible=True)
    return render(request, 'produits/detail.html', {'produit': produit})
