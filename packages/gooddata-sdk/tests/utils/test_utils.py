# (C) 2022 GoodData Corporation
from __future__ import annotations

import json
from pathlib import Path

from gooddata_sdk.utils import camel_to_snake, change_case, snake_to_camel

_current_dir = Path(__file__).parent.absolute()


def test_dictionary_case_convertor(test_config):
    path = _current_dir / "test_dictionary.json"
    with open(path, encoding="utf8") as f:
        data = json.load(f)
    x = change_case(change_case(data, camel_to_snake), snake_to_camel)
    assert data == x


def test_snake_to_camel(test_config):
    value = "this_is_an_example_of_snake_case"
    assert snake_to_camel(value) == "thisIsAnExampleOfSnakeCase"


def test_camel_to_snake(test_config):
    value = "thisIsAnExampleOfCamelCase"
    assert camel_to_snake(value) == "this_is_an_example_of_camel_case"
