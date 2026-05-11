from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    PROPRIETAIRE = 'proprietaire'
    LOCATAIRE = 'locataire'

    ROLE_CHOICES = [
        (PROPRIETAIRE, 'Propriétaire'),
        (LOCATAIRE, 'Locataire'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        verbose_name='Rôle'
    )

    telephone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Téléphone'
    )

    photo = models.ImageField(
        upload_to='profils/',
        blank=True,
        null=True,
        verbose_name='Photo de profil'
    )

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"


class ProfilProprietaire(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profil_proprietaire',
        verbose_name='Utilisateur'
    )

    adresse = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Adresse'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Créé le'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Modifié le'
    )

    class Meta:
        verbose_name = 'Profil propriétaire'
        verbose_name_plural = 'Profils propriétaires'

    def __str__(self):
        return f"Propriétaire : {self.user.username}"


class ProfilLocataire(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profil_locataire',
        verbose_name='Utilisateur'
    )

    proprietaire = models.ForeignKey(
        ProfilProprietaire,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='locataires',
        verbose_name='Propriétaire'
    )
    
    adresse_actuelle = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Adresse actuelle'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Créé le'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Modifié le'
    )

    class Meta:
        verbose_name = 'Profil locataire'
        verbose_name_plural = 'Profils locataires'

    def __str__(self):
        return f"Locataire : {self.user.username}"
