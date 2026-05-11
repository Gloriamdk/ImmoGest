from django.urls import path

from . import views


app_name = 'payments'

urlpatterns = [
    path('', views.liste_paiements, name='liste_paiements'),

    path(
        'ajouter/',
        views.ajouter_paiement,
        name='ajouter_paiement'
    ),

    path(
        '<int:pk>/',
        views.detail_paiement,
        name='detail_paiement'
    ),

    path(
        '<int:pk>/modifier/',
        views.modifier_paiement,
        name='modifier_paiement'
    ),
]