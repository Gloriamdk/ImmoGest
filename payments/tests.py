from django.db import models
from django.urls import reverse

from properties.models import ContratBail


class Paiement(models.Model):
    EN_ATTENTE = 'en_attente'
    CONFIRME = 'confirme'
    EN_RETARD = 'en_retard'

    STATUT_CHOICES = [
        (EN_ATTENTE, 'En attente'),
        (CONFIRME, 'Confirmé'),
        (EN_RETARD, 'En retard'),
    ]

    ESPECES = 'especes'
    MOBILE_MONEY = 'mobile_money'
    VIREMENT = 'virement'
    CHEQUE = 'cheque'

    MODE_CHOICES = [
        (ESPECES, 'Espèces'),
        (MOBILE_MONEY, 'Mobile Money'),
        (VIREMENT, 'Virement bancaire'),
        (CHEQUE, 'Chèque'),
    ]

    contrat = models.ForeignKey(
        ContratBail,
        on_delete=models.CASCADE,
        related_name='paiements'
    )

    mois_concerne = models.DateField(
        verbose_name='Mois concerné'
    )

    montant = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        verbose_name='Montant'
    )

    date_paiement = models.DateField(
        verbose_name='Date de paiement'
    )

    mode_paiement = models.CharField(
        max_length=30,
        choices=MODE_CHOICES,
        verbose_name='Mode de paiement'
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default=EN_ATTENTE,
        verbose_name='Statut'
    )

    note = models.TextField(
        blank=True,
        verbose_name='Note'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = 'Paiement'
        verbose_name_plural = 'Paiements'
        ordering = ['-mois_concerne']

    def __str__(self):
        return f"{self.contrat} - {self.mois_concerne} - {self.montant} FCFA"

    def get_absolute_url(self):
        return reverse('payments:detail_paiement', kwargs={'pk': self.pk})