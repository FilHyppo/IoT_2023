from django.urls import path
from .views import *

urlpatterns = [
    # Altri percorsi e viste possono essere aggiunti qui
    path('lista_master/', lista_master, name='lista_master'),
    path('mappa_aree/', mappa_aree, name='mappa_aree')
]
