# Testing overview & how-to

Tests included herein consist of typical unit tests and then component tests whose mocks are obtained using
[vcrpy](https://pypi.org/project/vcrpy/). Furthermore, some of the unit tests use the [pytest-snapshot](https://pypi.org/project/pytest-snapshot/)
to simplify assertions in tests that verify different conversion logic.

## Unit tests with snapshots

Check out the documentation of [pytest-snapshot](https://pypi.org/project/pytest-snapshot/) to learn more and then look at
some of the test for [compute_model](./compute_model) or [insight](./insight) to compute model conversions.

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

There are a bunch of tests in [compute_model](./compute_model) and [insight](./insight) whose purpose is to verify
that conversion from internal models to the API models (stored in gooddata-afm-client or gooddata-metadata-client) work
as intended.

I was unable (so far) to convert the API model to the actual format that is used when sending requests to the server. The
snapshots verify the 'intermediate' form obtained by calling `to_dict()` on the generated model classes. This operation
already does all the validations of the request data - so the tests verify that the necessary logic is correct. However, you
will find that the data in snapshots does not match the conventions of the API.

## Component tests with vcrpy

The vcrpy simplifies mocking HTTP endpoints. The component tests use the insurance-dev environment and the insurance-demo
workspace. The connection details are stored in [__init__.py](__init__.py) with the exception of the authentication token.

You can specify token in the `.env.test` file located either in the gooddata-sdk directory or in the repository root. The
file is set to be ignored by git.

Additionally, make sure that every time you use vcrpy, you configure the tool to not store the 'Authorization' token
in the captured data:

```python3
gd_vcr = vcr.VCR(filter_headers=['authorization'], serializer='json')
import vcr

@gd_vcr.use_cassette(os.path.join(_fixtures_dir, 'my_fixture.json'))
def test_something():
    pass
```

**NOTE**: you do not have to set any token in `.env.test` unless you are going to create new recordings.
