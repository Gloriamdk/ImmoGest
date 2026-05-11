from django.contrib import admin

from .models import Bien, ContratBail


@admin.register(Bien)
class BienAdmin(admin.ModelAdmin):
    list_display = (
        'titre',
        'proprietaire',
        'type_bien',
        'ville',
        'loyer_mensuel',
        'statut',
        'is_archived',
        'created_at',
    )
    list_filter = ('type_bien', 'statut', 'is_archived', 'ville')
    search_fields = ('titre', 'adresse', 'ville', 'proprietaire__user__username')


@admin.register(ContratBail)
class ContratBailAdmin(admin.ModelAdmin):
    list_display = (
        'bien',
        'locataire',
        'date_debut',
        'date_fin',
        'montant_loyer',
        'statut',
    )
    list_filter = ('statut', 'date_debut')
    search_fields = (
        'bien__titre',
        'locataire__user__username',
        'locataire__user__email',
    )