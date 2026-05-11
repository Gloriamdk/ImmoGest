from django import forms

from .models import Bien, ContratBail


class BienForm(forms.ModelForm):
    class Meta:
        model = Bien
        fields = [
            'titre',
            'type_bien',
            'adresse',
            'ville',
            'superficie',
            'loyer_mensuel',
            'caution',
            'description',
            'image',
            'statut',
        ]

        labels = {
            'titre': 'Titre du bien',
            'type_bien': 'Type de bien',
            'adresse': 'Adresse',
            'ville': 'Ville',
            'superficie': 'Superficie en m²',
            'loyer_mensuel': 'Loyer mensuel',
            'caution': 'Caution',
            'description': 'Description',
            'image': 'Image du bien',
            'statut': 'Statut',
        }


class ContratBailForm(forms.ModelForm):
    class Meta:
        model = ContratBail
        fields = [
            'bien',
            'locataire',
            'date_debut',
            'date_fin',
            'montant_loyer',
            'montant_caution',
            'document',
            'statut',
            'notes',
        ]

        labels = {
            'bien': 'Bien immobilier',
            'locataire': 'Locataire',
            'date_debut': 'Date de début',
            'date_fin': 'Date de fin',
            'montant_loyer': 'Montant du loyer',
            'montant_caution': 'Montant de la caution',
            'document': 'Contrat signé',
            'statut': 'Statut du contrat',
            'notes': 'Notes',
        }

        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        bien = cleaned_data.get('bien')
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')
        statut = cleaned_data.get('statut')

        if date_debut and date_fin and date_fin < date_debut:
            raise forms.ValidationError(
                "La date de fin ne peut pas être avant la date de début."
            )

        if bien and bien.is_archived:
            raise forms.ValidationError(
                "Impossible de créer un contrat sur un bien archivé."
            )

        if bien and statut == ContratBail.ACTIF:
            contrat_existant = ContratBail.objects.filter(
                bien=bien,
                statut=ContratBail.ACTIF,
                is_archived=False
            )

            if self.instance.pk:
                contrat_existant = contrat_existant.exclude(pk=self.instance.pk)

            if contrat_existant.exists():
                raise forms.ValidationError(
                    "Ce bien a déjà un contrat actif."
                )

        return cleaned_data