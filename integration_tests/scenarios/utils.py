# (C) 2024 GoodData Corporation
import difflib
import json


def print_diff(actual, expected, context):
    actual_str = json.dumps(actual, indent=4, sort_keys=True)
    expected_str = json.dumps(expected, indent=4, sort_keys=True)
    diff = difflib.unified_diff(
        expected_str.splitlines(), actual_str.splitlines(), fromfile="expected", tofile="actual", lineterm=""
    )
    print(f"\n{context} mismatch:")
    for line in diff:
        print(line)


def compare_and_print_diff(actual, expected, context):
    if actual != expected:
        print_diff(actual, expected, context)
    assert actual == expected, f"{context} mismatch"


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
