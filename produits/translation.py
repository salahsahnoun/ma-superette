from modeltranslation.translator import register, TranslationOptions
from .models import Categorie, Produit, Slide


@register(Categorie)
class CategorieTranslation(TranslationOptions):
    fields = ('nom',)


@register(Produit)
class ProduitTranslation(TranslationOptions):
    fields = ('nom', 'description')


@register(Slide)
class SlideTranslation(TranslationOptions):
    fields = ('titre', 'sous_titre', 'badge', 'lien_texte')
