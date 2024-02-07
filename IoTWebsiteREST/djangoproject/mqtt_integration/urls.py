from . import views
from django.urls import path
from .MQTT_client import MQTT_client

urlpatterns = [
    #path('connect/', views.mqtt_connect, name='mqtt'),
    #path('disconnect/', views.mqtt_disconnect, name='mqtt_disconnect'),
    path('celery/', views.celery_test, name='celery_test'),
    path('celery/sprinkle/<int:sprinkler_id>/<int:duration>/', views.celery_sprinkle, name='celery_sprinkle'),
]

#client = MQTT_client(topic='django/+')
#client.start()
