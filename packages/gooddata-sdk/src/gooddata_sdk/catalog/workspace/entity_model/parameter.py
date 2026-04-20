# (C) 2024 GoodData Corporation
from __future__ import annotations

from typing import Any

import attrs
from gooddata_api_client.model.json_api_parameter_in import JsonApiParameterIn
from gooddata_api_client.model.json_api_parameter_in_document import JsonApiParameterInDocument
from gooddata_api_client.model.json_api_parameter_patch import JsonApiParameterPatch
from gooddata_api_client.model.json_api_parameter_patch_document import JsonApiParameterPatchDocument
from gooddata_api_client.model.json_api_parameter_post_optional_id import JsonApiParameterPostOptionalId
from gooddata_api_client.model.json_api_parameter_post_optional_id_document import (
    JsonApiParameterPostOptionalIdDocument,
)
from gooddata_api_client.model.number_constraints import NumberConstraints
from gooddata_api_client.model.number_parameter_definition import NumberParameterDefinition

from gooddata_sdk.catalog.base import Base


@attrs.define(kw_only=True)
class CatalogWorkspaceParameterConstraints(Base):
    """Constraints for a number parameter."""

    min: float | None = None
    max: float | None = None

    @staticmethod
    def client_class() -> type[NumberConstraints]:
        return NumberConstraints

    def as_api_model(self) -> NumberConstraints:
        kwargs: dict[str, Any] = {}
        if self.min is not None:
            kwargs["min"] = self.min
        if self.max is not None:
            kwargs["max"] = self.max
        return NumberConstraints(_check_type=False, **kwargs)


@attrs.define(kw_only=True)
class CatalogNumberParameterDefinition(Base):
    """Definition of a number-typed parameter."""

    default_value: float
    type: str = "NUMBER"
    constraints: CatalogWorkspaceParameterConstraints | None = None

    @staticmethod
    def client_class() -> type[NumberParameterDefinition]:
        return NumberParameterDefinition

    def as_api_model(self) -> NumberParameterDefinition:
        kwargs: dict[str, Any] = {}
        if self.constraints is not None:
            kwargs["constraints"] = self.constraints.as_api_model()
        return NumberParameterDefinition(
            default_value=self.default_value,
            _check_type=False,
            **kwargs,
        )


@attrs.define(kw_only=True)
class CatalogWorkspaceParameter(Base):
    """A workspace-scoped parameter entity."""

    id: str | None = None
    definition: CatalogNumberParameterDefinition | None = None
    title: str | None = None
    description: str | None = None
    tags: list[str] = attrs.field(factory=list)

    @staticmethod
    def client_class() -> type[JsonApiParameterIn]:
        return JsonApiParameterIn

    @classmethod
    def init(
        cls,
        *,
        parameter_id: str,
        default_value: float,
        title: str | None = None,
        description: str | None = None,
        tags: list[str] | None = None,
        constraints: CatalogWorkspaceParameterConstraints | None = None,
    ) -> CatalogWorkspaceParameter:
        definition = CatalogNumberParameterDefinition(
            default_value=default_value,
            constraints=constraints,
        )
        return cls(
            id=parameter_id,
            definition=definition,
            title=title,
            description=description,
            tags=tags or [],
        )

    @classmethod
    def from_api(cls, entity: Any) -> CatalogWorkspaceParameter:
        """Deserialize from an API model object or a snake_case dict.

        When entity is an API model object (ModelNormal), its internal
        _data_store uses snake_case keys.  When it is a plain dict produced
        by ``model.to_dict()``, the keys are also snake_case (the default).
        """
        attrs_data = entity.get("attributes") or {}
        raw_definition = attrs_data.get("definition")
        definition: CatalogNumberParameterDefinition | None = None
        if raw_definition is not None:
            raw_constraints = raw_definition.get("constraints")
            constraints: CatalogWorkspaceParameterConstraints | None = None
            if raw_constraints is not None:
                constraints = CatalogWorkspaceParameterConstraints(
                    min=raw_constraints.get("min"),
                    max=raw_constraints.get("max"),
                )
            definition = CatalogNumberParameterDefinition(
                default_value=raw_definition.get("default_value", 0.0),
                type=raw_definition.get("type", "NUMBER"),
                constraints=constraints,
            )
        raw_tags = attrs_data.get("tags")
        return cls(
            id=entity.get("id"),
            definition=definition,
            title=attrs_data.get("title"),
            description=attrs_data.get("description"),
            tags=raw_tags if raw_tags is not None else [],
        )

    def as_post_document(self) -> JsonApiParameterPostOptionalIdDocument:
        """Serialize to document for POST (create)."""
        attributes = self._build_attributes()
        kwargs: dict[str, Any] = {}
        if self.id is not None:
            kwargs["id"] = self.id
        data = JsonApiParameterPostOptionalId(
            type="parameter",
            attributes=attributes,
            _check_type=False,
            **kwargs,
        )
        return JsonApiParameterPostOptionalIdDocument(data=data, _check_type=False)

    def as_put_document(self) -> JsonApiParameterInDocument:
        """Serialize to document for PUT (full update)."""
        attributes = self._build_attributes()
        data = JsonApiParameterIn(
            id=self.id,
            type="parameter",
            attributes=attributes,
            _check_type=False,
        )
        return JsonApiParameterInDocument(data=data, _check_type=False)

    def as_patch_document(self) -> JsonApiParameterPatchDocument:
        """Serialize to document for PATCH."""
        attributes = self._build_attributes()
        data = JsonApiParameterPatch(
            id=self.id,
            type="parameter",
            attributes=attributes,
            _check_type=False,
        )
        return JsonApiParameterPatchDocument(data=data, _check_type=False)

    def _build_attributes(self) -> dict[str, Any]:
        attributes: dict[str, Any] = {}
        if self.definition is not None:
            definition_dict: dict[str, Any] = {
                "defaultValue": self.definition.default_value,
                "type": self.definition.type,
            }
            if self.definition.constraints is not None:
                constraints_dict: dict[str, Any] = {}
                if self.definition.constraints.min is not None:
                    constraints_dict["min"] = self.definition.constraints.min
                if self.definition.constraints.max is not None:
                    constraints_dict["max"] = self.definition.constraints.max
                if constraints_dict:
                    definition_dict["constraints"] = constraints_dict
            attributes["definition"] = definition_dict
        if self.title is not None:
            attributes["title"] = self.title
        if self.description is not None:
            attributes["description"] = self.description
        if self.tags:
            attributes["tags"] = self.tags
        return attributes
