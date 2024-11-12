# (C) 2024 GoodData Corporation
import pytest
from jsonschema.exceptions import ValidationError


@pytest.mark.parametrize(
    "value",
    [
        {
            "dateFilter": {
                "relativeDateFilter": {
                    "from": -1,
                    "to": 0,
                    "granularity": "DAY",
                    "dataset": {"id": "dataset1", "type": "dataset"},
                }
            }
        },
        {
            "dateFilter": {
                "absoluteDateFilter": {
                    "from": "2021-01-01",
                    "to": "2021-12-31",
                    "dataset": {"id": "dataset1", "type": "dataset"},
                }
            }
        },
    ],
)
def test_valid_depends_on_date_filter_schema(value, get_validator):
    validator = get_validator("execution-context/label-elements/depends-on-date-filter.json")
    validator.validate(value)


@pytest.mark.parametrize(
    "value",
    [
        {"dateFilter": {"relativeDateFilter": {"from": -1, "to": 0, "granularity": "DAY"}}},  # missing dataset
        {"dateFilter": {"absoluteDateFilter": {"from": "2021-01-01", "to": "2021-12-31"}}},  # missing dataset
        {
            "dateFilter": {
                "relativeDateFilter": {
                    "from": "-1",  # wrong value type
                    "to": "0",
                    "granularity": "DAY",
                    "dataset": {"id": "dataset1", "type": "dataset"},
                }
            }
        },
    ],
)
def test_invalid_depends_on_date_filter_schema(value, get_validator):
    validator = get_validator("execution-context/label-elements/depends-on-date-filter.json")
    with pytest.raises(ValidationError):
        validator.validate(value)
