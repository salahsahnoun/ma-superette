from django.contrib import admin, messages
from django.urls import path, reverse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.html import format_html
from .models import Commande, LigneCommande, ConfigNotification

STATUT_CONFIG = [
    ('',           'Toutes',              '#6c757d', '📋'),
    ('en_attente', 'En attente',          '#856404', '⏳'),
    ('en_cours',   'En cours',            '#0c5460', '⚙️'),
    ('prete',      'Prête / En livraison','#155724', '✅'),
    ('livree',     'Livrée / Récupérée',  '#1b5e20', '🎉'),
    ('annulee',    'Annulée',             '#721c24', '❌'),
]


class LigneCommandeInline(admin.TabularInline):
    model = LigneCommande
    extra = 0
    readonly_fields = ['produit', 'nom_produit', 'quantite', 'prix_unitaire', 'total_ligne_affiche']
    can_delete = False

    def total_ligne_affiche(self, obj):
        return f"{obj.total_ligne():.2f} €"
    total_ligne_affiche.short_description = 'Total'


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'nom', 'telephone', 'mode_badge',
        'heure_retrait', 'sous_total_affiche', 'frais_affiche',
        'total_affiche', 'statut', 'created', 'btn_detail'
    ]
    list_filter = ['created']          # statut géré par les onglets
    list_editable = ['statut']         # Changement rapide en liste
    search_fields = ['nom', 'telephone', 'adresse']
    readonly_fields = ['sous_total', 'frais_livraison', 'total', 'created']
    view_on_site = True   # bouton "Voir sur le site" dans le détail admin
    inlines = [LigneCommandeInline]
    fieldsets = (
        ('Client', {
            'fields': ('nom', 'telephone', 'adresse', 'note')
        }),
        ('Mode de récupération', {
            'fields': ('mode_livraison', 'heure_retrait')
        }),
        ('Tarif', {
            'fields': ('sous_total', 'frais_livraison', 'total')
        }),
        ('Statut', {
            'fields': ('statut', 'created')
        }),
    )

    # ── URL personnalisée ─────────────────────────────────────────────────

    def get_urls(self):
        urls = super().get_urls()
        extra = [
            path(
                '<int:pk>/detail/',
                self.admin_site.admin_view(self.detail_view),
                name='commandes_commande_detail',
            ),
        ]
        return extra + urls

    def detail_view(self, request, pk):
        commande = get_object_or_404(Commande, pk=pk)
        context = {
            **self.admin_site.each_context(request),
            'commande': commande,
            'title': f'Commande #{commande.pk} — {commande.nom}',
            'opts': self.model._meta,
        }
        return TemplateResponse(request, 'admin/commandes/commande/detail.html', context)

    # ── Colonnes personnalisées ───────────────────────────────────────────

    def mode_badge(self, obj):
        if obj.mode_livraison == 'livraison':
            return format_html(
                '<span style="background:#e3f2fd;color:#1565c0;padding:3px 10px;border-radius:12px;font-size:0.8rem;">🚚 Livraison</span>'
            )
        return format_html(
            '<span style="background:#f3e5f5;color:#6a1b9a;padding:3px 10px;border-radius:12px;font-size:0.8rem;">🏪 Retrait</span>'
        )
    mode_badge.short_description = 'Mode'

    def statut_badge(self, obj):
        colors = {
            'en_attente': ('#fff3cd', '#856404'),
            'en_cours':   ('#d1ecf1', '#0c5460'),
            'prete':      ('#d4edda', '#155724'),
            'livree':     ('#c3e6cb', '#1b5e20'),
            'annulee':    ('#f8d7da', '#721c24'),
        }
        bg, fg = colors.get(obj.statut, ('#eee', '#333'))
        return format_html(
            '<span style="background:{};color:{};padding:3px 10px;border-radius:12px;font-size:0.8rem;">{}</span>',
            bg, fg, obj.get_statut_display()
        )
    statut_badge.short_description = 'Statut'

    def sous_total_affiche(self, obj):
        return f"{obj.sous_total:.2f} €"
    sous_total_affiche.short_description = 'Sous-total'

    def frais_affiche(self, obj):
        if obj.frais_livraison:
            return format_html('<span style="color:#1565c0;">+{} €</span>', f"{obj.frais_livraison:.2f}")
        return '—'
    frais_affiche.short_description = 'Frais livr.'

    def total_affiche(self, obj):
        return format_html('<strong>{} €</strong>', f"{obj.total:.2f}")
    total_affiche.short_description = 'Total'
    total_affiche.admin_order_field = 'total'

    def btn_detail(self, obj):
        url = reverse('admin:commandes_commande_detail', args=[obj.pk])
        return format_html(
            '<a href="{}" style="'
            'background:#1B3829;color:#fff;padding:4px 12px;'
            'border-radius:6px;font-size:.78rem;font-weight:600;white-space:nowrap;">'
            '🔍 Détails</a>',
            url,
        )
    btn_detail.short_description = ''

    # ── Onglets de statut ─────────────────────────────────────────────────

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        statut_actif = request.GET.get('statut__exact', '')
        tabs = []
        for statut, label, color, icone in STATUT_CONFIG:
            if statut == '':
                count = Commande.objects.count()
                url = '?'
            else:
                count = Commande.objects.filter(statut=statut).count()
                url = f'?statut__exact={statut}'
            tabs.append({
                'statut': statut,
                'label': label,
                'color': color,
                'icone': icone,
                'count': count,
                'actif': statut_actif == statut,
                'url': url,
            })

        extra_context['tabs_statut'] = tabs
        return super().changelist_view(request, extra_context=extra_context)


# ── Configuration WhatsApp (singleton) ───────────────────────────────────────

@admin.register(ConfigNotification)
class ConfigNotificationAdmin(admin.ModelAdmin):
    fieldsets = (
        ('📱 Numéro destinataire', {
            'fields': ('whatsapp_phone',),
            'description': (
                'Le numéro WhatsApp qui recevra les alertes de nouvelles commandes. '
                'Format international : +213 6XX XXX XXX'
            ),
        }),
        ('🔑 Clé API CallMeBot', {
            'fields': ('whatsapp_apikey',),
            'description': (
                'Clé obtenue en envoyant "I allow callmebot.com to send me messages" '
                'au +34 644 63 99 00 sur WhatsApp.'
            ),
        }),
        ('⚙️ Options', {
            'fields': ('actif',),
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        extra = [
            path(
                'tester/',
                self.admin_site.admin_view(self.tester_view),
                name='commandes_confignotification_tester',
            ),
        ]
        return extra + urls

    def tester_view(self, request):
        """Envoie un message WhatsApp de test."""
        from .notifications import _envoyer_whatsapp_test
        cfg = ConfigNotification.get()
        if not cfg.whatsapp_phone or not cfg.whatsapp_apikey:
            messages.error(request, "Numéro ou clé API manquant — configurez-les d'abord.")
        elif not cfg.actif:
            messages.warning(request, "Les notifications sont désactivées.")
        else:
            ok = _envoyer_whatsapp_test(cfg)
            if ok:
                messages.success(request, f"✅ Message de test envoyé à {cfg.whatsapp_phone} !")
            else:
                messages.error(request, "❌ Échec de l'envoi. Vérifiez le numéro et la clé API.")
        return redirect('admin:commandes_confignotification_change', 1)

    def has_add_permission(self, request):
        return not ConfigNotification.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # Redirige directement vers le formulaire d'édition (singleton)
        return redirect(
            reverse('admin:commandes_confignotification_change', args=[1])
            if ConfigNotification.objects.exists()
            else reverse('admin:commandes_confignotification_add')
        )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['test_url'] = reverse('admin:commandes_confignotification_tester')
        extra_context['show_save_and_continue'] = False
        extra_context['show_save_and_add_another'] = False
        return super().change_view(request, object_id, form_url, extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save_and_add_another'] = False
        return super().add_view(request, form_url, extra_context)
