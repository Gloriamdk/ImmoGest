from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, ProfilProprietaire, ProfilLocataire


@receiver(post_save, sender=User)
def creer_profil_utilisateur(sender, instance, created, **kwargs):
    """
    Crée automatiquement un profil propriétaire ou locataire
    après la création d'un utilisateur.
    """
    if created:
        if instance.role == User.PROPRIETAIRE:
            ProfilProprietaire.objects.create(user=instance)

        elif instance.role == User.LOCATAIRE:
            ProfilLocataire.objects.create(user=instance)