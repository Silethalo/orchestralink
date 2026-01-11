"""
File contains data logic.
"""

import random
from app.config.machine_parameters import MACHINE_NAMES
from app.services.parameter_randomizer import get_random_parameters

def get_machine_name():
    """
    Return a randomly selected machine name from the list.
    """
    machine_name = random.choice(MACHINE_NAMES)
    return machine_name

MACHINE_PARAMETERS = get_random_parameters()
MACHINE_NAME = get_machine_name()

TOPICS = {param: details["unit"] for param, details in MACHINE_PARAMETERS.items()}
