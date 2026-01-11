"""
Database configuration related file.
"""

import os
import time
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError, OperationalError

logger = logging.getLogger(__name__)

Base = declarative_base()

class Database:
    _engine = None
    _Session = None

    @classmethod
    def initialize(cls, db_url=None, retries=5, retry_delay=5):
        """Initialize the database engine and session factory with retries."""
        if cls._engine is not None:
            logger.warning("Database engine is already initialized.")
            return

        db_url = db_url or os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@database:5432/postgres")
        logger.info(f"Using database URL: {db_url}")

        attempt = 0
        while attempt < retries:
            try:
                logger.info(f"Initializing database engine (attempt {attempt + 1}/{retries})...")
                cls._engine = create_engine(db_url, echo=True)
                cls._Session = sessionmaker(bind=cls._engine)
                cls._engine.connect()
                logger.info("Database engine initialized successfully.")
                return
            except (SQLAlchemyError, OperationalError) as e:
                attempt += 1
                logger.error(f"Failed to connect to the database: {e}")
                if attempt < retries:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    logger.error("Exceeded maximum retry attempts. Initialization failed.")
                    raise

    @classmethod
    def get_engine(cls):
        """Retrieve the SQLAlchemy engine."""
        if cls._engine is None:
            raise RuntimeError("Database engine is not initialized.")
        return cls._engine

    @classmethod
    def get_session(cls):
        """Retrieve a new SQLAlchemy session."""
        if cls._Session is None:
            raise RuntimeError("Database session factory is not initialized.")
        
        try:
            logger.info("Creating a new database session...")
            # pylint: disable=not-callable
            return cls._Session()
        except SQLAlchemyError as e:
            logger.error(f"Failed to create a database session: {e}")
            raise

    @classmethod
    def get_connection(cls):
        """Retrieve a raw database connection."""
        if cls._engine is None:
            raise RuntimeError("Database engine is not initialized.")
        
        try:
            logger.info("Acquiring a raw database connection...")
            return cls._engine.connect()
        except SQLAlchemyError as e:
            logger.error(f"Failed to acquire a database connection: {e}")
            raise

    @classmethod
    def release_connection(cls, conn):
        """Close the given connection."""
        try:
            conn.close()
            logger.info("Database connection closed.")
        except SQLAlchemyError as e:
            logger.error(f"Failed to close the database connection: {e}")
            raise
