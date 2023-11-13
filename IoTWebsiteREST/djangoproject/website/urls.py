from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import *
app_name = 'website'

urlpatterns = [
    # Altri percorsi e viste possono essere aggiunti qui
    path('lista_master/', lista_master, name='lista_master'),
    path('mappa_aree/', mappa_aree, name='mappa_aree'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path("logout/", views.custom_logout, name="logout"),
]
