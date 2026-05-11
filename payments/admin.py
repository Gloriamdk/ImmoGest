from django.contrib import admin

from .models import Paiement


@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = (
        'contrat',
        'mois_concerne',
        'montant',
        'date_paiement',
        'mode_paiement',
        'statut',
    )

    list_filter = (
        'statut',
        'mode_paiement',
        'mois_concerne',
    )

    search_fields = (
        'contrat__bien__titre',
        'contrat__locataire__user__username',
        'contrat__locataire__user__email',
    )