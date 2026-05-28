from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from commandes.models import Commande
from .forms import InscriptionForm, ConnexionForm


class ConnexionView(LoginView):
    template_name = 'comptes/connexion.html'
    authentication_form = ConnexionForm

    def get_success_url(self):
        if self.request.user.is_staff:
            return '/admin/'
        return super().get_success_url()


def inscription(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin/')
        return redirect('comptes:profil')
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='comptes.backends.EmailOrPhoneBackend')
            messages.success(request, _('Bienvenue ! Votre compte a été créé.'))
            return redirect('comptes:profil')
    else:
        form = InscriptionForm()
    return render(request, 'comptes/inscription.html', {'form': form})


@login_required
def profil(request):
    if request.user.is_staff:
        return redirect('/admin/')
    commandes = Commande.objects.filter(user=request.user).order_by('-created')
    total_depense = sum(c.total for c in commandes if c.statut != 'annulee')
    return render(request, 'comptes/profil.html', {
        'commandes':     commandes,
        'total_depense': total_depense,
    })
