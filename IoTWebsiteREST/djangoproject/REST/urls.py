from django.urls import path
from .views import *

#Se necessario l'id dell'oggetto è contenuto nel json passato, non è presente nell'url

urlpatterns = [
    path('igrometri/', IgrometroAPIView.as_view(), name='igrometro-api'),
    path('masterigrometri/', MasterIgrometriAPIView.as_view(), name='masterigrometri-api'),
    path('igrometri/aggiungi-ultima-misurazione/', aggiungi_ultima_misurazione, name='aggiungi_ultima_misurazione'),
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