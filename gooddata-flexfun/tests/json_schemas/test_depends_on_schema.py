# (C) 2024 GoodData Corporation
import pytest
from jsonschema.exceptions import ValidationError


@pytest.mark.parametrize(
    "value",
    [
        {"label": "exampleLabel", "values": ["value1", "value2", None]},
        {"label": "exampleLabel", "values": ["value1", "value2", None], "complementFilter": True},
    ],
)
def test_valid_depends_on_schema(value, get_validator):
    validator = get_validator("execution-context/label-elements/depends-on.json")
    validator.validate(value)


@pytest.mark.parametrize(
    "value",
    [
        {"label": "exampleLabel"},  # missing values
        {"values": ["value1", "value2", None]},  # missing label
        {"label": "exampleLabel", "values": [1, 2, None], "complementFilter": "True"},  # wrong value type
    ],
)
def test_invalid_depends_on_schema(value, get_validator):
    validator = get_validator("execution-context/label-elements/depends-on.json")
    with pytest.raises(ValidationError):
        validator.validate(value)
