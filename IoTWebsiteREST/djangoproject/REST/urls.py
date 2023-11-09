from django.urls import path
from .views import IgrometroCreateView, MasterIgrometriCreateView

urlpatterns = [
    path('igrometri/create/', IgrometroCreateView.as_view(), name='igrometro-create'),
    path('masterigrometri/create/', MasterIgrometriCreateView.as_view(), name='igrometro-create'),
]
