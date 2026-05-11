from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ProfilProprietaire, ProfilLocataire


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'telephone', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'telephone')

    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('role', 'telephone', 'photo')
        }),
    )


@admin.register(ProfilProprietaire)
class ProfilProprietaireAdmin(admin.ModelAdmin):
    list_display = ('user', 'adresse', 'created_at')
    search_fields = ('user__username', 'user__email', 'adresse')


@admin.register(ProfilLocataire)
class ProfilLocataireAdmin(admin.ModelAdmin):
    list_display = ('user', 'adresse_actuelle', 'created_at')
    search_fields = ('user__username', 'user__email', 'adresse_actuelle')