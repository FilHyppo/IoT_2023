import os

from celery import Celery
from celery.beat import crontab
from mqtt_integration.tasks import periodic_task

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproject.settings')

app = Celery('djangoproject')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'my-periodic-task': {
        'task': 'mqtt_integration.tasks.periodic_task',
        'schedule': crontab(),  # Esegui ogni minuto
    },
    # Aggiungi altri task periodici se necessario
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')