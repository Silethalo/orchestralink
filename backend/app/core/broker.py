"""
Broker configuration.
"""

import os
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from app.services.data_manager import get_machine_name

load_dotenv("backend/app/config/.env")

machine_name = get_machine_name()

def setup_mqtt_client(client_id, on_message_callback, topics):
    """Set up and return an MQTT client configured with topics."""
    mqtt_broker = os.getenv("MQTT_BROKER", "mqtt-broker")
    mqtt_port = os.getenv("MQTT_PORT", "1883")
    client = mqtt.Client(client_id=machine_name, protocol=mqtt.MQTTv5)
    client.on_message = on_message_callback
    client.connect(mqtt_broker, int(mqtt_port))

    for topic in topics:
        client.subscribe(topic)

    return client
