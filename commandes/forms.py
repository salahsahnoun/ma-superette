from django import forms
from .models import Commande


class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['nom', 'telephone', 'mode_livraison', 'adresse', 'heure_retrait', 'note']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom complet',
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '06 12 34 56 78',
            }),
            'mode_livraison': forms.RadioSelect(attrs={
                'class': 'mode-radio',
            }),
            'adresse': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Numéro, rue, code postal, ville...',
            }),
            'heure_retrait': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
            }),
            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Instructions particulières (optionnel)',
            }),
        }
        labels = {
            'nom': 'Nom complet',
            'telephone': 'Téléphone',
            'mode_livraison': 'Comment souhaitez-vous récupérer votre commande ?',
            'adresse': 'Adresse de livraison',
            'heure_retrait': 'Heure de passage prévue',
            'note': 'Note (optionnel)',
        }

    def clean(self):
        cleaned_data = super().clean()
        mode = cleaned_data.get('mode_livraison')
        adresse = cleaned_data.get('adresse', '').strip()
        heure = cleaned_data.get('heure_retrait')

        if mode == 'livraison' and not adresse:
            self.add_error('adresse', 'L\'adresse de livraison est obligatoire.')

        if mode == 'retrait' and not heure:
            self.add_error('heure_retrait', 'Veuillez indiquer l\'heure à laquelle vous passerez.')

        return cleaned_data
