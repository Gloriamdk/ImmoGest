from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from properties.models import ContratBail

from .forms import DemandeMaintenanceForm, MessageMaintenanceForm
from .models import DemandeMaintenance, MessageMaintenance


def utilisateur_a_acces_demande(user, demande):
    if user.role == 'proprietaire':
        return demande.contrat.bien.proprietaire == user.profil_proprietaire

    if user.role == 'locataire':
        return demande.contrat.locataire == user.profil_locataire

    return False


@login_required
def liste_demandes(request):
    if request.user.role == 'proprietaire':
        demandes = DemandeMaintenance.objects.filter(
            contrat__bien__proprietaire=request.user.profil_proprietaire
        )

    elif request.user.role == 'locataire':
        demandes = DemandeMaintenance.objects.filter(
            contrat__locataire=request.user.profil_locataire
        )

    else:
        demandes = DemandeMaintenance.objects.none()

    return render(request, 'maintenance/liste_demandes.html', {
        'demandes': demandes
    })


@login_required
def nouvelle_demande(request):
    if request.user.role != 'locataire':
        messages.error(request, "Seul un locataire peut créer une demande.")
        return redirect('maintenance:liste_demandes')

    contrat = ContratBail.objects.filter(
        locataire=request.user.profil_locataire,
        statut=ContratBail.ACTIF,
        is_archived=False
    ).first()

    if not contrat:
        messages.error(request, "Vous n'avez pas de contrat actif.")
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = DemandeMaintenanceForm(request.POST)

        if form.is_valid():
            demande = form.save(commit=False)
            demande.contrat = contrat
            demande.cree_par = request.user
            demande.save()

            MessageMaintenance.objects.create(
                demande=demande,
                auteur=request.user,
                contenu=demande.description
            )

            messages.success(request, "Demande de maintenance envoyée.")
            return redirect('maintenance:detail_demande', pk=demande.pk)

    else:
        form = DemandeMaintenanceForm()

    return render(request, 'maintenance/nouvelle_demande.html', {
        'form': form
    })


@login_required
def detail_demande(request, pk):
    demande = get_object_or_404(DemandeMaintenance, pk=pk)

    if not utilisateur_a_acces_demande(request.user, demande):
        messages.error(request, "Accès refusé.")
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = MessageMaintenanceForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.demande = demande
            message.auteur = request.user
            message.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})

            return redirect('maintenance:detail_demande', pk=demande.pk)

    else:
        form = MessageMaintenanceForm()

    return render(request, 'maintenance/detail_demande.html', {
        'demande': demande,
        'form': form
    })


@login_required
def messages_json(request, pk):
    demande = get_object_or_404(DemandeMaintenance, pk=pk)

    if not utilisateur_a_acces_demande(request.user, demande):
        return JsonResponse({'error': 'Accès refusé'}, status=403)

    messages_demande = demande.messages.select_related('auteur')

    data = []

    for message in messages_demande:
        data.append({
            'auteur': message.auteur.username,
            'role': message.auteur.role,
            'contenu': message.contenu,
            'date': message.created_at.strftime('%d/%m/%Y %H:%M')
        })

    return JsonResponse({'messages': data})