# (C) 2024 GoodData Corporation
import pytest
from jsonschema.exceptions import ValidationError


@pytest.mark.parametrize(
    "value",
    [
        # bare minimum
        {
            "label": "label1",
        },
        # all properties
        {
            "label": "label2",
            "limit": 5,
            "offset": 2,
            "excludePrimaryLabel": False,
            "exactFilter": ["value3"],
            "patternFilter": "pattern?",
            "complementFilter": True,
            "dependsOn": [{"label": "parent1", "values": ["foo", "bar"]}],
            "validateBy": [{"id": "validator2", "type": "attribute"}],
        },
    ],
)
def test_valid_execution_request_schema(value, get_validator):
    validator = get_validator("execution-context/label-elements/execution-request.json")
    validator.validate(value)


@pytest.mark.parametrize(
    "value",
    [
        {"label": "label2", "limit": "5"},  # wrong value type
        {"label": "label2", "offset": "2"},  # wrong value type
        {"label": "label2", "excludePrimaryLabel": "False"},  # wrong value type
        {"label": "label2", "exactFilter": "value3"},  # wrong value type
        {"label": "label2", "patternFilter": 5},  # wrong value type
        {"label": "label2", "complementFilter": "True"},  # wrong value type
        {"label": "label2", "dependsOn": {"label": "parent1", "values": ["foo", "bar"]}},  # wrong value type
        {"label": "label2", "validateBy": {"id": "validator2", "type": "attribute"}},  # wrong value type
        {"label": "label2", "validateBy": {"id": "validator2", "type": "invalid"}},  # wrong validateBy type
    ],
)
def test_invalid_execution_request_schema(value, get_validator):
    validator = get_validator("execution-context/label-elements/execution-request.json")
    with pytest.raises(ValidationError):
        validator.validate(value)
