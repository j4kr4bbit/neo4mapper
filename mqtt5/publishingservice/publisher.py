

import paho.mqtt.client as mqtt
import json
import time

# MQTT settings
MQTT_HOST = 'mqtt5'  # Use the Docker service name if in the same network, else the IP
MQTT_PORT = 1883
MQTT_TOPIC = 'your/topic'

def publish_message():
    client = mqtt.Client()

    client.connect(MQTT_HOST, MQTT_PORT, 60)
    while True:
        message = {'key': 'value'}  # Your JSON message
        client.publish(MQTT_TOPIC, json.dumps(message))
        time.sleep(1)  # Delay for demonstration; adjust as necessary

if __name__ == '__main__':
    publish_message()
