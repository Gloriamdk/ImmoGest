from django.conf import settings
from django.db import models

from properties.models import ContratBail


class DemandeMaintenance(models.Model):
    OUVERTE = 'ouverte'
    EN_COURS = 'en_cours'
    RESOLUE = 'resolue'

    STATUT_CHOICES = [
        (OUVERTE, 'Ouverte'),
        (EN_COURS, 'En cours'),
        (RESOLUE, 'Résolue'),
    ]

    contrat = models.ForeignKey(
        ContratBail,
        on_delete=models.CASCADE,
        related_name='demandes_maintenance'
    )

    titre = models.CharField(max_length=200)

    description = models.TextField()

    cree_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='demandes_maintenance'
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default=OUVERTE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.titre


class MessageMaintenance(models.Model):
    demande = models.ForeignKey(
        DemandeMaintenance,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    contenu = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message de {self.auteur.username}"