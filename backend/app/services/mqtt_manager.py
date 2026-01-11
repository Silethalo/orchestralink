"""
File contains MQTT logic.
"""

import random
import time
import logging
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from paho.mqtt.client import Client, MQTT_ERR_SUCCESS

from app.config.database import Database
from app.models.models import MachineData
from app.services.data_manager import TOPICS, MACHINE_NAME

logger = logging.getLogger(__name__)

def handle_mqtt_message(client, userdata, msg):
    """Handle incoming MQTT messages and store them in the database."""
    topic = msg.topic
    try:
        # Decode message
        message = float(msg.payload.decode())
    except ValueError:
        message = msg.payload.decode()

    unit = TOPICS.get(topic, "")
    timestamp = datetime.utcnow()

    logger.info(f"Received data for topic '{topic}': {message} {unit}")

    try:
        with Database.get_session() as session:
            # Insert the new entry
            entry = MachineData.create_entry(session, MACHINE_NAME, topic, message, unit)
            logger.info(f"Data inserted for topic '{topic}'. Entry ID: {entry.id} Timestamp: {entry.timestamp}")
    except SQLAlchemyError as db_error:
        logger.error(f"Database error while inserting data for topic '{topic}': {db_error}")
        session.rollback()
    except Exception as e:
        logger.error(f"Unexpected error while handling MQTT message for topic '{topic}': {e}")

def publish_data(machine_name, machine_parameters, client: Client):
    """Continuously publish random data to MQTT topics and log it in the database."""
    while True:
        for topic, param_info in machine_parameters.items():
            value = random.uniform(*param_info["range"])
            unit = param_info.get("unit", "")
            timestamp = datetime.utcnow()

            try:
                # Publish data to MQTT topic
                publish_result = client.publish(topic, value)
                if publish_result.rc != MQTT_ERR_SUCCESS:
                    logger.error(f"Failed to publish to topic '{topic}'. MQTT error code: {publish_result.rc}")
                    continue

                logger.info(f"Published data to topic '{topic}': {value}")

                # Insert data into the database
                with Database.get_session() as session:
                    MachineData.create_entry(session, machine_name, topic, value, unit)
                    logger.info(f"Data inserted for topic '{topic}' in the database.")
            except SQLAlchemyError as db_error:
                logger.error(f"Database error while inserting data for topic '{topic}': {db_error}")
            except Exception as e:
                logger.error(f"Unexpected error during publish to topic '{topic}': {e}")

        # Sleep to simulate periodic data publishing
        time.sleep(15)

def setup_mqtt():
    """Configure and return an MQTT client with reconnection logic."""
    client = Client()

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logger.info("MQTT client connected successfully.")
        else:
            logger.error(f"MQTT client failed to connect. Return code: {rc}")

    def on_disconnect(client, userdata, rc):
        logger.warning("MQTT client disconnected. Attempting to reconnect...")
        try:
            client.reconnect()
        except Exception as e:
            logger.error(f"Reconnection failed: {e}")

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    try:
        client.connect("mqtt_broker_host", 1883, 60)  # Replace with actual broker details
    except Exception as e:
        logger.error(f"Failed to connect to the MQTT broker: {e}")
        raise

    client.loop_start()  # Start the loop in a separate thread
    return client
