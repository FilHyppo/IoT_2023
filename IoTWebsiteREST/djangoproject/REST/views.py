from django.shortcuts import render
from rest_framework import generics
from .models import Idrometro
from .serializer import IdrometroSerializer, MasterIdrometriSerializer

class IdrometroCreateView(generics.CreateAPIView):
    queryset = Idrometro.objects.all()
    serializer_class = IdrometroSerializer

class MasterIdrometriCreateView(generics.CreateAPIView):
    queryset = Idrometro.objects.all()
    serializer_class = MasterIdrometriSerializer