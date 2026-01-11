# """
# File running whole infrastructure.
# """

# import logging
# import threading
# import uvicorn
# from fastapi import FastAPI
# from sqlalchemy import inspect

# from app.api.routes import router as machine_router
# from app.config.database import Database, Base
# from app.core.machine import run_machine
# from app.config.logging import setup_logging

# setup_logging()
# logger = logging.getLogger(__name__)

# app = FastAPI(title="Machine Data API")

# @app.on_event("startup")
# async def on_startup():
#     """Handle application startup."""
#     logger.info("Starting application...")

#     try:
#         DATABASE_URL = "postgresql+psycopg2://postgres:postgres@database:5432/postgres"
#         Database.initialize(DATABASE_URL)
#         logger.info("Database initialized successfully.")
#     except Exception as e:
#         logger.error(f"Failed to initialize the database: {e}")
#         raise

#     try:
#         logger.info("Creating database tables...")
#         Base.metadata.create_all(bind=Database.get_engine())

#         inspector = inspect(Database.get_engine())
#         tables = inspector.get_table_names()
#         if 'machine_data' not in tables:
#             logger.error("Table 'machine_data' was not created.")
#             raise RuntimeError("Table creation failed despite calling 'create_all()'")

#         logger.info("All database tables created successfully.")
#     except Exception as e:
#         logger.error(f"Error during table creation: {e}")
#         raise

#     try:
#         threading.Thread(target=run_machine, daemon=True).start()
#         logger.info("Machine operations started.")
#     except Exception as e:
#         logger.error(f"Failed to start machine operations: {e}")
#         raise

# @app.on_event("shutdown")
# async def on_shutdown():
#     """Handle application shutdown."""
#     try:
#         Database.get_engine().dispose()
#         logger.info("Database connections closed.")
#     except Exception as e:
#         logger.error(f"Error during shutdown: {e}")

# app.include_router(machine_router, prefix="/api", tags=["Machine Data"])

# def main():
#     """Run the FastAPI server."""
#     try:
#         logger.info("Starting FastAPI server...")
#         uvicorn.run(app, host="0.0.0.0", port=8000)
#     except Exception as e:
#         logger.error(f"Failed to start the application: {e}")

# if __name__ == "__main__":
#     main()

"""
File running whole infrastructure.
"""

import logging
import threading
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- Import CORSMiddleware
from sqlalchemy import inspect

from app.api.routes import router as machine_router
from app.config.database import Database, Base
from app.core.machine import run_machine
from app.config.logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Machine Data API")

# Configure CORS middleware
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # Add additional origins if needed (e.g., production URLs)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # Allowed origins
    allow_credentials=True,
    allow_methods=["*"],             # Allow all HTTP methods
    allow_headers=["*"],             # Allow all headers
)

@app.on_event("startup")
async def on_startup():
    """Handle application startup."""
    logger.info("Starting application...")

    try:
        DATABASE_URL = "postgresql+psycopg2://postgres:postgres@database:5432/postgres"
        Database.initialize(DATABASE_URL)
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize the database: {e}")
        raise

    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=Database.get_engine())

        inspector = inspect(Database.get_engine())
        tables = inspector.get_table_names()
        if 'machine_data' not in tables:
            logger.error("Table 'machine_data' was not created.")
            raise RuntimeError("Table creation failed despite calling 'create_all()'")

        logger.info("All database tables created successfully.")
    except Exception as e:
        logger.error(f"Error during table creation: {e}")
        raise

    try:
        threading.Thread(target=run_machine, daemon=True).start()
        logger.info("Machine operations started.")
    except Exception as e:
        logger.error(f"Failed to start machine operations: {e}")
        raise

@app.on_event("shutdown")
async def on_shutdown():
    """Handle application shutdown."""
    try:
        Database.get_engine().dispose()
        logger.info("Database connections closed.")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

# Include the router for machine data endpoints
app.include_router(machine_router, prefix="/api", tags=["Machine Data"])

def main():
    """Run the FastAPI server."""
    try:
        logger.info("Starting FastAPI server...")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except Exception as e:
        logger.error(f"Failed to start the application: {e}")

if __name__ == "__main__":
    main()
