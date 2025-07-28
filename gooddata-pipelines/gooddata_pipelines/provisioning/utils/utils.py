# (C) 2025 GoodData Corporation

"""Module for utilities used in GoodData Pipelines provisioning."""

from pydantic import BaseModel
from requests import Response


class AttributesMixin:
    """
    Mixin class to provide a method for getting attributes of an object which may or may not exist.
    """

    @staticmethod
    def get_attrs(
        *objects: object, overrides: dict[str, str] | None = None
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
        # TODO: This might not work great with nested objects, values  which are lists of objects etc.
        # If we care about parsing the logs back from the string, we should consider some other approach
        attrs: dict[str, str] = {}
        for context_object in objects:
            if isinstance(context_object, Response):
                # for request.Response objects, keys need to be renamed to match the log schema
                attrs.update(
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
            else:
                # Generic handling for other objects
                for key, value in context_object.__dict__.items():
                    if value is None:
                        continue

                    if isinstance(value, list):
                        attrs[key] = ", ".join(
                            str(list_item) for list_item in value
                        )
                    else:
                        attrs[key] = str(value)

        if overrides:
            attrs.update(overrides)

        return attrs


class SplitMixin:
    @staticmethod
    def split(string_value: str, delimiter: str = ",") -> list[str]:
        """
        Splits a string by the given delimiter and returns a list of stripped values.
        If the input is empty, returns an empty list.
        """
        if not string_value:
            return []

        return [value.strip() for value in string_value.split(delimiter)]


class EntityGroupIds(BaseModel):
    ids_in_both_systems: set[str]
    ids_to_delete: set[str]
    ids_to_create: set[str]
