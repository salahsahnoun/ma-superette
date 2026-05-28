from django.contrib import admin
from django.utils.html import format_html
from .models import Categorie, Produit, Slide


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['icone', 'nom', 'slug', 'nb_produits']
    prepopulated_fields = {'slug': ('nom',)}

    def nb_produits(self, obj):
        return obj.produits.count()
    nb_produits.short_description = 'Produits'


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ['apercu_image', 'nom', 'categorie', 'prix', 'stock', 'disponible', 'updated']
    list_editable = ['prix', 'stock', 'disponible']
    list_filter = ['categorie', 'disponible']
    search_fields = ['nom', 'description']
    prepopulated_fields = {'slug': ('nom',)}
    readonly_fields = ['created', 'updated', 'apercu_image_detail']
    fieldsets = (
        ('Informations', {
            'fields': ('nom', 'slug', 'categorie', 'description')
        }),
        ('Prix & Stock', {
            'fields': ('prix', 'stock', 'disponible')
        }),
        ('Photo', {
            'fields': ('image', 'apercu_image_detail')
        }),
        ('Dates', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',)
        }),
    )

    def apercu_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="48" height="48" style="object-fit:cover;border-radius:6px;" />',
                obj.image.url
            )
        return format_html('<span style="color:#aaa;">—</span>')
    apercu_image.short_description = 'Photo'

    def apercu_image_detail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:200px;border-radius:8px;margin-top:8px;" />',
                obj.image.url
            )
        return '—'
    apercu_image_detail.short_description = 'Aperçu'


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display  = ['apercu', 'titre', 'badge', 'ordre', 'actif']
    list_editable = ['ordre', 'actif']
    readonly_fields = ['apercu_detail']
    fieldsets = (
        ('Contenu', {
            'fields': ('titre', 'sous_titre', 'badge')
        }),
        ('Visuel', {
            'fields': ('image', 'apercu_detail')
        }),
        ('Action', {
            'fields': ('lien', 'lien_texte')
        }),
        ('Affichage', {
            'fields': ('ordre', 'actif')
        }),
    )

    def apercu(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="40" style="object-fit:cover;border-radius:4px;">',
                obj.image.url
            )
        return '—'
    apercu.short_description = 'Aperçu'

    def apercu_detail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:400px;border-radius:8px;margin-top:8px;">',
                obj.image.url
            )
        return '—'
    apercu_detail.short_description = 'Prévisualisation'
