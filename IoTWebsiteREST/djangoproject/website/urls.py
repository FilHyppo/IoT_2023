from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views
from .views import *
app_name = 'website'

urlpatterns = [
    # Altri percorsi e viste possono essere aggiunti qui
    path('lista_master/', lista_master, name='lista_master'),
    path('mappa_aree/', mappa_aree, name='mappa_aree'),
    path('homepage/', homepage, name='homepage'),
    path("logout/", views.custom_logout, name="logout"),
    path('search/', MasterIgrometriSearchView.as_view(), name='search-view'),
    path('aggiungi_irrigatore/', AggiungiIrrigatoreView.as_view(), name='aggiungi_irrigatore'),
    path('hygrometer/<int:igrometro_id>/', igrometro_detail_and_edit, name='igrometro_detail_and_edit'),
    path('master/<int:master_id>/', master_detail_and_edit, name='master_detail_and_edit'),
    path('sprinkler/<int:sprinkler_id>/', sprinkler_detail_and_edit, name='sprinkler_detail_and_edit')
]

