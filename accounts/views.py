from payments.models import Paiement
from properties.models import Bien, ContratBail
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import ConnexionForm, InscriptionForm, ProfilForm

def home(request):
    return render(request, 'home.html')

def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'proprietaire'
            user.save()

            login(request, user)

            messages.success(
                request,
                "Votre compte propriétaire a été créé avec succès."
            )

            return redirect('accounts:dashboard')
    else:
        form = InscriptionForm()

    return render(request, 'accounts/inscription.html', {
        'form': form
    })


class ConnexionView(LoginView):
    """
    Permet à un utilisateur de se connecter.
    """
    template_name = 'accounts/connexion.html'
    authentication_form = ConnexionForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, "Connexion réussie. Bienvenue sur ImmoGest.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:dashboard')

@login_required
def deconnexion(request):
    """
    Déconnecte l'utilisateur.
    """
    logout(request)
    messages.success(request, "Vous êtes déconnecté.")
    return redirect('accounts:login')


@login_required
def dashboard(request):

    if request.user.role == 'proprietaire':

        profil = request.user.profil_proprietaire

        biens = Bien.objects.filter(
            proprietaire=profil,
            is_archived=False
        )

        contrats = ContratBail.objects.filter(
            bien__proprietaire=profil,
            is_archived=False
        )

        total_biens = biens.count()

        biens_libres = biens.filter(
            statut=Bien.LIBRE
        ).count()

        biens_loues = biens.filter(
            statut=Bien.LOUE
        ).count()

        contrats_actifs = contrats.filter(
            statut=ContratBail.ACTIF
        ).count()

        paiements = Paiement.objects.filter(
        contrat__bien__proprietaire=profil
        )

        total_paiements = sum(
            paiement.montant
            for paiement in paiements.filter(
                statut=Paiement.CONFIRME
            )
        )

        paiements_en_retard = paiements.filter(
            statut=Paiement.EN_RETARD
        ).count()

        derniers_paiements = paiements.order_by(
            '-created_at'
        )[:5]

        derniers_biens = biens.order_by('-created_at')[:5]

        derniers_contrats = contrats.order_by('-created_at')[:5]

        return render(request, 'accounts/dash_proprio.html', {

            'total_biens': total_biens,
            'biens_libres': biens_libres,
            'biens_loues': biens_loues,
            'contrats_actifs': contrats_actifs,

            'total_paiements': total_paiements,
            'paiements_en_retard': paiements_en_retard,
            'derniers_paiements': derniers_paiements,

            'derniers_biens': derniers_biens,
            'derniers_contrats': derniers_contrats,
        })

    elif request.user.role == 'locataire':

        profil = request.user.profil_locataire

        contrat = ContratBail.objects.filter(
            locataire=profil,
            statut=ContratBail.ACTIF,
            is_archived=False
        ).first()

        return render(
            request,
            'accounts/dash_loc.html',
            {
                'contrat': contrat
            }
        )

    messages.error(request, "Votre rôle n'est pas reconnu.")
    return redirect('accounts:login')

@login_required
def profil(request):
    """
    Permet à l'utilisateur connecté de modifier son profil.
    """
    if request.method == 'POST':
        form = ProfilForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été modifié avec succès.")
            return redirect('accounts:profil')
    else:
        form = ProfilForm(instance=request.user)

    return render(request, 'accounts/profil.html', {
        'form': form
    })