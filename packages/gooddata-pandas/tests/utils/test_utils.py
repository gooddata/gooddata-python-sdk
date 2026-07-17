# (C) 2025 GoodData Corporation
import types
from pathlib import Path

import pandas
from gooddata_pandas.utils import _typed_attribute_values, get_catalog_attributes_for_extract
from gooddata_sdk import (
    Attribute,
    GoodDataSdk,
)
from tests_support.vcrpy_utils import get_vcr

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"


@gd_vcr.use_cassette(str(_fixtures_dir / "test_get_catalog_attributes_for_extract.yaml"))
def test_get_catalog_attributes_for_extract(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    workspace_id = "demo"
    attributes = [Attribute(local_id="0", label="campaign_name"), Attribute(local_id="1", label="region")]
    catalog_attributes = get_catalog_attributes_for_extract(sdk, workspace_id, attributes, character_limit=28)
    assert len(catalog_attributes) == 2
    assert [ca.id for ca in catalog_attributes] == ["campaign_name", "region"]


# ---------------------------------------------------------------------------
# _typed_attribute_values — JSON-path attribute value conversion
#
# The JSON path converts a whole attribute column in one vectorized pandas call
# instead of once per value. These pin the resulting values (the behaviour the
# per-value path produced before the change); nothing else covers this function -
# the JSON exec_def cassettes only contain text attributes (granularity: null).
# ---------------------------------------------------------------------------


def _date_catalog_attribute(granularity: str) -> types.SimpleNamespace:
    """Minimal stand-in exposing the two fields _typed_attribute_values reads."""
    return types.SimpleNamespace(
        dataset=types.SimpleNamespace(dataset_type="DATE"),
        granularity=granularity,
    )


def test_typed_attribute_values_batches_dates_to_timestamps():
    """DAY/MONTH/YEAR granularities convert the whole column to pandas.Timestamp."""
    assert _typed_attribute_values(_date_catalog_attribute("DAY"), ["2023-01-15", "2024-06-30"]) == [
        pandas.Timestamp("2023-01-15"),
        pandas.Timestamp("2024-06-30"),
    ]
    # partial dates (year-only / year-month) still parse to the period start
    assert _typed_attribute_values(_date_catalog_attribute("YEAR"), ["2023", "2024"]) == [
        pandas.Timestamp("2023-01-01"),
        pandas.Timestamp("2024-01-01"),
    ]
    assert _typed_attribute_values(_date_catalog_attribute("MONTH"), ["2023-01", "2023-03"]) == [
        pandas.Timestamp("2023-01-01"),
        pandas.Timestamp("2023-03-01"),
    ]


def test_typed_attribute_values_week_and_quarter_stay_strings():
    """WEEK/QUARTER use a string converter (no external pandas fn) — values unchanged."""
    assert _typed_attribute_values(_date_catalog_attribute("WEEK"), ["2025-1", "2025-49"]) == ["2025-1", "2025-49"]
    assert _typed_attribute_values(_date_catalog_attribute("QUARTER"), ["2025-1", "2025-4"]) == ["2025-1", "2025-4"]


def test_typed_attribute_values_empty_list():
    """Empty column returns an empty list without error."""
    assert _typed_attribute_values(_date_catalog_attribute("DAY"), []) == []
