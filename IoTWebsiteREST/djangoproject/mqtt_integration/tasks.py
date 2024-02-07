from celery import Celery, shared_task
import time
from django.conf import settings


@shared_task
def periodic_task(param=None):
    from .MQTT_client import MQTT_client
    from REST import models
    print(param)
    #client = MQTT_client(settings.MQTT_TOPIC1)
    #client.start()
    time.sleep(3)
    #client.disconnect()
    print('Periodic task executed')
    return 0

@shared_task
def add(x, y):
    print("Add task executed")
    return x + y

@shared_task
def test_modelli(nome):
    from REST import models
    igrometro = models.Igrometro.objects.get(pk=1)
    igrometro.nome = nome
    igrometro.save()
    return 0