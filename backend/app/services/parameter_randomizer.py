"""
File containing parameter logic.
"""

import random

from app.config.machine_parameters import GLOBAL_PARAMETERS

state = {}

def clear_old_state():
    """Clear the state dictionary."""
    global state # pylint: disable=W0602
    state.clear()

def get_random_parameters(max_params=4, data_sample=5, data_margin=0.03, previous_values=None):
    """Function picking and generating smooth parameters for machines."""
    param_names = list(GLOBAL_PARAMETERS.keys())
    selected_params = random.sample(param_names, min(max_params, len(param_names)))
    print(f"Selected parameters: {selected_params}")

    smooth_params = {}
    clear_old_state()

    for param in selected_params:
        print(f"Processing parameter: {param}")
        param_info = GLOBAL_PARAMETERS[param]
        min_val, max_val = param_info["range"]

        if previous_values and param in previous_values:
            base_value = previous_values[param]['value']
            value = base_value + base_value * random.uniform(-data_margin, data_margin)
        else:
            value = random.uniform(min_val, max_val)

        values = [value]

        for _ in range(data_sample - 1):
            variation = value * random.uniform(-data_margin, data_margin)
            variation_value = value + variation
            values.append(variation_value)
            print(f"Generated variation: {variation_value:.2f}")

        average_value = round(sum(values) / len(values), 2)
        print(f"Average value for {param}: {average_value}")

        unit = param_info.get('unit', '')
        smooth_params[param] = {
            'value': average_value,
            'unit': unit,
            'range': (min_val, max_val)
        }

    print("Final smoothed parameters:")
    print(smooth_params)
    return smooth_params
