# (C) 2024 GoodData Corporation
import pytest
from jsonschema.exceptions import ValidationError


@pytest.mark.parametrize(
    "value",
    [
        {
            "attributeIdentifier": "attr1",
            "attributeTitle": "Attribute 1",
            "labelIdentifier": "label1",
            "labelTitle": "Label 1",
        },
        {
            "attributeIdentifier": "attr1",
            "attributeTitle": "Attribute 1",
            "labelIdentifier": "label1",
            "labelTitle": "Label 1",
            "dateGranularity": "DAY",
            "sorting": {"sortColumn": "column1", "sortDirection": "ASC"},
        },
    ],
)
def test_valid_attribute_schema(value, get_validator):
    validator = get_validator("execution-context/attribute.json")
    validator.validate(value)


@pytest.mark.parametrize(
    "value",
    [
        {"attributeIdentifier": "attr1"},  # missing attributeTitle
        {"attributeTitle": "Attribute 1"},  # missing attributeIdentifier
        # missing labelTitle
        {"attributeIdentifier": "attr1", "attributeTitle": "Attribute 1", "labelIdentifier": "label1"},
        # missing sortDirection
        {
            "attributeIdentifier": "attr1",
            "attributeTitle": "Attribute 1",
            "labelIdentifier": "label1",
            "labelTitle": "Label 1",
            "dateGranularity": "DAY",
            "sorting": {"sortColumn": "column1"},
        },
    ],
)
def test_invalid_attribute_schema(value, get_validator):
    validator = get_validator("execution-context/attribute.json")
    with pytest.raises(ValidationError):
        validator.validate(value)
