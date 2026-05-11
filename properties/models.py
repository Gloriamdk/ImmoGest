from django.db import models
from django.urls import reverse

from accounts.models import ProfilLocataire, ProfilProprietaire


class Bien(models.Model):
    APPARTEMENT = 'appartement'
    VILLA = 'villa'
    STUDIO = 'studio'
    MAISON = 'maison'

    TYPE_BIEN_CHOICES = [
        (APPARTEMENT, 'Appartement'),
        (VILLA, 'Villa'),
        (STUDIO, 'Studio'),
        (MAISON, 'Maison'),
    ]

    LIBRE = 'libre'
    LOUE = 'loue'
    EN_TRAVAUX = 'en_travaux'

    STATUT_CHOICES = [
        (LIBRE, 'Libre'),
        (LOUE, 'Loué'),
        (EN_TRAVAUX, 'En travaux'),
    ]

    proprietaire = models.ForeignKey(
        ProfilProprietaire,
        on_delete=models.CASCADE,
        related_name='biens'
    )

    titre = models.CharField(
        max_length=200
    )

    type_bien = models.CharField(
        max_length=30,
        choices=TYPE_BIEN_CHOICES
    )

    adresse = models.CharField(
        max_length=255
    )

    ville = models.CharField(
        max_length=100,
        default='Lomé'
    )

    superficie = models.PositiveIntegerField(
        help_text='Superficie en m²'
    )

    loyer_mensuel = models.DecimalField(
        max_digits=10,
        decimal_places=0
    )

    caution = models.DecimalField(
        max_digits=10,
        decimal_places=0
    )

    description = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to='biens/',
        blank=True,
        null=True
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default=LIBRE
    )

    is_archived = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = 'Bien immobilier'
        verbose_name_plural = 'Biens immobiliers'
        ordering = ['-created_at']

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return reverse('properties:detail_bien', kwargs={'pk': self.pk})


class ContratBail(models.Model):
    ACTIF = 'actif'
    RESILIE = 'resilie'
    EXPIRE = 'expire'

    STATUT_CHOICES = [
        (ACTIF, 'Actif'),
        (RESILIE, 'Résilié'),
        (EXPIRE, 'Expiré'),
    ]

    bien = models.ForeignKey(
        Bien,
        on_delete=models.CASCADE,
        related_name='contrats'
    )

    locataire = models.ForeignKey(
        ProfilLocataire,
        on_delete=models.CASCADE,
        related_name='contrats'
    )

    date_debut = models.DateField()

    date_fin = models.DateField(
        blank=True,
        null=True
    )

    montant_loyer = models.DecimalField(
        max_digits=10,
        decimal_places=0
    )

    montant_caution = models.DecimalField(
        max_digits=10,
        decimal_places=0
    )

    document = models.FileField(
        upload_to='contrats/',
        blank=True,
        null=True
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default=ACTIF
    )

    notes = models.TextField(
        blank=True
    )

    is_archived = models.BooleanField(
    default=False
    
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = 'Contrat de bail'
        verbose_name_plural = 'Contrats de bail'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.bien} - {self.locataire.user.username}"