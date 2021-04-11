import paho.mqtt.client as mqtt
from analyze_web_command import analyze_web_json

class MQTT():

    def __init__(self, client=None, vehicle=None):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set('aiotlab', password='aiotlab208')
        self.client.connect("35.201.182.150", 1883, 60)
        self.client.loop_start()
        
        self.vehicle = vehicle

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.client.subscribe("id_name/cmd")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        # print(msg.topic+" "+str(msg.payload))
        analyze_web_json(self.vehicle, msg.payload)

    def publish(self, topic, payload=None):
        self.client.publish(topic, payload)
    