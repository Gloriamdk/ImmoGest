from django import forms

from .models import Paiement


class PaiementForm(forms.ModelForm):

    class Meta:
        model = Paiement

        fields = [
            'contrat',
            'mois_concerne',
            'montant',
            'date_paiement',
            'mode_paiement',
            'statut',
            'note',
        ]

        labels = {
            'contrat': 'Contrat',
            'mois_concerne': 'Mois concerné',
            'montant': 'Montant',
            'date_paiement': 'Date du paiement',
            'mode_paiement': 'Mode de paiement',
            'statut': 'Statut',
            'note': 'Note',
        }

        widgets = {
            'mois_concerne': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'date_paiement': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'note': forms.Textarea(
                attrs={'rows': 4}
            ),
        }

    def clean_montant(self):
        montant = self.cleaned_data.get('montant')

        if montant <= 0:
            raise forms.ValidationError(
                "Le montant doit être supérieur à zéro."
            )

        return montant

class PaiementMultipleLocataireForm(forms.Form):
    mois_depart = forms.DateField(
        label='Premier mois payé',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    nombre_mois = forms.IntegerField(
        label='Nombre de mois à payer',
        min_value=1,
        max_value=12
    )

    mode_paiement = forms.ChoiceField(
        label='Mode de paiement',
        choices=Paiement.MODE_CHOICES
    )

    note = forms.CharField(
        label='Note',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3})
    )