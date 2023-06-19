# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Union, dict

import gooddata_api_client.models as afm_models
from gooddata_api_client.model_utils import OpenApiModel


class ObjId:
    def __init__(self, id: str, type: str) -> None:
        self._id: str = id
        self._type: str = type

    @property
    def id(self) -> str:
        return self._id

    @property
    def type(self) -> str:
        return self._type

    def as_afm_id(self) -> afm_models.AfmObjectIdentifier:
        return afm_models.AfmObjectIdentifier(
            identifier=afm_models.AfmObjectIdentifierIdentifier(id=self._id, type=self._type)
        )

    def as_afm_id_label(self) -> afm_models.AfmObjectIdentifierLabel:
        return afm_models.AfmObjectIdentifierLabel(
            identifier=afm_models.AfmObjectIdentifierLabelIdentifier(id=self._id)
        )

    def as_afm_id_dataset(self) -> afm_models.AfmObjectIdentifierDataset:
        return afm_models.AfmObjectIdentifierDataset(
            identifier=afm_models.AfmObjectIdentifierDatasetIdentifier(id=self._id)
        )

    def as_afm_id_attribute(self) -> afm_models.AfmObjectIdentifierAttribute:
        return afm_models.AfmObjectIdentifierAttribute(
            identifier=afm_models.AfmObjectIdentifierAttributeIdentifier(id=self._id)
        )

    def as_identifier(self) -> afm_models.AfmIdentifier:
        return afm_models.AfmIdentifier(
            identifier=afm_models.AfmObjectIdentifierIdentifier(id=self._id, type=self._type),
            _check_type=False,
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ObjId) and self.id == other.id and self.type == other.type

    def __str__(self) -> str:
        """
        String representation is used to transform ObjId to string key.

        :return: string in format <type>/<id>
        :rtype: str
        """
        return f"{self.type}/{self.id}"

    def __repr__(self) -> str:
        return f"{self.type}/{self.id}"


class ExecModelEntity:
    def __init__(self) -> None:
        pass

    def as_api_model(self) -> OpenApiModel:
        raise NotImplementedError()


class Filter(ExecModelEntity):
    def __init__(self) -> None:
        super(Filter, self).__init__()

        self._apply_on_result = None

    @property
    def apply_on_result(self) -> Union[bool, None]:
        return self._apply_on_result

    @classmethod
    def from_dict(cls, data: dict) -> "Filter":
        """Creates a new Filter instance from a dictionary.

        Args: data (dict):
            A dictionary containing the filter data, with key:
          'apply_on_result' (Optional[bool]):
            whether the Filter is applied

        Returns: Filter:
            A new Filter instance with its apply_on_result set."""
        filter_obj = cls()
        filter_obj._apply_on_result = data.get("apply_on_result")
        return filter_obj

    def is_noop(self) -> bool:
        raise NotImplementedError()

    def as_api_model(self) -> OpenApiModel:
        raise NotImplementedError()
