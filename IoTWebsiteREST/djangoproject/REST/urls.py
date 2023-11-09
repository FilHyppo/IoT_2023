from django.urls import path
from .views import IdrometroCreateView, MasterIdrometriCreateView

urlpatterns = [
    path('idrometri/create/', IdrometroCreateView.as_view(), name='idrometro-create'),
    path('masteridrometri/create/', MasterIdrometriCreateView.as_view(), name='idrometro-create'),
]
