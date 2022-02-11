# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Union

import gooddata_afm_client.models as afm_models
from gooddata_afm_client.model_utils import OpenApiModel


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
        return afm_models.AfmObjectIdentifier(identifier=afm_models.ObjectIdentifier(id=self._id, type=self._type))

    def as_identifier(self) -> afm_models.Identifier:
        return afm_models.Identifier(
            identifier=afm_models.ObjectIdentifier(id=self._id, type=self._type),
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

    def is_noop(self) -> bool:
        raise NotImplementedError()

    def as_api_model(self) -> OpenApiModel:
        raise NotImplementedError()
