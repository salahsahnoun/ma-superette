from django.urls import path
from . import views

app_name = 'commandes'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('confirmation/<int:pk>/', views.confirmation, name='confirmation'),
    path('suivi/<int:pk>/', views.suivi, name='suivi'),
]
