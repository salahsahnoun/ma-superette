from django.urls import path
from . import views

app_name = 'produits'

urlpatterns = [
    path('', views.liste, name='liste'),
    path('categorie/<slug:slug>/', views.par_categorie, name='par_categorie'),
    path('<int:pk>/<slug:slug>/', views.detail, name='detail'),
]
