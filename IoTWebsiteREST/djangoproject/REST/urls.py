from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token
from allauth.account.views import LoginView, LogoutView

# Se necessario l'id dell'oggetto è contenuto nel json passato, non è presente nell'url

urlpatterns = [
    path('igrometri/', IgrometroAPIView.as_view(), name='igrometro-api'),
    path('igrometri/<int:pk>/', IgrometroAPIView.as_view(), name='igrometro-api-pk'),
    path('igrometri/<int:pk>/misurazioni/', misurazioni, name='misurazioni-api'),
    path('masterigrometri/', MasterIgrometriAPIView.as_view(), name='masterigrometri-api'),
    path('masterigrometri/<int:pk>/', MasterIgrometriAPIView.as_view(), name='masterigrometri-api-pk'),

    path('token/', CustomAuthToken.as_view(), name='token-api'),
]

"""     
    path('igrometri/create/', IgrometroCreateView.as_view(), name='igrometro-create'),
    path('igrometri/<int:pk>/delete/', IgrometroDestroyView.as_view(), name='igrometro-delete'),
    path('igrometri/<int:pk>/update/', IgrometroUpdateView.as_view(), name='update-igrometro'),
 """

""" 
    path('masterigrometri/create/', MasterIgrometriCreateView.as_view(), name='master-create'),
    path('masterigrometri/<int:pk>/delete/', MasterIgrometriDestroyView.as_view(), name='master-delete'),
    path('masterigrometri/<int:pk>/update/', MasterIgrometriUpdateView.as_view(), name='master-update'),
 """

"""
    path('igrometri/aggiungi-ultima-misurazione/', aggiungi_ultima_misurazione, name='aggiungi_ultima_misurazione'),
    path('igrometri/elimina-misurazione/', cancella_ultima_misurazione, name='elimina_misurazione'),
"""