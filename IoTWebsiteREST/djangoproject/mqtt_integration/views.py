from django.http import JsonResponse
from django.shortcuts import render
from . import tasks
from djangoproject.celery import debug_task 
from django.conf import settings
from .MQTT_client import MQTT_client

def celery_test(request):
    a = int(request.GET.get('a', 0))
    b = int(request.GET.get('b', 0))
    result = tasks.add.delay(a, b)
    print("Celery test executed")
    return JsonResponse({'status': 'OK', 'result': result.get(timeout=1)})