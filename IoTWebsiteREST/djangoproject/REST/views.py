from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import generics, status
from .models import *
from .serializer import IgrometroSerializer, MasterIgrometriSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is None:
            name = request.GET.get('name')
            print(name)
            igrometro = Igrometro.objects.filter(nome__icontains=name)
            if igrometro is None:
                return JsonResponse({'error': 'L\'igrometro specificato non esiste.'}, status=status.HTTP_404_NOT_FOUND)
            igrometro = [igrometro.values()[i] for i in range(len(igrometro.values()))]
            return JsonResponse({'data': igrometro}, status=status.HTTP_200_OK)
        try:
            igrometro = Igrometro.objects.get(id=pk)
        except Igrometro.DoesNotExist:
            return JsonResponse({'error': 'L\'igrometro specificato non esiste.'}, status=status.HTTP_404_NOT_FOUND)
        # voglio ritornare un json con tutte le ultime misurazioni degli igrometri sotto il master
        data = []
        if igrometro.ultima_misurazione is not None:
            data.append({'id': igrometro.id, 'nome': igrometro.nome, 'misurazioni': igrometro.misurazioni})
        return JsonResponse({'data': data}, status=status.HTTP_200_OK)

    def post(self, request):
        # Use the existing MasterIgrometriCreateView to handle the request
        create_view = IgrometroCreateView.as_view()
        response = create_view(request._request)

        response.render()

        data = {'message': response.content.decode('utf-8')}

        return JsonResponse(data, status=response.status_code)

    def put(self, request, pk=None):
        try:
            igrometro = Igrometro.objects.get(id=pk)
        except Igrometro.DoesNotExist:
            return JsonResponse({'error': 'L\'igrometro specificato non esiste.'},
                                status=status.HTTP_404_NOT_FOUND)  # Estrai il campo specifico da modificare dal corpo della richiesta
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

    def delete(self, request, pk=None):
        delete_view = IgrometroDestroyView.as_view()
        # controllo se l'id esiste
        try:
            igrometro = Igrometro.objects.get(id=pk)
        except Igrometro.DoesNotExist:
            return JsonResponse({'error': 'L\'igrometro specificato non esiste.'}, status=status.HTTP_404_NOT_FOUND)

        response = delete_view(request._request, pk=pk)

        response.render()

        data = {'message': response.content.decode('utf-8')}
        return JsonResponse(data, status=response.status_code)


class MasterIgrometriAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        if pk is None:
            name = request.GET.get('name')
            print(name)
            igrometro = MasterIgrometri.objects.filter(nome__icontains=name)
            if igrometro is None:
                return JsonResponse({'error': 'Il master specificato non esiste.'}, status=status.HTTP_404_NOT_FOUND)
            igrometro = [igrometro.values()[i] for i in range(len(igrometro.values()))]
            return JsonResponse({'data': igrometro}, status=status.HTTP_200_OK)
        try:
            # Recupera l'oggetto Igrometro
            master = MasterIgrometri.objects.get(id=pk)
        except MasterIgrometri.DoesNotExist:
            return JsonResponse({'error': 'Il master specificato non esiste.'}, status=status.HTTP_404_NOT_FOUND)
        # voglio ritornare un json con tutte le ultime misurazioni degli igrometri sotto il master
        igrometri = Igrometro.objects.filter(master=master.id)
        data = []
        for igrometro in igrometri:
            if igrometro.ultima_misurazione is not None:
                data.append({'id': igrometro.id, 'nome': igrometro.nome, 'misurazioni': igrometro.misurazioni})
        return JsonResponse({'data': data}, status=status.HTTP_200_OK)

    def post(self, request):
        # Use the existing MasterIgrometriCreateView to handle the request
        create_view = MasterIgrometriCreateView.as_view()
        response = create_view(request._request)

        response.render()

        data = {'message': response.content.decode('utf-8')}

        return JsonResponse(data, status=response.status_code)

    def put(self, request, pk=None):
        try:
            # Recupera l'oggetto Igrometro
            master = MasterIgrometri.objects.get(id=pk)
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

    def delete(self, request, pk=None):
        delete_view = MasterIgrometriDestroyView.as_view()
        # controllo che esista il master
        try:
            master = MasterIgrometri.objects.get(id=pk)
        except MasterIgrometri.DoesNotExist:
            return JsonResponse({'error': 'Il master specificato non esiste.'}, status=status.HTTP_404_NOT_FOUND)

        response = delete_view(request._request, pk=pk)

        response.render()

        data = {'message': response.content.decode('utf-8')}
        return JsonResponse(data, status=response.status_code)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST', 'DELETE'])
def misurazioni(request, pk):
    try:
        Igrometro.objects.get(id=pk)
    except Igrometro.DoesNotExist:
        return JsonResponse({'error': 'L\'igrometro specificato non esiste.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        return aggiungi_ultima_misurazione(request._request, pk)
    elif request.method == 'DELETE':
        return cancella_ultima_misurazione(request._request, pk)
    else:
        return JsonResponse({'error': 'Metodo non supportato.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def aggiungi_ultima_misurazione(request, igrometro_id):
    igrometro = Igrometro.objects.get(id=igrometro_id)
    nuova_misurazione = request.data.get('ultima_misurazione')
    # if "umidita" not in nuova_misurazione.keys() or "data" not in nuova_misurazione.keys():
    if not nuova_misurazione.keys() <= set(PARAMS):
        return JsonResponse({'error': 'Campi misurazione errati'})
    igrometro.ultima_misurazione = nuova_misurazione
    igrometro.misurazioni.append(nuova_misurazione)
    igrometro.save()
    return JsonResponse({'message': 'Ultima misurazione aggiunta con successo.'}, status=status.HTTP_200_OK)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def cancella_ultima_misurazione(request, igrometro_id):
    igrometro = Igrometro.objects.get(id=igrometro_id)
    # Verifica che ci siano misurazioni da cancellare
    if not igrometro.misurazioni:
        return JsonResponse({'error': 'Nessuna misurazione da cancellare.'}, status=status.HTTP_400_BAD_REQUEST)
    # Rimuovi l'ultima misurazione
    ultima_misurazione = igrometro.misurazioni.pop()
    # ultima misurazione diventa quella in fondo alla lista
    igrometro.ultima_misurazione = igrometro.misurazioni[-1] if len(
        igrometro.misurazioni) > 0 else None  # Puoi impostare l'ultima misurazione su None se vuoi
    igrometro.save()
    return JsonResponse({'message': 'Ultima misurazione cancellata con successo.'}, status=status.HTTP_200_OK)


class CustomAuthToken(APIView):
    def get(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        username = request.data.get('username')
        user = authenticate(request, email=email, password=password, username=username)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
