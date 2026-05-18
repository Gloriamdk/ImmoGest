from django.urls import path

from . import views


app_name = 'maintenance'

urlpatterns = [
    path('', views.liste_demandes, name='liste_demandes'),
    path('nouvelle/', views.nouvelle_demande, name='nouvelle_demande'),
    path('<int:pk>/', views.detail_demande, name='detail_demande'),
    path('<int:pk>/messages/', views.messages_json, name='messages_json'),
]