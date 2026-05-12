# (C) 2025 GoodData Corporation
from pathlib import Path

from gooddata_sdk.sdk import GoodDataSdk
from tests_support.vcrpy_utils import get_vcr

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"


@gd_vcr.use_cassette(str(_fixtures_dir / "ai_search_error_field.yaml"))
def test_search_ai_error_field(test_config):
    """Test that SearchResult properly exposes the ErrorInfo error field.

    The error field is populated when search could not run (e.g. metadata sync
    is in progress). It is absent on success. This test verifies that when the
    API returns an error the SDK surfaces it correctly via result.error.
    """
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    test_workspace_id = test_config["workspace_test"]

    result = sdk.compute.search_ai(test_workspace_id, "What is the total revenue?")
    # On success the error field is absent; on failure it carries structured info.
    if result.error is not None:
        assert isinstance(result.error.reason, str), "error.reason must be a string"
        assert isinstance(result.error.status_code, int), "error.status_code must be an int"
    else:
        assert result.results is not None, "On success, results must be present"
