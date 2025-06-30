# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Optional, Union

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
    def __init__(self, _apply_on_result: Optional[bool] = None) -> None:
        super().__init__()

        self._apply_on_result = _apply_on_result

    @property
    def apply_on_result(self) -> Union[bool, None]:
        return self._apply_on_result

    def is_noop(self) -> bool:
        raise NotImplementedError()

    def as_api_model(self) -> OpenApiModel:
        raise NotImplementedError()

    def description(self, labels: dict[str, str], format_locale: Optional[str] = None) -> str:
        """
        Description of the filter as it's visible for customer in UI.

        :param labels: Dict of labels in a form of `id: label`. Measures and attributes are expected to be here.
        :param format_locale: Locale ICU format to use for dates formatting in the description (ie. "en-US" or "cs-CZ")
        :return: Filter's human-readable description
        """
        raise NotImplementedError()
