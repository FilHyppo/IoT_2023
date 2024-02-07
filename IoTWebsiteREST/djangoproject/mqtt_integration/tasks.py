from celery import Celery, shared_task
import time
from django.conf import settings

app = Celery('mqtt_integration.tasks')

# Configura la connessione al broker (es. Redis)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carica i task di Django
app.autodiscover_tasks()

@app.task(ignore_result=True)
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

@app.task
def add(x, y):
    print("Add task executed")
    return x + y

@app.task
def sprinkle(sprinkler_id, duration):
    print("sprinklig, id:" + str(sprinkler_id) + '  duration: ' + str(duration))
    return duration

@app.task(ignore_result=True)
def test_modelli(nome):
    from REST import models
    igrometro = models.Igrometro.objects.get(pk=1)
    igrometro.nome = nome
    igrometro.save()
    return 0