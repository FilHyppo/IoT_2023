from celery import Celery, shared_task
import time
from django.conf import settings

from .mqtt import send_MQTT_message


@shared_task
def periodic_task(param=None):
    print(param)
    time.sleep(3)
    print('Periodic task executed')
    return 0

@shared_task()
def sprinkle(irrigatore_id, duration):
    from REST.models import Irrigatore
    irrigatore = Irrigatore.objects.get(id=irrigatore_id)
    irrigatore.irriga(duration)
    secret = irrigatore.secret
    send_MQTT_message(settings.MQTT_TOPIC_IRRIGATORE + str(secret), duration)
    return duration
