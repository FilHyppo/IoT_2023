from celery import Celery, shared_task
from django.conf import settings

app = Celery('djangoproject')

@app.task
def periodic_task():
    print("Periodic task executed")
    return 0
