from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import proprietaire_required
from properties.models import ContratBail

from .forms import PaiementForm
from .models import Paiement


@login_required
@proprietaire_required
def liste_paiements(request):

    profil = request.user.profil_proprietaire
    query = request.GET.get('q', '')

    paiements = Paiement.objects.filter(
        contrat__bien__proprietaire=profil
    )

    if query:
        paiements = paiements.filter(
            contrat__bien__titre__icontains=query
        ) | paiements.filter(
            contrat__locataire__user__username__icontains=query
        )

    return render(request, 'payments/liste_paiements.html', {
        'paiements': paiements,
        'query': query
    })


@login_required
@proprietaire_required
def detail_paiement(request, pk):

    profil = request.user.profil_proprietaire

    paiement = get_object_or_404(
        Paiement,
        pk=pk,
        contrat__bien__proprietaire=profil
    )

    return render(request, 'payments/detail_paiement.html', {
        'paiement': paiement
    })


@login_required
@proprietaire_required
def ajouter_paiement(request):

    profil = request.user.profil_proprietaire

    if request.method == 'POST':

        form = PaiementForm(request.POST)

        form.fields['contrat'].queryset = ContratBail.objects.filter(
            bien__proprietaire=profil,
            statut=ContratBail.ACTIF,
            is_archived=False
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Paiement enregistré avec succès."
            )

            return redirect('payments:liste_paiements')

    else:

        form = PaiementForm()

        form.fields['contrat'].queryset = ContratBail.objects.filter(
            bien__proprietaire=profil,
            statut=ContratBail.ACTIF,
            is_archived=False
        )

    return render(request, 'payments/form_paiement.html', {
        'form': form,
        'titre': 'Ajouter un paiement'
    })


@login_required
@proprietaire_required
def modifier_paiement(request, pk):

    profil = request.user.profil_proprietaire

    paiement = get_object_or_404(
        Paiement,
        pk=pk,
        contrat__bien__proprietaire=profil
    )

    if request.method == 'POST':

        form = PaiementForm(request.POST, instance=paiement)

        form.fields['contrat'].queryset = ContratBail.objects.filter(
            bien__proprietaire=profil,
            statut=ContratBail.ACTIF,
            is_archived=False
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Paiement modifié avec succès."
            )

            return redirect(
                'payments:detail_paiement',
                pk=paiement.pk
            )

    else:

        form = PaiementForm(instance=paiement)

        form.fields['contrat'].queryset = ContratBail.objects.filter(
            bien__proprietaire=profil,
            statut=ContratBail.ACTIF,
            is_archived=False
        )

    return render(request, 'payments/form_paiement.html', {
        'form': form,
        'titre': 'Modifier le paiement'
    })