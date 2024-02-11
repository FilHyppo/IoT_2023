from django.http import JsonResponse
from django.shortcuts import render
from . import tasks
from djangoproject.celery import debug_task 
from django.conf import settings
from .MQTT_client import MQTT_client
from REST.models import Irrigatore


def celery_sprinkle(request, sprinkler_id, duration):
    # Ora puoi usare sprinkler_id e duration nella tua logica per attivare lo sprinkler per la durata specificata
    # Ad esempio, potresti chiamare la tua funzione Celery per attivare lo sprinkler con id=sprinkler_id per la durata specificata.
    result = tasks.sprinkle.delay(sprinkler_id, duration)
    print("sprinkling")
    return JsonResponse({'status': 'OK', 'result': result.get(timeout=2)})