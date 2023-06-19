# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any, Optional, Union

import gooddata_api_client.models as afm_models
from gooddata_sdk.compute.model.base import ExecModelEntity, ObjId


class Attribute(ExecModelEntity):
    def __init__(self, local_id: str, label: Union[ObjId, str], show_all_values: Optional[bool] = None) -> None:
        """
        Creates new attribute that can be used to slice or dice metric values during computation.

        :param local_id: identifier of the attribute within the execution
        :param label: identifier of the label to use for slicing or dicing; specified either as ObjId or str containing
               the label id
        :param show_all_values: request show all values functionality for a given attribute
        """
        super(Attribute, self).__init__()

        self._local_id = local_id
        self._label = ObjId(label, "label") if isinstance(label, str) else label
        self._show_all_values = show_all_values

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Attribute":
        """Create a new Attribute instance from a dictionary.

        Args:
            data (dict[str, Any]):
                A dictionary containing the following keys:
                - local_id' (str):
                    Identifier of the attribute within the execution
                - label (str):
                    Identifier of the label to use for slicing or dicing;
                    specified either as ObjId or str containing the label id
                - show_all_values (Optional[bool]):
                    Request show all values functionality for a given attribute

        Returns:
            Attribute:
                A new Attribute instance with its local_id, label, and show_all_values set.
        """

        local_id = data["local_id"]
        label = data["label"]
        show_all_values = data.get("show_all_values")
        return cls(local_id, label, show_all_values)

    @property
    def local_id(self) -> str:
        return self._local_id

    @property
    def label(self) -> ObjId:
        return self._label

    @property
    def show_all_values(self) -> Optional[bool]:
        return self._show_all_values

    def has_same_label(self, other: ExecModelEntity) -> bool:
        return isinstance(other, Attribute) and other.label == self.label

    def as_api_model(self) -> afm_models.AttributeItem:
        optional_args = dict()
        if self._show_all_values is not None:
            optional_args["show_all_values"] = self._show_all_values
        return afm_models.AttributeItem(
            local_identifier=self.local_id, label=self.label.as_afm_id_label(), **optional_args
        )

    def __repr__(self) -> str:
        return (
            f"compute_model.Attribute(local_id='{self.local_id}', label='{self.label}', "
            f"show_all_values='{self._show_all_values}')"
        )
