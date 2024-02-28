from fastapi import FastAPI, HTTPException
import threading
import paho.mqtt.client as mqtt
import json

app = FastAPI()
mqtt_client = mqtt.Client()

received_messages = []

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("your/topic")  # Replace "your/topic" with your actual topic

def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    message = json.loads(msg.payload.decode())  # Decode message from JSON
    received_messages.append(message)  # Add the message to the list

# Set the callback functions
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to the MQTT broker
def start_mqtt_client():
    mqtt_client.username_pw_set("", "your_password")  # Add this before mqtt_client.connect(...)
    mqtt_client.connect("mqtt5", 1883, 60)  # Adjust if necessary for your setup
    mqtt_client.loop_start()  # Start the loop in a separate thread

@app.on_event("startup")
async def startup_event():
    threading.Thread(target=start_mqtt_client).start()

@app.get("/latest-message")
def get_latest_message():
    if received_messages:
        return received_messages[-1]  # Return the last message received
    else:
        raise HTTPException(status_code=404, detail="No messages received yet")
