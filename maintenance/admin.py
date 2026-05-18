from django.contrib import admin

from .models import DemandeMaintenance, MessageMaintenance


@admin.register(DemandeMaintenance)
class DemandeMaintenanceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'contrat', 'statut', 'cree_par', 'created_at')
    list_filter = ('statut', 'created_at')
    search_fields = ('titre', 'description')


@admin.register(MessageMaintenance)
class MessageMaintenanceAdmin(admin.ModelAdmin):
    list_display = ('demande', 'auteur', 'created_at')
    search_fields = ('contenu',)