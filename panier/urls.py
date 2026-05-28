from django.urls import path
from . import views

app_name = 'panier'

urlpatterns = [
    path('', views.detail, name='detail'),
    path('ajouter/<int:produit_id>/', views.ajouter, name='ajouter'),
    path('modifier/<int:produit_id>/', views.modifier, name='modifier'),
    path('supprimer/<int:produit_id>/', views.supprimer, name='supprimer'),
]
