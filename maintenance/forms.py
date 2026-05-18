from django import forms

from .models import DemandeMaintenance, MessageMaintenance


class DemandeMaintenanceForm(forms.ModelForm):
    class Meta:
        model = DemandeMaintenance
        fields = ['titre', 'description']

        labels = {
            'titre': 'Sujet de la demande',
            'description': 'Description du problème',
        }


class MessageMaintenanceForm(forms.ModelForm):
    class Meta:
        model = MessageMaintenance
        fields = ['contenu']

        labels = {
            'contenu': '',
        }

        widgets = {
            'contenu': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Écrire un message...'
            })
        }