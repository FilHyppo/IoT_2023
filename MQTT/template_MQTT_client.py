import paho.mqtt.client as mqtt
import time


class MQTT_client:
    def __init__(self, client_id, topic, qos, keep_alive, broker_ip='127.0.0.1', broker_port=1883):
        self.client_id = client_id
        self.broker_ip = broker_ip
        self.broker_port = broker_port
        self.topic = topic
        self.qos = qos
        self.keep_alive = keep_alive
        self.client = mqtt.Client(client_id=self.client_id, userdata=None, protocol=mqtt.MQTTv5, transport="tcp")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        self.client.on_disconnect = self.on_disconnect

        self.client.connect(self.broker_ip, self.broker_port, self.keep_alive)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc, properties=None):
        print("Connected with result code "+str(rc))
        self.client.subscribe(self.topic, qos=self.qos)

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

    def on_publish(self, client, userdata, mid):
        print("mid: "+str(mid))

    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_disconnect(self, client, userdata, rc):
        print("Disconnected with result code "+str(rc))

    def publish(self, message):
        self.client.publish(self.topic, message, qos=self.qos, retain=False)

    def disconnect(self):
        self.client.disconnect()

if __name__ == '__main__':
    client = MQTT_client(client_id='test', topic='test', qos=2, keep_alive=60)
    client.publish('test')
    time.sleep(1000)
    client.disconnect()
