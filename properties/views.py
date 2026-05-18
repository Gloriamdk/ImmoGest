from django.contrib.auth import get_user_model
from accounts.models import ProfilLocataire
from payments.models import Paiement
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import proprietaire_required
from .forms import BienForm, ContratBailForm
from .models import Bien, ContratBail


@login_required
@proprietaire_required
def liste_biens(request):
    profil = request.user.profil_proprietaire
    query = request.GET.get('q', '')

    biens = Bien.objects.filter(proprietaire=profil, is_archived=False)

    if query:
        biens = biens.filter(titre__icontains=query) | biens.filter(adresse__icontains=query) | biens.filter(ville__icontains=query)

    return render(request, 'properties/liste_biens.html', {
        'biens': biens,
        'query': query
    })


@login_required
@proprietaire_required
def biens_archives(request):
    profil = request.user.profil_proprietaire
    query = request.GET.get('q', '')

    biens = Bien.objects.filter(proprietaire=profil, is_archived=True)

    if query:
        biens = biens.filter(titre__icontains=query) | biens.filter(adresse__icontains=query) | biens.filter(ville__icontains=query)

    return render(request, 'properties/biens_archives.html', {
        'biens': biens,
        'query': query
    })


@login_required
@proprietaire_required
def detail_bien(request, pk):
    profil = request.user.profil_proprietaire
    bien = get_object_or_404(Bien, pk=pk, proprietaire=profil)
    contrats = bien.contrats.all()

    return render(request, 'properties/detail_bien.html', {
        'bien': bien,
        'contrats': contrats
    })


@login_required
@proprietaire_required
def ajouter_bien(request):
    profil = request.user.profil_proprietaire

    if request.method == 'POST':
        form = BienForm(request.POST, request.FILES)

        if form.is_valid():
            bien = form.save(commit=False)
            bien.proprietaire = profil
            bien.save()
            messages.success(request, "Bien ajouté avec succès.")
            return redirect('properties:liste_biens')
        else:
            messages.error(request, "Impossible d'ajouter le bien.")
    else:
        form = BienForm()

    return render(request, 'properties/form_bien.html', {
        'form': form,
        'titre': 'Ajouter un bien'
    })


@login_required
@proprietaire_required
def modifier_bien(request, pk):
    profil = request.user.profil_proprietaire
    bien = get_object_or_404(Bien, pk=pk, proprietaire=profil)

    if request.method == 'POST':
        form = BienForm(request.POST, request.FILES, instance=bien)

        if form.is_valid():
            form.save()
            messages.success(request, "Bien modifié avec succès.")
            return redirect('properties:detail_bien', pk=bien.pk)
    else:
        form = BienForm(instance=bien)

    return render(request, 'properties/form_bien.html', {
        'form': form,
        'titre': 'Modifier le bien'
    })


@login_required
@proprietaire_required
def archiver_bien(request, pk):
    profil = request.user.profil_proprietaire
    bien = get_object_or_404(Bien, pk=pk, proprietaire=profil)

    if request.method == 'POST':
        bien.is_archived = True
        bien.save()
        messages.success(request, "Bien archivé avec succès.")
        return redirect('properties:liste_biens')

    return render(request, 'properties/confirmer_archivage_bien.html', {
        'bien': bien
    })


@login_required
@proprietaire_required
def restaurer_bien(request, pk):
    profil = request.user.profil_proprietaire
    bien = get_object_or_404(Bien, pk=pk, proprietaire=profil, is_archived=True)

    if request.method == 'POST':
        bien.is_archived = False
        bien.save()
        messages.success(request, "Bien restauré avec succès.")
        return redirect('properties:biens_archives')

    return render(request, 'properties/confirmer_restauration_bien.html', {
        'bien': bien
    })


@login_required
@proprietaire_required
def liste_contrats(request):
    profil = request.user.profil_proprietaire
    query = request.GET.get('q', '')

    contrats = ContratBail.objects.filter(
        bien__proprietaire=profil,
        is_archived=False
    )

    if query:
        contrats = contrats.filter(bien__titre__icontains=query) | contrats.filter(locataire__user__username__icontains=query) | contrats.filter(locataire__user__email__icontains=query)

    return render(request, 'properties/liste_contrats.html', {
        'contrats': contrats,
        'query': query
    })


@login_required
@proprietaire_required
def contrats_archives(request):
    profil = request.user.profil_proprietaire
    query = request.GET.get('q', '')

    contrats = ContratBail.objects.filter(
        bien__proprietaire=profil,
        is_archived=True
    )

    if query:
        contrats = contrats.filter(bien__titre__icontains=query) | contrats.filter(locataire__user__username__icontains=query) | contrats.filter(locataire__user__email__icontains=query)

    return render(request, 'properties/contrats_archives.html', {
        'contrats': contrats,
        'query': query
    })

@login_required
@proprietaire_required
def ajouter_contrat(request):
    profil = request.user.profil_proprietaire

    if request.method == 'POST':
        form = ContratBailForm(request.POST, request.FILES)
        form.fields['bien'].queryset = Bien.objects.filter(proprietaire=profil, is_archived=False)
        form.fields['locataire'].queryset = ProfilLocataire.objects.filter(proprietaire=profil)

        if form.is_valid():
            contrat = form.save()
            contrat.bien.statut = Bien.LOUE
            contrat.bien.save()
            messages.success(request, "Contrat créé avec succès.")
            return redirect('properties:liste_contrats')
        else:
            messages.error(request, "Impossible de créer le contrat.")
    else:
        form = ContratBailForm()
        form.fields['bien'].queryset = Bien.objects.filter(proprietaire=profil, is_archived=False)
        form.fields['locataire'].queryset = ProfilLocataire.objects.filter(proprietaire=profil)

    return render(request, 'properties/form_contrat.html', {
        'form': form,
        'titre': 'Créer un contrat'
    })

@login_required
@proprietaire_required
def detail_contrat(request, pk):
    profil = request.user.profil_proprietaire
    contrat = get_object_or_404(ContratBail, pk=pk, bien__proprietaire=profil)

    return render(request, 'properties/detail_contrat.html', {
        'contrat': contrat
    })


@login_required
@proprietaire_required
def modifier_contrat(request, pk):
    profil = request.user.profil_proprietaire
    contrat = get_object_or_404(ContratBail, pk=pk, bien__proprietaire=profil)

    if request.method == 'POST':
        form = ContratBailForm(request.POST, request.FILES, instance=contrat)
        form.fields['bien'].queryset = Bien.objects.filter(proprietaire=profil, is_archived=False)

        if form.is_valid():
            form.save()
            messages.success(request, "Contrat modifié avec succès.")
            return redirect('properties:detail_contrat', pk=contrat.pk)
    else:
        form = ContratBailForm(instance=contrat)
        form.fields['bien'].queryset = Bien.objects.filter(proprietaire=profil, is_archived=False)

    return render(request, 'properties/form_contrat.html', {
        'form': form,
        'titre': 'Modifier le contrat'
    })


@login_required
@proprietaire_required
def resilier_contrat(request, pk):
    profil = request.user.profil_proprietaire
    contrat = get_object_or_404(ContratBail, pk=pk, bien__proprietaire=profil)

    if request.method == 'POST':
        contrat.statut = ContratBail.RESILIE
        contrat.save()

        contrat.bien.statut = Bien.LIBRE
        contrat.bien.save()

        messages.success(request, "Contrat résilié avec succès.")
        return redirect('properties:detail_contrat', pk=contrat.pk)

    return render(request, 'properties/confirmer_resiliation_contrat.html', {
        'contrat': contrat
    })


@login_required
@proprietaire_required
def archiver_contrat(request, pk):
    profil = request.user.profil_proprietaire
    contrat = get_object_or_404(ContratBail, pk=pk, bien__proprietaire=profil)

    if request.method == 'POST':
        contrat.is_archived = True
        contrat.save()
        messages.success(request, "Contrat archivé avec succès.")
        return redirect('properties:liste_contrats')

    return render(request, 'properties/confirmer_archivage_contrat.html', {
        'contrat': contrat
    })


@login_required
@proprietaire_required
def restaurer_contrat(request, pk):
    profil = request.user.profil_proprietaire
    contrat = get_object_or_404(
        ContratBail,
        pk=pk,
        bien__proprietaire=profil,
        is_archived=True
    )

    if request.method == 'POST':
        contrat.is_archived = False
        contrat.save()
        messages.success(request, "Contrat restauré avec succès.")
        return redirect('properties:contrats_archives')

    return render(request, 'properties/confirmer_restauration_contrat.html', {
        'contrat': contrat
    })

@login_required
@proprietaire_required
def liste_locataires(request):
    proprietaire = request.user.profil_proprietaire
    query = request.GET.get('q', '')

    locataires = ProfilLocataire.objects.filter(proprietaire=proprietaire)

    if query:
        locataires = locataires.filter(
            Q(user__username__icontains=query) |
            Q(user__email__icontains=query) |
            Q(user__telephone__icontains=query)
        )

    return render(request, 'properties/liste_locataires.html', {
        'locataires': locataires,
        'query': query
    })


@login_required
@proprietaire_required
def detail_locataire(request, pk):
    proprietaire = request.user.profil_proprietaire

    locataire = get_object_or_404(
        ProfilLocataire,
        pk=pk,
        proprietaire=proprietaire
    )

    contrats = ContratBail.objects.filter(
        locataire=locataire,
        bien__proprietaire=proprietaire
    )

    paiements = Paiement.objects.filter(
        contrat__locataire=locataire,
        contrat__bien__proprietaire=proprietaire
    )

    return render(request, 'properties/detail_locataire.html', {
        'locataire': locataire,
        'contrats': contrats,
        'paiements': paiements
    })

@login_required
@proprietaire_required
def modifier_locataire(request, pk):
    proprietaire = request.user.profil_proprietaire

    locataire = get_object_or_404(
        ProfilLocataire,
        pk=pk,
        proprietaire=proprietaire
    )

    if request.method == 'POST':
        user = locataire.user

        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.telephone = request.POST.get('telephone')
        user.save()

        locataire.adresse_actuelle = request.POST.get('adresse')
        locataire.save()

        messages.success(request, "Locataire modifié avec succès.")
        return redirect('properties:detail_locataire', pk=locataire.pk)

    return render(request, 'properties/modifier_locataire.html', {
        'locataire': locataire
    })    

@login_required
@proprietaire_required
def supprimer_locataire(request, pk):
    proprietaire = request.user.profil_proprietaire

    locataire = get_object_or_404(
        ProfilLocataire,
        pk=pk,
        proprietaire=proprietaire
    )

    if request.method == 'POST':
        user = locataire.user
        user.delete()

        messages.success(request, "Locataire supprimé avec succès.")
        return redirect('properties:liste_locataires')

    return render(request, 'properties/confirmer_suppression_locataire.html', {
        'locataire': locataire
    })

@login_required
@proprietaire_required
def ajouter_locataire(request):
    proprietaire = request.user.profil_proprietaire
    User = get_user_model()

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        adresse = request.POST.get('adresse')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur existe déjà.")
            return redirect('properties:ajouter_locataire')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet email existe déjà.")
            return redirect('properties:ajouter_locataire')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='locataire'
        )

        user.telephone = telephone
        user.save()

        profil_locataire = user.profil_locataire
        profil_locataire.proprietaire = proprietaire
        profil_locataire.adresse_actuelle = adresse
        profil_locataire.save()

        messages.success(request, "Locataire créé avec succès.")
        return redirect('properties:liste_locataires')

    return render(request, 'properties/ajouter_locataire.html')

@login_required
def mon_contrat(request):
    if request.user.role != 'locataire':
        return redirect('accounts:dashboard')

    locataire = request.user.profil_locataire

    contrats = ContratBail.objects.filter(
        locataire=locataire,
        is_archived=False
    )

    return render(request, 'properties/mon_contrat.html', {
        'contrats': contrats
    })