# (C) 2024 GoodData Corporation
"""Unit tests for CatalogWorkspaceParameter entity model.

These tests are pure-Python (no live server, no VCR cassettes) and exercise
the entity-model layer only: construction, serialization, and deserialization.
"""

from __future__ import annotations

from gooddata_sdk.catalog.workspace.entity_model.parameter import (
    CatalogNumberParameterDefinition,
    CatalogWorkspaceParameter,
    CatalogWorkspaceParameterConstraints,
)

# ---------------------------------------------------------------------------
# CatalogWorkspaceParameterConstraints
# ---------------------------------------------------------------------------


class TestCatalogWorkspaceParameterConstraints:
    def test_both_bounds(self) -> None:
        c = CatalogWorkspaceParameterConstraints(min=1.0, max=100.0)
        assert c.min == 1.0
        assert c.max == 100.0

    def test_min_only(self) -> None:
        c = CatalogWorkspaceParameterConstraints(min=0.0)
        assert c.min == 0.0
        assert c.max is None

    def test_max_only(self) -> None:
        c = CatalogWorkspaceParameterConstraints(max=50.0)
        assert c.min is None
        assert c.max == 50.0

    def test_no_bounds(self) -> None:
        c = CatalogWorkspaceParameterConstraints()
        assert c.min is None
        assert c.max is None

    def test_as_api_model_both_bounds(self) -> None:
        c = CatalogWorkspaceParameterConstraints(min=1.0, max=100.0)
        api = c.as_api_model()
        assert api["min"] == 1.0
        assert api["max"] == 100.0

    def test_as_api_model_no_bounds_omits_keys(self) -> None:
        c = CatalogWorkspaceParameterConstraints()
        api = c.as_api_model()
        # Neither min nor max should appear when they are None
        assert "min" not in api or api.get("min") is None
        assert "max" not in api or api.get("max") is None


# ---------------------------------------------------------------------------
# CatalogNumberParameterDefinition
# ---------------------------------------------------------------------------


class TestCatalogNumberParameterDefinition:
    def test_defaults(self) -> None:
        d = CatalogNumberParameterDefinition(default_value=42.0)
        assert d.default_value == 42.0
        assert d.type == "NUMBER"
        assert d.constraints is None

    def test_with_constraints(self) -> None:
        constraints = CatalogWorkspaceParameterConstraints(min=0.0, max=200.0)
        d = CatalogNumberParameterDefinition(default_value=10.0, constraints=constraints)
        assert d.constraints is not None
        assert d.constraints.min == 0.0
        assert d.constraints.max == 200.0

    def test_as_api_model_no_constraints(self) -> None:
        d = CatalogNumberParameterDefinition(default_value=5.0)
        api = d.as_api_model()
        assert api["default_value"] == 5.0

    def test_as_api_model_with_constraints(self) -> None:
        constraints = CatalogWorkspaceParameterConstraints(min=1.0, max=99.0)
        d = CatalogNumberParameterDefinition(default_value=50.0, constraints=constraints)
        api = d.as_api_model()
        assert api["default_value"] == 50.0
        assert api["constraints"]["min"] == 1.0
        assert api["constraints"]["max"] == 99.0


# ---------------------------------------------------------------------------
# CatalogWorkspaceParameter.init()
# ---------------------------------------------------------------------------


class TestCatalogWorkspaceParameterInit:
    def test_minimal(self) -> None:
        p = CatalogWorkspaceParameter.init(parameter_id="p1", default_value=7.0)
        assert p.id == "p1"
        assert p.definition is not None
        assert p.definition.default_value == 7.0
        assert p.definition.type == "NUMBER"
        assert p.definition.constraints is None
        assert p.title is None
        assert p.description is None
        assert p.tags == []

    def test_full(self) -> None:
        constraints = CatalogWorkspaceParameterConstraints(min=0.0, max=100.0)
        p = CatalogWorkspaceParameter.init(
            parameter_id="p2",
            default_value=50.0,
            title="My Param",
            description="A test parameter",
            tags=["tag1", "tag2"],
            constraints=constraints,
        )
        assert p.id == "p2"
        assert p.title == "My Param"
        assert p.description == "A test parameter"
        assert p.tags == ["tag1", "tag2"]
        assert p.definition is not None
        assert p.definition.constraints is not None
        assert p.definition.constraints.min == 0.0
        assert p.definition.constraints.max == 100.0

    def test_tags_default_to_empty_list(self) -> None:
        p = CatalogWorkspaceParameter.init(parameter_id="p3", default_value=1.0)
        assert p.tags == []
        assert isinstance(p.tags, list)


# ---------------------------------------------------------------------------
# CatalogWorkspaceParameter.from_api()
# ---------------------------------------------------------------------------


class TestCatalogWorkspaceParameterFromApi:
    """Test deserialization from snake_case dict (as returned by API model .to_dict())."""

    def _make_entity(
        self,
        *,
        id: str = "param-1",
        default_value: float = 10.0,
        param_type: str = "NUMBER",
        min_val: float | None = None,
        max_val: float | None = None,
        title: str | None = None,
        description: str | None = None,
        tags: list[str] | None = None,
    ) -> dict:
        """Build a snake_case dict that mimics a deserialized API response."""
        constraints: dict = {}
        if min_val is not None:
            constraints["min"] = min_val
        if max_val is not None:
            constraints["max"] = max_val

        definition: dict = {"default_value": default_value, "type": param_type}
        if constraints:
            definition["constraints"] = constraints

        attributes: dict = {"definition": definition}
        if title is not None:
            attributes["title"] = title
        if description is not None:
            attributes["description"] = description
        if tags is not None:
            attributes["tags"] = tags

        return {"id": id, "attributes": attributes}

    def test_minimal_entity(self) -> None:
        entity = self._make_entity()
        p = CatalogWorkspaceParameter.from_api(entity)
        assert p.id == "param-1"
        assert p.definition is not None
        assert p.definition.default_value == 10.0
        assert p.definition.type == "NUMBER"
        assert p.definition.constraints is None
        assert p.title is None
        assert p.description is None
        assert p.tags == []

    def test_full_entity(self) -> None:
        entity = self._make_entity(
            id="param-full",
            default_value=42.5,
            min_val=0.0,
            max_val=100.0,
            title="Full Param",
            description="Has everything",
            tags=["a", "b"],
        )
        p = CatalogWorkspaceParameter.from_api(entity)
        assert p.id == "param-full"
        assert p.definition is not None
        assert p.definition.default_value == 42.5
        assert p.definition.constraints is not None
        assert p.definition.constraints.min == 0.0
        assert p.definition.constraints.max == 100.0
        assert p.title == "Full Param"
        assert p.description == "Has everything"
        assert p.tags == ["a", "b"]

    def test_no_attributes(self) -> None:
        entity: dict = {"id": "bare"}
        p = CatalogWorkspaceParameter.from_api(entity)
        assert p.id == "bare"
        assert p.definition is None
        assert p.tags == []

    def test_tags_none_becomes_empty_list(self) -> None:
        entity = self._make_entity()
        entity["attributes"].pop("tags", None)
        p = CatalogWorkspaceParameter.from_api(entity)
        assert p.tags == []

    def test_default_value_fallback(self) -> None:
        """When default_value is missing, fall back to 0.0."""
        entity = {
            "id": "p-fallback",
            "attributes": {"definition": {"type": "NUMBER"}},
        }
        p = CatalogWorkspaceParameter.from_api(entity)
        assert p.definition is not None
        assert p.definition.default_value == 0.0


# ---------------------------------------------------------------------------
# CatalogWorkspaceParameter serialization round-trip
# ---------------------------------------------------------------------------


class TestCatalogWorkspaceParameterSerialization:
    def test_as_post_document(self) -> None:
        p = CatalogWorkspaceParameter.init(parameter_id="post-param", default_value=3.14)
        doc = p.as_post_document()
        data = doc.data
        assert data.type == "parameter"
        assert data.id == "post-param"

    def test_as_put_document(self) -> None:
        p = CatalogWorkspaceParameter.init(parameter_id="put-param", default_value=2.71)
        doc = p.as_put_document()
        data = doc.data
        assert data.type == "parameter"
        assert data.id == "put-param"

    def test_as_patch_document(self) -> None:
        p = CatalogWorkspaceParameter.init(parameter_id="patch-param", default_value=1.0)
        doc = p.as_patch_document()
        data = doc.data
        assert data.type == "parameter"
        assert data.id == "patch-param"

    def test_post_document_no_id(self) -> None:
        """When id is None, POST document should omit id."""
        p = CatalogWorkspaceParameter(
            id=None,
            definition=CatalogNumberParameterDefinition(default_value=5.0),
        )
        doc = p.as_post_document()
        data = doc.data
        assert data.type == "parameter"

    def test_build_attributes_with_title_and_description(self) -> None:
        p = CatalogWorkspaceParameter.init(
            parameter_id="p",
            default_value=1.0,
            title="T",
            description="D",
            tags=["x"],
        )
        attrs = p._build_attributes()
        assert "definition" in attrs
        assert attrs["definition"]["defaultValue"] == 1.0
        assert attrs["definition"]["type"] == "NUMBER"
        assert attrs["title"] == "T"
        assert attrs["description"] == "D"
        assert attrs["tags"] == ["x"]

    def test_build_attributes_with_constraints(self) -> None:
        constraints = CatalogWorkspaceParameterConstraints(min=0.0, max=50.0)
        p = CatalogWorkspaceParameter.init(
            parameter_id="p",
            default_value=25.0,
            constraints=constraints,
        )
        attrs = p._build_attributes()
        definition = attrs["definition"]
        assert definition["defaultValue"] == 25.0
        assert definition["constraints"]["min"] == 0.0
        assert definition["constraints"]["max"] == 50.0

    def test_build_attributes_no_tags_omitted(self) -> None:
        p = CatalogWorkspaceParameter.init(parameter_id="p", default_value=1.0)
        attrs = p._build_attributes()
        assert "tags" not in attrs

    def test_build_attributes_no_title_omitted(self) -> None:
        p = CatalogWorkspaceParameter.init(parameter_id="p", default_value=1.0)
        attrs = p._build_attributes()
        assert "title" not in attrs
        assert "description" not in attrs
