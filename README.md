# GoodData.CN Python Foundations

This repository contains Python packages useful for integration with GoodData Cloud Native.

Code is compatible with Python 3.9 or newer.

## Available packages

### API Clients

API clients are generated directly from GoodData.CN OpenAPI specifications and allow you to call any API from
Python. Learn more about the clients in their [dedicated readme](./clients_README.md).

### Python SDK

Python SDK is a layer of convenience and use-case oriented APIs that allows simple interaction with GoodData.CN.

Check out the [gooddata-sdk](./gooddata-sdk) documentation to learn more.

## GoodData.CN Foreign Data Wrapper for PostgreSQL

Foreign Data Wrapper (FDW) presents a way to map GoodData.CN semantic layer and/or insights stored in your GoodData.CN
into PostgreSQL as foreign tables that you can then query using SQL.

Check out the [gooddata-fdw package](./gooddata-fdw) documentation to learn more and get started.

## GoodData to pandas adapters

The [gooddata-pandas](./gooddata-pandas) is a thin layer that utilizes Python SDK and allows you to conveniently
create pandas series and data frames.

## Contributing

### Getting Started

1.  Ensure you have Python >3.7 installed: `python3 --version`

2.  Clone and setup environment:

    ```
    git clone git@github.com:gooddata/gooddata-python-sdk.git
    cd gooddata-python-sdk
    make dev
    ```

    The `make dev` command will create a new Python virtual environment in the `.venv` directory, install all
    third party dependencies into it and setup git hooks.

    Additionally if you use [direnv](https://direnv.net/) you can run `direnv allow .envrc` to enable automatic
    activation of the virtual environment that was previously created in `.venv`.

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
