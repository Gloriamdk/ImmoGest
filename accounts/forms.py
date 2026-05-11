from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User


class InscriptionForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Adresse email'
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'role',
            'telephone',
            'photo',
            'password1',
            'password2',
        ]

        labels = {
            'username': "Nom d'utilisateur",
            'role': 'Rôle',
            'telephone': 'Téléphone',
            'photo': 'Photo de profil',
        }


class ConnexionForm(AuthenticationForm):
    username = forms.CharField(
        label="Nom d'utilisateur"
    )

    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput
    )


class ProfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'telephone',
            'photo',
        ]

        labels = {
            'username': "Nom d'utilisateur",
            'email': 'Adresse email',
            'telephone': 'Téléphone',
            'photo': 'Photo de profil',
        }