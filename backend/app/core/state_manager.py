"""
File contains data storage logic.
"""

import threading

DATA_STORAGE = {}
DATA_LOCK = threading.Lock()

def initialize_data_storage(machine_name, machine_parameters):
    """Initialize in-memory data storage."""
    with DATA_LOCK:
        DATA_STORAGE.clear()
        DATA_STORAGE[machine_name] = {
            param_name: {"value": None, "unit": param_info["unit"]}
            for param_name, param_info in machine_parameters.items()
        }

def get_data_storage():
    """Retrieve stored data."""
    return DATA_STORAGE
