"""
Module for managing MQTT-specific environment configuration.
"""

import os
from dotenv import load_dotenv

load_dotenv("backend/app/config/.env")

MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt-broker")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
