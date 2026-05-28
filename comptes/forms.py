import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class InscriptionForm(forms.Form):
    identifiant = forms.CharField(
        label=_("Email ou numéro de téléphone"),
        widget=forms.TextInput(attrs={'placeholder': 'exemple@mail.com ou +213 6XX XXX XXX'}),
    )
    password1 = forms.CharField(
        label=_("Mot de passe"),
        widget=forms.PasswordInput(attrs={'placeholder': '8 caractères minimum'}),
    )
    password2 = forms.CharField(
        label=_("Confirmez le mot de passe"),
        widget=forms.PasswordInput(attrs={'placeholder': 'Répétez le mot de passe'}),
    )

    def _is_email(self, val):
        return '@' in val

    def _normalise_phone(self, val):
        """Supprime espaces/tirets, garde chiffres et + initial."""
        phone = re.sub(r'[\s\-\(\).]', '', val)
        if not re.match(r'^\+?\d{8,15}$', phone):
            raise ValidationError(_("Numéro de téléphone invalide (8 à 15 chiffres)."))
        return phone

    def clean_identifiant(self):
        val = self.cleaned_data['identifiant'].strip()
        if self._is_email(val):
            try:
                validate_email(val)
            except ValidationError:
                raise ValidationError(_("Adresse email invalide."))
            if User.objects.filter(email=val).exists():
                raise ValidationError(_("Cette adresse email est déjà utilisée."))
        else:
            val = self._normalise_phone(val)
            if User.objects.filter(username=val).exists():
                raise ValidationError(_("Ce numéro de téléphone est déjà utilisé."))
        return val

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1', '')
        p2 = cleaned.get('password2', '')
        if p1 and len(p1) < 8:
            self.add_error('password1', _("Le mot de passe doit contenir au moins 8 caractères."))
        if p1 and p2 and p1 != p2:
            self.add_error('password2', _("Les mots de passe ne correspondent pas."))
        return cleaned

    def save(self):
        identifiant = self.cleaned_data['identifiant']
        password    = self.cleaned_data['password1']
        if self._is_email(identifiant):
            username = identifiant[:150]
            user = User(username=username, email=identifiant)
        else:
            user = User(username=identifiant)
        user.set_password(password)
        user.save()
        return user


class ConnexionForm(AuthenticationForm):
    """AuthenticationForm avec libellé adapté (email ou téléphone)."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _("Email ou numéro de téléphone")
        self.fields['username'].widget.attrs['placeholder'] = 'exemple@mail.com ou +213 6XX XXX XXX'
        self.fields['password'].label = _("Mot de passe")
        self.fields['password'].widget.attrs['placeholder'] = '••••••••'
