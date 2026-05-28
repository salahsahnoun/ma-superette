from django.conf import settings
from .cart import Panier


def panier_context(request):
    from produits.models import Categorie
    return {
        'panier':     Panier(request),
        'categories': Categorie.objects.all(),
        'currency':   getattr(settings, 'CURRENCY_SYMBOL', 'DA'),
    }
