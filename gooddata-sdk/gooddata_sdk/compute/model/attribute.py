# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Union

import gooddata_afm_client.models as afm_models
from gooddata_sdk.compute.model.base import ExecModelEntity, ObjId


class Attribute(ExecModelEntity):
    def __init__(self, local_id: str, label: Union[ObjId, str]) -> None:
        """
        Creates new attribute that can be used to slice or dice metric values during computation.

        :param local_id: identifier of the attribute within the execution
        :param label: identifier of the label to use for slicing or dicing; specified either as ObjId or str containing
               the label id
        """
        super(Attribute, self).__init__()

        self._local_id = local_id
        self._label = ObjId(label, "label") if isinstance(label, str) else label

    @property
    def local_id(self) -> str:
        return self._local_id

    @property
    def label(self) -> ObjId:
        return self._label

    def has_same_label(self, other: ExecModelEntity) -> bool:
        return isinstance(other, Attribute) and other.label == self.label

    def as_api_model(self) -> afm_models.AttributeItem:
        return afm_models.AttributeItem(local_identifier=self.local_id, label=self.label.as_afm_id())

    def __repr__(self) -> str:
        return f"compute_model.Attribute(local_id='{self.local_id}', label='{self.label}')"
