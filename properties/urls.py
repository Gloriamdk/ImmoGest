from django.urls import path

from . import views


app_name = 'properties'

urlpatterns = [
    path('biens/', views.liste_biens, name='liste_biens'),

    path('biens/ajouter/', views.ajouter_bien, name='ajouter_bien'),

    path('biens/archives/', views.biens_archives, name='biens_archives'),

    path('biens/<int:pk>/', views.detail_bien, name='detail_bien'),

    path('locataires/', views.liste_locataires, name='liste_locataires'),

    path('locataires/ajouter/', views.ajouter_locataire, name='ajouter_locataire'),

    path('locataires/<int:pk>/', views.detail_locataire, name='detail_locataire'),

    
    path('locataires/<int:pk>/modifier/', views.modifier_locataire, name='modifier_locataire'),
    
    path('locataires/<int:pk>/supprimer/', views.supprimer_locataire, name='supprimer_locataire'),

    path('mon-contrat/', views.mon_contrat, name='mon_contrat'),
    
    path(
        'biens/<int:pk>/modifier/',
        views.modifier_bien,
        name='modifier_bien'
    ),

    path(
        'biens/<int:pk>/archiver/',
        views.archiver_bien,
        name='archiver_bien'
    ),

    path(
        'biens/<int:pk>/restaurer/',
        views.restaurer_bien,
        name='restaurer_bien'
),

    path('contrats/', views.liste_contrats, name='liste_contrats'),

    path(
        'contrats/ajouter/',
        views.ajouter_contrat,
        name='ajouter_contrat'
    ),

    path(
    'contrats/archives/',
    views.contrats_archives,
    name='contrats_archives'
),

path(
    'locataires/',
    views.liste_locataires,
    name='liste_locataires'
),

path(
    'locataires/ajouter/',
    views.ajouter_locataire,
    name='ajouter_locataire'
),

path(
    'locataires/<int:pk>/',
    views.detail_locataire,
    name='detail_locataire'
),

path(
    'contrats/<int:pk>/modifier/',
    views.modifier_contrat,
    name='modifier_contrat'
),

path(
    'contrats/<int:pk>/resilier/',
    views.resilier_contrat,
    name='resilier_contrat'
),

path(
    'contrats/<int:pk>/archiver/',
    views.archiver_contrat,
    name='archiver_contrat'
),

path(
    'contrats/<int:pk>/restaurer/',
    views.restaurer_contrat,
    name='restaurer_contrat'
),

path(
    'contrats/<int:pk>/',
    views.detail_contrat,
    name='detail_contrat'
),
]