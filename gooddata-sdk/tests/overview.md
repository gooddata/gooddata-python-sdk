# Testing overview & how-to

Tests included herein consist of typical unit tests and then component tests whose mocks are obtained using
[vcrpy](https://pypi.org/project/vcrpy/). Furthermore, some of the unit tests use the [pytest-snapshot](https://pypi.org/project/pytest-snapshot/)
to simplify assertions in tests that verify different conversion logic.

## Unit tests with snapshots

Check out the documentation of [pytest-snapshot](https://pypi.org/project/pytest-snapshot/) to learn more and then look at
some of the test for [compute_model](./compute_model) or [visualization](./visualization) to compute model conversions.

There are three important things to remember:

1.  Always name snapshot files so that they contain `.snapshot.` as part of the file name

    All these files will be excluded from pre-commit hooks and so there is no chance something will alter them and
    then render snapshot test failing

2.  When writing new tests or updating existing snapshots, use the `pytest --snapshot-update` command

    This will run the tests and create snapshot files.

3.  Always verify snapshots / diffs in snapshots to prevent false positive tests

    In the end snapshot tests are the same as unit tests except that computer writes the expected 'side' of the
    assertion.

### Type conversion tests

There are a bunch of tests in [compute_model](./compute_model) and [visualization](./visualization) whose purpose is to verify
that conversion from internal models to the API models (stored in gooddata-api-client) work
as intended.

I was unable (so far) to convert the API model to the actual format that is used when sending requests to the server. The
snapshots verify the 'intermediate' form obtained by calling `to_dict()` on the generated model classes. This operation
already does all the validations of the request data - so the tests verify that the necessary logic is correct. However, you
will find that the data in snapshots does not match the conventions of the API.

## Component tests with vcrpy

The vcrpy simplifies mocking HTTP endpoints. The component tests use the AIO image environment and the demo
workspace. The connection details are stored in [gd_test_config.yaml](gd_test_config.yaml). Tests accept command
line parameter `--gd-test-config` to pass custom test configuration.

Additionally, make sure that every time you use vcrpy, you configure the tool:
- to not store the 'Authorization' token and 'user-agent' in the captured data
- to compare also by request body

```python3
from pathlib import Path

import vcr

from tests import VCR_MATCH_ON

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"

gd_vcr = vcr.VCR(filter_headers=["authorization", "user-agent"], serializer="json", match_on=VCR_MATCH_ON)

@gd_vcr.use_cassette(str(_fixtures_dir / 'my_fixture.json'))
def test_something():
    pass
```

**NOTE**: you do not have to set token value in config file unless you are going to create new recordings.
