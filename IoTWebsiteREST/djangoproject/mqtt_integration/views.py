from django.http import JsonResponse
from django.shortcuts import render
from . import tasks
from django.conf import settings
from .MQTT_client import MQTT_client

def celery_test(request):
    tasks.periodic_task.delay()
    return JsonResponse({'status': 'ok'})