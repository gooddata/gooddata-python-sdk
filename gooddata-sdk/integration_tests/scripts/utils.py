# (C) 2024 GoodData Corporation
import json


def load_json(file_path):
    """Load a JSON file and return its contents."""
    with open(file_path) as file:  # Removed the "r" as it's the default mode
        return json.load(file)


def normalize_metrics(metrics, exclude_keys=None):
    """
    Normalize keys in the metrics list to camelCase, excluding specified keys.

    :param metrics: List of dictionaries with metric data.
    :param exclude_keys: List of keys to exclude from normalization.
    :return: List of normalized metric dictionaries.
    """
    if exclude_keys is None:
        exclude_keys = []

    def snake_to_camel(snake_str):
        components = snake_str.split("_")
        return components[0] + "".join(x.title() for x in components[1:])

    return [
        {snake_to_camel(key): value for key, value in metric.items() if key not in exclude_keys}
        for metric in metrics
        if isinstance(metric, dict)
    ]
