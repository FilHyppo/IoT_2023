from django.conf import settings
from .MQTT_client import MQTT_client
import time

def send_MQTT_message(topic, message):
    client = MQTT_client(topic)
    client.start()
    client.publish(message)
    time.sleep(1)
    client.stop()
    client.disconnect()

def trigger_Irrigatore(id_irrigatore):
    message = 'ON'
    send_MQTT_message(settings.MQTT_TOPIC1 + f'/{id_irrigatore}', message)