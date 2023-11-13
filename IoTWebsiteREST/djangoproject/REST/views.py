from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics, status
from .models import *
from .serializer import IgrometroSerializer, MasterIgrometriSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

import json

class IgrometroCreateView(generics.CreateAPIView):
    queryset = Igrometro.objects.all()
    serializer_class = IgrometroSerializer


class MasterIgrometriCreateView(generics.CreateAPIView):
    queryset = Igrometro.objects.all()
    serializer_class = MasterIgrometriSerializer


class IgrometroDestroyView(generics.DestroyAPIView):
    queryset = Igrometro.objects.all()
    serializer_class = IgrometroSerializer

    def perform_destroy(self, instance):
        instance.delete()
        return JsonResponse({'message': 'Igrometro eliminato con successo.'}, status=status.HTTP_204_NO_CONTENT)


class MasterIgrometriDestroyView(generics.DestroyAPIView):
    queryset = MasterIgrometri.objects.all()
    serializer_class = MasterIgrometriSerializer

    def perform_destroy(self, instance):
        instance.delete()
        return Response({'message': 'Master eliminato con successo.'}, status=status.HTTP_204_NO_CONTENT)



class IgrometroUpdateView(generics.UpdateAPIView):
    queryset = Igrometro.objects.all()
    serializer_class = IgrometroSerializer

    def update(self, request, *args, **kwargs):
        # Estrai l'ID dell'oggetto Igrometro
        igrometro_id = kwargs['pk']

        # Estrai il campo specifico da modificare dal corpo della richiesta
        updated_fields = []
        for field in Igrometro._meta.get_fields():
            field = field.name
            try:
                campo_da_modificare = request.data.get(field)
            except Exception:
                continue

            if campo_da_modificare is not None:
                try:
                    # Recupera l'oggetto Igrometro
                    igrometro = self.get_object()
                except Igrometro.DoesNotExist:
                    return Response({'error': 'L\'Igrometro specificato non esiste.'}, status=status.HTTP_404_NOT_FOUND)
                    # Modifica il campo specifico
                setattr(igrometro, field, campo_da_modificare)
                igrometro.save()
                updated_fields.append(field)


        return Response({'message': f'Campi {updated_fields} modificati con successo.'})


class MasterIgrometriUpdateView(generics.UpdateAPIView):
    queryset = MasterIgrometri.objects.all()
    serializer_class = MasterIgrometriSerializer

    def update(self, request, *args, **kwargs):
        # Estrai l'ID dell'oggetto Igrometro
        master_id = kwargs['pk']

        # Estrai il campo specifico da modificare dal corpo della richiesta
        updated_fields = []
        for field in MasterIgrometri._meta.get_fields():
            field = field.name
            try:
                campo_da_modificare = request.data.get(field)
            except Exception:
                continue

            if campo_da_modificare is not None:
                try:
                    # Recupera l'oggetto Igrometro
                    master = self.get_object()
                except Igrometro.DoesNotExist:
                    return Response({'error': 'Il master specificato non esiste.'}, status=status.HTTP_404_NOT_FOUND)
                # Modifica il campo specifico
                setattr(master, field, campo_da_modificare)
                master.save()
                updated_fields.append(field)


        return Response({'message': f'Campi {updated_fields} modificati con successo.'})




@api_view(['POST'])
def aggiungi_ultima_misurazione(request):
    try:
        igrometro_id = request.data.get('id')
        igrometro = Igrometro.objects.get(id=igrometro_id)
        nuova_misurazione = request.data.get('ultima_misurazione')

        print(type(nuova_misurazione))


        #if "umidita" not in nuova_misurazione.keys() or "data" not in nuova_misurazione.keys():
        if not nuova_misurazione.keys() <= set(PARAMS):
            return JsonResponse({'error':'Campi misurazione errati'})

        igrometro.ultima_misurazione = nuova_misurazione
        igrometro.misurazioni.append(nuova_misurazione)
        igrometro.save()
        return JsonResponse({'message': 'Ultima misurazione aggiunta con successo.'})
    except Igrometro.DoesNotExist:
        return JsonResponse({'error': 'L\'ogrometro specificato non esiste.'})