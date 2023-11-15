from django.http import HttpRequest, JsonResponse
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
    queryset = MasterIgrometri.objects.all()
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


class IgrometroAPIView(APIView):
    def post(self, request):
        # Use the existing MasterIgrometriCreateView to handle the request
        create_view = IgrometroCreateView.as_view()
        response = create_view(request._request)

        response.render()

        data = {'message': response.content.decode('utf-8')}

        return JsonResponse(data, status=status.HTTP_201_CREATED)

    def put(self, request):
        # Estrai l'ID dell'oggetto Igrometro
        try:
            igrometro = Igrometro.objects.get(id=request.data.get('id'))
        except Igrometro.DoesNotExist:
            return JsonResponse({'error': 'L\'Igrometro specificato non esiste.'}, status=status.HTTP_404_NOT_FOUND)        # Estrai il campo specifico da modificare dal corpo della richiesta
        updated_fields = []
        for field in Igrometro._meta.get_fields():
            field = field.name
            try:
                campo_da_modificare = request.data.get(field)
            except Exception:
                continue

            if campo_da_modificare is not None and field != 'id':
                # Modifica il campo specifico
                setattr(igrometro, field, campo_da_modificare)
                igrometro.save()
                updated_fields.append(field)

        return JsonResponse({'message': f'Campi {updated_fields} modificati con successo.'}, status=status.HTTP_200_OK)



    def delete(self, request):
        delete_view = IgrometroDestroyView.as_view()

        try:
            pk = request.data.get('id')
        except:
            return JsonResponse({'error': 'ID non fornito.'}, status=status.HTTP_400_BAD_REQUEST)

        #controllo se l'id esiste
        try:
            igrometro = Igrometro.objects.get(id=pk)
        except Igrometro.DoesNotExist:
            return JsonResponse({'error': 'L\'igrometro specificato non esiste.'}, status=status.HTTP_404_NOT_FOUND)
        
        response = delete_view(request._request, pk=pk)

        response.render()

        data = {'message': response.content.decode('utf-8')}
        return JsonResponse(data, status=status.HTTP_204_NO_CONTENT)


class MasterIgrometriAPIView(APIView):
    def post(self, request):
        # Use the existing MasterIgrometriCreateView to handle the request
        create_view = MasterIgrometriCreateView.as_view()
        response = create_view(request._request)

        response.render()

        data = {'message': response.content.decode('utf-8')}

        return JsonResponse(data, status=status.HTTP_201_CREATED)
     
    def put(self, request):
        try:
        # Recupera l'oggetto Igrometro
            master = MasterIgrometri.objects.get(id=request.data.get('id'))
        except MasterIgrometri.DoesNotExist:
            return JsonResponse({'error': 'Il master specificato non esiste.'}, status=status.HTTP_404_NOT_FOUND)
        updated_fields = []
        
        for field in MasterIgrometri._meta.get_fields():
            field = field.name
            try:
                campo_da_modificare = request.data.get(field)
            except Exception:
                print(field + ' non c\'è')
                continue

            if campo_da_modificare is not None and field != 'id':
                # Modifica il campo specifico
                setattr(master, field, campo_da_modificare)
                master.save()
                updated_fields.append(field)


        return JsonResponse({'message': f'Campi {updated_fields} modificati con successo.'}, status=status.HTTP_200_OK)


    def delete(self, request):
        delete_view = MasterIgrometriDestroyView.as_view()

        try:
            pk = request.data.get('id')
        except:
            return JsonResponse({'error': 'ID non fornito.'}, status=status.HTTP_400_BAD_REQUEST)

        #controllo che sista il master
        try:
            master = MasterIgrometri.objects.get(id=pk)
        except MasterIgrometri.DoesNotExist:
            return JsonResponse({'error': 'Il master specificato non esiste.'}, status=status.HTTP_404_NOT_FOUND)

        response = delete_view(request._request, pk=pk)

        response.render()

        data = {'message': response.content.decode('utf-8')}
        return JsonResponse(data, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def aggiungi_ultima_misurazione(request):
    try:
        igrometro_id = request.data.get('id')
        igrometro = Igrometro.objects.get(id=igrometro_id)
        nuova_misurazione = request.data.get('ultima_misurazione')

        #if "umidita" not in nuova_misurazione.keys() or "data" not in nuova_misurazione.keys():
        if not nuova_misurazione.keys() <= set(PARAMS):
            return JsonResponse({'error':'Campi misurazione errati'})

        igrometro.ultima_misurazione = nuova_misurazione
        igrometro.misurazioni.append(nuova_misurazione)
        igrometro.save()
        return JsonResponse({'message': 'Ultima misurazione aggiunta con successo.'}, status=status.HTTP_200_OK)
    except Igrometro.DoesNotExist:
        return JsonResponse({'error': 'L\'igrometro specificato non esiste.'}, status=status.HTTP_404_NOT_FOUND)