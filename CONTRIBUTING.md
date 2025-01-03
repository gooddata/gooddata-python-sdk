# Contributing

## Getting Started

1. Ensure you have at minimum Python 3.13 installed; Python 3.12, 3.11, 3.10 and 3.9 are optional for multi-environment tests

   This repo uses [tox](https://tox.readthedocs.io/en/latest/) and by default will try to run tests against all
   supported versions. If you have only subset of supported python interpreters installed, see
   [Run tests](#run-tests) section for information how to limit tests only to your subset.

2. Create your fork of `gooddata-python-sdk` repository

3. Clone and setup environment:

    ```bash
    git clone git@github.com:<your_user>/gooddata-python-sdk.git
    cd gooddata-python-sdk
    git remote add upstream git@github.com:gooddata/gooddata-python-sdk.git
    make dev
    # activate venv
    source .venv/bin/activate
    ```

   The `make dev` command will create a new Python 3.13 virtual environment in the `.venv` directory, install all
   third party dependencies into it and setup git hooks.

   Additionally, if you use [direnv](https://direnv.net/) you can run `direnv allow .envrc` to enable automatic
   activation of the virtual environment that was previously created in `.venv`.

   If `direnv` is not your cup of tea, you may want to adopt the PYTHONPATH exports that are done as part of the
   script so that you can run custom Python code using the packages container herein without installing them.

   To make sure you have successfully set up your environment run `make test` in virtualenv in the root of git repo.
   Please note, that `make test` executes tests against all the supported python versions. If you need to specify only
   subset of them, see section [Run tests](#Run tests)

4. Develop the feature or the fix. Make sure your code follows [coding conventions](#coding-conventions). Create pull
   request.


## Coding Conventions

This project uses [ruff](https://github.com/astral-sh/ruff) to ensure basic code sanity and for no-nonsense, consistent formatting.

`ruff` is part of the pre-commit hook that is automatically set up during `make dev`.

You can also run the lint and formatter manually:

-  To run `ruff` run: `make format-fix`

**NOTE:** If the pre-commit hook finds and auto-corrects some formatting errors, it will not auto-stage
the updated files and will fail the commit operation. You have to re-drive the commit. This is a well-known and
unlikely-to-change behavior of the [pre-commit](https://github.com/pre-commit/pre-commit/issues/806) package that this repository uses to manage hooks.

The project documents code by docstrings in [google-like](https://google.github.io/styleguide/pyguide.html#3-python-style-rules) format.

The project documentation is done in hugo. To contribute:

1. Install [Hugo](https://gohugo.io/)

2. Run `make new-docs`

The documentation is deployed using manually triggered GitHub workflows.

One logical change is done in one commit.

### Documenting new features

To document a new feature, you need to create a new `.md` file in one of the subsections. These subsections reresent the left navigation menu and are in a hierarchical directories.

e.g.:

     administration
         ├── organization
         │       ├── create_or_update_jwk.md
         │       ├── delete_jwk.md
         │       └── ...
         ├── premissions
         │       ├── list_available_assignees.md
         │       ├── get_declarative_organization_permissions.md
         │       └── ...
         └── ...


> Note that you would not only need to add new `.md` but also edit the existing `_index.md` in the same directory to add a link to your new method.

Example:

Imagine you just created a new method named `super_permissions_method` and would like to document it.

Steps:

1. You make sure to properly document your new method in the docstrings.

1. You create a new file `super_permissions_method.md` in `docs/content/en/docs/administration/permissions/`

    1. With content:

        ```
        ---
        title: "super_permissions_method"
        linkTitle: "super_permissions_method"
        superheading: "catalog_permission."
        weight: 100
        ---

        {{< python "sdk.CatalogPermissionService.super_permissions_method" >}}

        ## Example
        ```python
        # This method does something very cool, trust me bro
        sdk.super_permissions_method(user_id = "demo_user", give_all_permission = True)
        ```

        The `{{< python  "PATH" >}}` is a hugo shortcode, that will render the information about the method directly from the docstrings. The `PATH` parameter is represented as a path in the API references with a dot `.` denoting each step.

        So in our example, this is an `sdk` package with the permissions service (`CatalogPermissionService`) and then followed by the actual method (`super_permissions_method`).



1. You update the `_index.md` in the same folder:

    ```diff
    * [update_name](./update_name/)
    * [update_oidc_parameters](./update_oidc_parameters/)
    * [create_or_update_jwk](./create_or_update_jwk/)
    * [delete_jwk](./delete_jwk/)
    * [get_jwk](./get_jwk/)
    * [list_jwks](./list_jwks/)
    + * [super_permissions_method](./super_permissions_method/)
    ```

1. Lastly you contact someone from the documentation team for a proof-read and merge. Your changes should be visible in the preview in the PR job named `Netlify Deploy Preview`

## Run tests
Tests use [tox](https://tox.wiki/en/latest/index.html) and [pytest](https://docs.pytest.org/en/6.2.x/contents.html)
libraries. Each project has its own `tox.ini`.
**NOTE:** Tests are not executed for OpenAPI client projects.

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

Tests triggered by `make` can be controlled via these environment variables:
- `RECREATE_ENVS` - set environment variable `RECREATE_ENVS` to 1 and make will add `--recreate` flag, `--recreate`
  flag is not used otherwise
  ```bash
  RECREATE_ENVS=1 make test
  ```
- `TEST_ENVS` - define tox test environments (targets) as comma-separated list, by default all tox default targets are
  executed
  ```bash
  TEST_ENVS=py311,py310 make test
  ```
- `ADD_ARGS` - send additional arguments to pytest tool, useful for pin-pointing just part of tests
  ```bash
  ADD_ARGS="-k http_headers" make test
  ```

### How to update vcrpy tests
Some tests include HTTP call(s) to GD.CN instance. That tests are executed through
[vcrpy](https://vcrpy.readthedocs.io/) so that GD.CN instance is needed either first time or when request is changed.
It has clear benefits:
- ability to run the tests without GD.CN
- request and response snapshot - it makes debugging of HTTP calls simple

But there is one disadvantage. One needs GD.CN instance with the original setup to change tests.
`docker-compose.yaml` in root of the repository is here to help. It starts:
- GD.CN AIO in selected version
- postgres with gooddata-fdw extension
- service which setups GD.CN AIO demo project including PDM, LDM, metrics and visualizations

When a vcrpy supported test needs to be updated:
- start GD.CN using above `docker-compose.yaml`
- delete original vcrpy cassette with `make remove-cassettes`
- execute test
- update a newly generated cassette to the git

## Run continuous integration tests
Tests in pull request (PR) are executed using docker. The following is done to make test environment as close
to reproducible as possible:
- each supported python version has defined python base docker image
- tox version installed to docker is frozen to specific version
- all test dependencies specified in test-requirements.txt should be limited to some version range

Above rules give a chance to execute tests on localhost in the same or very similar environment as used in PR.
Orchestration is driven by `make test-ci`. Target `test-ci` supports the same features as `make test`, see
[Run tests](#Run tests) for details.

**NOTE:** docker tox tests and localhost tox tests are using the same .tox directory. Virtual environments for both test
types are most likely incompatible due to different base python version. tox is able to recognize it and recreate
venv automatically. So when docker tox tests are executed after localhost tests or vice-versa envs are recreated.

### Examples
- run all tests for all supported python environments
  ```bash
  make test-ci
  ```
- run all tests for all supported python environments and for one project
  ```bash
  cd gooddata-sdk
  make test-ci
  ```
- run all tests containing `http_headers` in name for py310 and py39 for all projects
  ```bash
  TEST_ENVS=py310,py39 ADD_ARGS="-k http_headers" make test-ci
  ```
- run tests on localhost against all-in-one image started with docker-compose
  ```bash
  RECREATE_ENVS=1 HOST_NETWORK=1 make test-ci
  ```

# How to generate and maintain OpenAPI clients
Refer to our [OpenAPI client README](./.openapi-generator/README.md)
