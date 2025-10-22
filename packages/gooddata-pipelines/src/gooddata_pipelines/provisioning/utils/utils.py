# (C) 2025 GoodData Corporation

"""Module for utilities used in GoodData Pipelines provisioning."""

from typing import Any, cast

import attrs
from requests import Response


class AttributesMixin:
    """
    Mixin class to provide a method for getting attributes of an object which may or may not exist.
    """

    def get_attrs(
        self, *objects: object, overrides: dict[str, str] | None = None
    ) -> dict[str, str]:
        """
        Returns a dictionary of attributes from the given objects.

        Args:
            objects: The objects to get the attributes from. Special handling is implemented for
                    requests.Response, __dict__ attribute is used for general objects.
            overrides: A dictionary of attributes to override the object's attributes.
        Returns:
            dict: Returns a dictionary of the objects' attributes.
        """
        attributes: dict[str, str] = {}
        for index, context_object in enumerate(objects):
            if isinstance(context_object, str):
                attributes[f"string_context_{index}"] = context_object

            if isinstance(context_object, Response):
                # for request.Response objects, keys need to be renamed to match the log schema
                attributes.update(
                    {
                        "http_status": str(context_object.status_code),
                        "http_method": getattr(
                            context_object.request, "method", "NA"
                        ),
                        "api_endpoint": getattr(
                            context_object.request, "url", "NA"
                        ),
                    }
                )
            elif attrs.has(type(context_object)):
                for key, value in attrs.asdict(
                    cast(attrs.AttrsInstance, context_object)
                ).items():
                    self._add_to_dict(attributes, key, value)
            elif hasattr(context_object, "__dict__"):
                # Generic handling for other objects
                for key, value in context_object.__dict__.items():
                    self._add_to_dict(attributes, key, value)
            else:
                attributes[f"object_{index}"] = str(context_object)

        if overrides:
            attributes.update(overrides)

        return attributes

    def _add_to_dict(
        self, attributes: dict[str, str], key: str, value: Any
    ) -> None:
        if value is None:
            return

        if isinstance(value, list):
            attributes[key] = ", ".join(str(list_item) for list_item in value)
        else:
            attributes[key] = str(value)


@attrs.define
class EntityGroupIds:
    ids_in_both_systems: set[str]
    ids_to_delete: set[str]
    ids_to_create: set[str]
