# GoodData.CN Python Foundations

This repository contains Python packages useful for integration with [GoodData Cloud Native](https://www.gooddata.com/developers/cloud-native/).

## Available packages

### API Clients

API clients are generated directly from GoodData.CN OpenAPI specifications and allow you to call any API from
Python. Learn more about the clients in their [dedicated readme](./clients_README.md).

### Python SDK

Python SDK is a layer of convenience and use-case oriented APIs that allows simple interaction with GoodData.CN.

Check out the [gooddata-sdk](./gooddata-sdk) documentation to learn more.

### GoodData.CN Foreign Data Wrapper for PostgreSQL

Foreign Data Wrapper (FDW) presents a way to map GoodData.CN semantic layer and/or insights stored in your GoodData.CN
into PostgreSQL as foreign tables that you can then query using SQL.

Check out the [gooddata-fdw package](./gooddata-fdw) documentation to learn more and get started.

### GoodData to pandas adapters

The [gooddata-pandas](./gooddata-pandas) is a thin layer that utilizes Python SDK and allows you to conveniently
create pandas series and data frames.

## Requirements

-  [GoodData.CN](https://www.gooddata.com/developers/cloud-native/) installation; either running on your cloud
   infrastructure or the free Community Edition running on your workstation

-  Python 3.7 or newer

-  The GoodData.CN Foreign Data Wrapper is tested with the latest version of multicorn (1.4.0) and PostgreSQL 12

## Contributing

### Getting Started

1. Ensure you have at minimum Python 3.9 installed; Python 3.8 and 3.7 are optional for multi-environment tests

    This repo uses [tox](https://tox.readthedocs.io/en/latest/) and by default will try to run tests against all
    supported versions. You can run `tox -e py39` to limit tests to just one environment.

2. Clone and setup environment:

    ```bash
    git clone git@github.com:gooddata/gooddata-python-sdk.git
    cd gooddata-python-sdk
    make dev
    ```

    The `make dev` command will create a new Python 3.9 virtual environment in the `.venv` directory, install all
    third party dependencies into it and setup git hooks.

    Additionally, if you use [direnv](https://direnv.net/) you can run `direnv allow .envrc` to enable automatic
    activation of the virtual environment that was previously created in `.venv`.

    If `direnv` is not your cup of tea, you may want to adopt the PYTHONPATH exports that are done as part of the
    script so that you can run custom Python code using the packages container herein without installing them.

    To make sure you have successfully set up your environment run `make test` in virtualenv in the root of git repo.
    Please note, that `make test` executes tests against all the supported python versions. If you need to specify only
    subset of them, see section [Run tests](#Run tests)

### Coding Conventions

This project uses [flake8](https://flake8.pycqa.org/en/latest/) to ensure basic code sanity and [black](https://github.com/psf/black)
for no-nonsense, consistent formatting.

Both `flake8` and auto-fixing `black` are part of the pre-commit hook that is automatically set up during `make dev`.

You can also run the lint and formatter manually:

-  To run flake8 run: `make lint`
-  To reformat code black run: `make format-fix`

**NOTE** If the pre-commit hook finds and auto-corrects some formatting errors, it will not auto-stage
the updated files and will fail the commit operation. You have to re-drive the commit. This is a well-known and
unlikely-to-change behavior of the [pre-commit](https://github.com/pre-commit/pre-commit/issues/806) package that this repository uses to manage hooks.

### Run tests
Tests use [tox](https://tox.wiki/en/latest/index.html) and [pytest](https://docs.pytest.org/en/6.2.x/contents.html)
libraries. Each project has its own `tox.ini`.
NOTE: Tests are not executed for OpenAPI client projects.

Here are the options how to run the tests:
- run tests for one sub-project - drill down to sub-project's directory
  - use `make test` to trigger tests
  ```bash
  cd gooddata-sdk
  make test
  ```
  - or execute `tox` command with arguments of your choice
  ```bash
  cd gooddata-sdk
  tox -e py39
  ```
- run tests for all non-client projects using `make test` in project root directory

Tests triggered by make can be controlled via these environment variables:
- `RECREATE_ENVS` - set environment variable `RECREATE_ENVS` to 1 and make will add `--recreate` flag, `--recreate`
  flag is not used otherwise
  ```bash
  RECREATE_ENVS=1 make test
  ```
- `TEST_ENVS` - define tox test environments (targets) as comma-separated list, by default all tox default targets are
  executed
  ```bash
  TEST_ENVS=py39,py37 make test
  ```
- `ADD_ARGS` - send additional arguments to pytest tool, useful for pin-pointing just part of tests
  ```bash
  ADD_ARGS="-k http_headers" make test
  ```

### Run continuous integration tests
Tests in pull request (PR) are executed using docker. The following is done to make tests environment as close
to reproducible as possible:
- each supported python version has defined python base docker image
- tox version installed to docker is frozen to specific version
- all test dependencies specified in test-requirements.txt should be limited to some version range

Above rules give a chance to execute tests on localhost in the same or very similar environment as used in PR.
Orchestration is driven by `make test-ci`. Target `test-ci` supports the same features as `make test`, see
[Run tests](#Run tests) for details.

NOTE: docker tox tests and localhost tox tests are using the same .tox directory. Virtual environments for both test
types are most likely incompatible due to different base python version. tox is able to recognize it and recreate
venv automatically. So when docker tox tests are executed after localhost tests or vice-versa envs are recreated.

#### Examples
- run all tests for all supported python environments
  ```bash
  make test-ci
  ```
- run all tests for all supported python environments and for one project
  ```bash
  cd gooddata-sdk
  make test-ci
  ```
- run all tests containing `http_headers` in name for py39 and py38 for all projects
  ```bash
  TEST_ENVS=py39,py38 ADD_ARGS="-k http_headers" make test-ci
  ```
