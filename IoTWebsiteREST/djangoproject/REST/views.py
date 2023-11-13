from django.shortcuts import render
from rest_framework import generics
from .models import Igrometro
from .serializer import IgrometroSerializer, MasterIgrometriSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

class IgrometroCreateView(generics.CreateAPIView):
    queryset = Igrometro.objects.all()
    serializer_class = IgrometroSerializer

    class LatestIgrometroView(APIView):
        def get(self, request):
            latest_reading = Igrometro.objects.order_by('-data').first()
            serializer = IgrometroSerializer(latest_reading)
            return Response(serializer.data)

class MasterIgrometriCreateView(generics.CreateAPIView):
    queryset = Igrometro.objects.all()
    serializer_class = MasterIgrometriSerializer