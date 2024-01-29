import paho.mqtt.client as mqtt
from django.conf import settings
import time
import threading

from REST import models


class MQTT_client:

    def __init__(self, topic):
        self.client_id = settings.MQTT_CLIENT_ID
        self.broker_ip = settings.MQTT_BROKER_HOST
        self.broker_port = settings.MQTT_BROKER_PORT
        self.qos = settings.MQTT_QOS
        self.topic = topic
        self.keep_alive = settings.MQTT_BROKER_KEEPALIVE
        self.client = mqtt.Client(client_id=self.client_id)
        self.client.username_pw_set(username=settings.MQTT_USERNAME, password=settings.MQTT_PASSWORD)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc==0:
            print(f'MQTT: client {self.client_id} connected succesfully at {self.broker_ip}:{self.broker_port}')
        self.client.subscribe(self.topic, qos=self.qos)
        #self.client.will_set('bug', payload='offline', qos=self.qos, retain=True)

    def on_message(self, client, userdata, msg):
        print(f'Client: {self.client_id}. Received message on topic: {msg.topic} with payload: {msg.payload}')
        id = msg.topic.split('/')[1]
        try:
            msg = msg.payload.decode('utf-8')
            igrometro = models.Igrometro.objects.get(id=id)
            val = int(msg)
            #voglio metterci la data nel formato solito nel primo campo di ogni misurazione
            misurazione = [time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), val]
            igrometro.ultima_misurazione = misurazione
            igrometro.misurazioni.append(misurazione)
            igrometro.save()
        except Exception as e:
            print(e)
            print('Errore nella ricezione del messaggio')


    def on_publish(self, client, userdata, mid):
        print("mid: "+str(mid))

    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        pass

    def on_disconnect(self, client, userdata, rc, properties=None):
        print("Disconnected with result code "+str(rc))

    def publish(self, message):
        self.client.publish(self.topic, message, qos=self.qos, retain=False)

    def disconnect(self):
        self.client.disconnect()

    def stop(self):
        self.client.loop_stop()

    def start(self):
        self.client.connect(self.broker_ip, self.broker_port, self.keep_alive)
        self.client.loop_start()
        