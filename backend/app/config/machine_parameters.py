"""
File contains machine names and parameters.
"""

GLOBAL_PARAMETERS = {
    'DrillingSpeed': {'range': (200, 6000), 'unit': 'rpm'},
    'Torque': {'range': (2, 40), 'unit': 'Nm'},
    'BeltSpeed': {'range': (0, 100), 'unit': '%'},
    'Temperature': {'range': (10, 2000), 'unit': '°C'},
}

# MACHINE_NAMES = [
#     'DrillMachine', 'SolderingMachine', 'WeldingMachine'
# ]

MACHINE_NAMES = [
    'DrillingMachine'
]
