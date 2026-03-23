# (C) 2024 GoodData Corporation
import pytest
from jsonschema.exceptions import ValidationError


@pytest.mark.parametrize(
    "value",
    [
        {
            "filterType": "positiveAttributeFilter",
            "labelIdentifier": "attribute1",
            "values": ["id1", "id2", "id3", None],
        },
        {
            "filterType": "negativeAttributeFilter",
            "labelIdentifier": "attribute1",
            "values": ["id1", "id2", "id3", None],
        },
        {
            "filterType": "matchAttributeFilter",
            "labelIdentifier": "attribute1",
            "literal": "foo",
            "matchType": "CONTAINS",
        },
        {
            "filterType": "relativeDateFilter",
            "from": -5,
            "to": 0,
            "granularity": "DAY",
            "datasetIdentifier": "dataset1",
        },
        {"filterType": "absoluteDateFilter", "from": "2021-01-01", "to": "2021-12-31", "datasetIdentifier": "dataset1"},
    ],
)
def test_valid_filter_schema(value, get_validator):
    validator = get_validator("execution-context/filter.json")
    validator.validate(value)


@pytest.mark.parametrize(
    "value",
    [
        {"labelIdentifier": "attribute1", "values": ["id1", "id2", "id3", None]},  # missing filterType
        # invalid filterType
        {"filterType": "invalid", "labelIdentifier": "attribute1", "values": ["id1", "id2", "id3", None]},
        {"filterType": "positiveAttributeFilter", "labelIdentifier": "attribute1"},  # missing values
        {"filterType": "positiveAttributeFilter", "labelIdentifier": "attribute1", "values": [5]},  # invalid values
        {"filterType": "negativeAttributeFilter", "labelIdentifier": "attribute1"},  # missing values
        {"filterType": "relativeDateFilter", "from": -5, "to": 0, "granularity": "DAY"},  # missing datasetIdentifier
        {"filterType": "absoluteDateFilter", "from": "2021-01-01", "to": "2021-12-31"},  # missing datasetIdentifier
        # missing match type
        {"filterType": "matchAttributeFilter", "labelIdentifier": "attribute1", "literal": "foo"},
        # invalid match type
        {
            "filterType": "matchAttributeFilter",
            "labelIdentifier": "attribute1",
            "literal": "foo",
            "matchType": "INVALID",
        },
    ],
)
def test_invalid_filter_schema(value, get_validator):
    validator = get_validator("execution-context/filter.json")
    with pytest.raises(ValidationError):
        validator.validate(value)
