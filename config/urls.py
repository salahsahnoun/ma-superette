from django.contrib import admin
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Administration — Ma Superette"
admin.site.site_title = "Ma Superette"
admin.site.index_title = "Tableau de bord"


def admin_deconnexion(request):
    auth_logout(request)
    return redirect('/admin/login/')


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/deconnexion/', admin_deconnexion, name='admin_deconnexion'),
    path('admin/', admin.site.urls),
    path('', include('produits.urls', namespace='produits')),
    path('panier/', include('panier.urls', namespace='panier')),
    path('commandes/', include('commandes.urls', namespace='commandes')),
    path('comptes/',   include('comptes.urls',   namespace='comptes')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
