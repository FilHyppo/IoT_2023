from django.shortcuts import render
from rest_framework import generics
from .models import Igrometro
from .serializer import IgrometroSerializer, MasterIgrometriSerializer

class IgrometroCreateView(generics.CreateAPIView):
    queryset = Igrometro.objects.all()
    serializer_class = IgrometroSerializer

class MasterIgrometriCreateView(generics.CreateAPIView):
    queryset = Igrometro.objects.all()
    serializer_class = MasterIgrometriSerializer