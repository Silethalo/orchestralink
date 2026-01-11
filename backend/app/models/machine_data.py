"""
File contains logic for inserting machine data into the database.
Refactored to use Single Table Design and SQLAlchemy ORM.
"""

import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.models import MachineData
from app.config.database import Database

logger = logging.getLogger(__name__)

def insert_machine_data(conn, machine_name, topic, value, unit, timestamp=None, retries=3, delay=1):
    """
    Insert data into the unified machine_data table using the ORM.
    
    This function replaces the previous raw SQL implementation to ensure 
    consistency with the API's read models.

    :param conn: A SQLAlchemy Session object or None. If None/Invalid, a new session is created.
    :param machine_name: Name of the machine (e.g., 'DrillingMachine').
    :param topic: MQTT topic associated with the data.
    :param value: Value of the machine parameter.
    :param unit: Unit of the parameter.
    :param timestamp: Timestamp for when the data was generated.
    """
    if not timestamp:
        timestamp = datetime.utcnow()

    session = None
    should_close = False

    try:
        # Determine if we were passed a valid ORM Session, otherwise create a temp one
        if isinstance(conn, Session):
            session = conn
        else:
            # If a raw connection or None was passed, we instantiate a proper ORM session
            # to ensure compatibility with the MachineData model.
            session = Database.get_session()
            should_close = True

        logger.debug(f"Inserting data for '{machine_name}' on topic '{topic}'")

        # FIX: Use the ORM 'create_entry' method to target the 'machine_data' table
        # instead of creating dynamic tables.
        MachineData.create_entry(
            session=session, 
            machine_name=machine_name, 
            topic=topic, 
            value=value, 
            unit=unit
        )
        
        logger.info(f"Successfully saved data for '{machine_name}'")

    except Exception as e:
        logger.error(f"[DB ERROR] Failed to insert data for topic '{topic}': {e}")
        if session:
            session.rollback()
    finally:
        # cleanup if we created a temporary session
        if should_close and session:
            session.close()
