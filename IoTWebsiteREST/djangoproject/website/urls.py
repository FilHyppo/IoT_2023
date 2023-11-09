from django.urls import path
from .views import lista_master

urlpatterns = [
    # Altri percorsi e viste possono essere aggiunti qui
    path('lista_master/', lista_master, name='lista_master'),
]
