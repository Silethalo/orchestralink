"""
File contains machine logic.
"""

import threading
import time
import logging

from app.core.state_manager import initialize_data_storage, get_data_storage
from app.core.broker import setup_mqtt_client
from app.config.database import Database
from app.models.models import Base
from app.services.mqtt_manager import handle_mqtt_message, publish_data
from app.services.data_manager import MACHINE_NAME, MACHINE_PARAMETERS, TOPICS

logger = logging.getLogger(__name__)

def setup_database():
    """Ensure that all tables are created by SQLAlchemy's metadata."""
    try:
        engine = Database.get_engine()
        Base.metadata.create_all(bind=engine)
        logger.info("All database tables created successfully.")
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        raise


def setup_mqtt():
    """Configure and return an MQTT client."""
    try:
        client = setup_mqtt_client(MACHINE_NAME, handle_mqtt_message, TOPICS)
        return client
    except ConnectionError as e:
        logger.error(f"Failed to connect MQTT client: {e}")
        raise

def run_machine():
    setup_database()
    initialize_data_storage(MACHINE_NAME, MACHINE_PARAMETERS)

    client = setup_mqtt()

    publish_thread = threading.Thread(
        target=publish_data,
        args=(MACHINE_NAME, MACHINE_PARAMETERS, client),
        daemon=True
    )
    publish_thread.start()

    try:
        while True:
            time.sleep(15)
    except KeyboardInterrupt:
        logger.info("Machine operations interrupted by user.")
    finally:
        logger.info("Shutting down machine...")
        if client:
            client.loop_stop()
            client.disconnect()
        get_data_storage().clear()
        logger.info("Data storage cleared.")
