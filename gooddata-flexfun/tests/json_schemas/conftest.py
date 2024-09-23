# (C) 2024 GoodData Corporation
from pathlib import Path
from typing import Any

import pytest
from jsonschema.validators import Draft202012Validator
from orjson import orjson
from referencing import Registry, Resource

SCHEMAS = Path("json_schemas")


def retrieve_from_filesystem(uri: str):
    path = SCHEMAS / Path(uri)
    contents = orjson.loads(path.read_text())
    return Resource.from_contents(contents)


@pytest.fixture
def schema_registry() -> Registry[Any]:
    return Registry(retrieve=retrieve_from_filesystem)


@pytest.fixture
def get_validator(schema_registry):
    def get_validator_for_schema(schema_uri):
        """Return a JSON schema validator for the given schema URI."""
        schema = schema_registry.get_or_retrieve(schema_uri)
        return Draft202012Validator(schema.value.contents, registry=schema_registry)

    return get_validator_for_schema
