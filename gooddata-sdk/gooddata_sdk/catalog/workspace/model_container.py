# (C) 2022 GoodData Corporation
from __future__ import annotations

import functools
from typing import List, Union

from gooddata_sdk.catalog.types import ValidObjects
from gooddata_sdk.catalog.workspace.entity_model.content_objects.dataset import (
    CatalogAttribute,
    CatalogDataset,
    CatalogFact,
    CatalogLabel,
)
from gooddata_sdk.catalog.workspace.entity_model.content_objects.metric import CatalogMetric
from gooddata_sdk.compute.model.attribute import Attribute
from gooddata_sdk.compute.model.base import ObjId
from gooddata_sdk.compute.model.execution import ExecutionDefinition
from gooddata_sdk.compute.model.filter import Filter
from gooddata_sdk.compute.model.metric import Metric
from gooddata_sdk.utils import AllPagedEntities, IdObjType

ValidObjectTypes = Union[Attribute, Metric, Filter, CatalogLabel, CatalogFact, CatalogMetric]

# Use typing collection types to support python < py3.9
ValidObjectsInputType = Union[ValidObjectTypes, List[ValidObjectTypes], ExecutionDefinition]


class CatalogWorkspaceContent:
    def __init__(
        self,
        valid_obj_fun: functools.partial[dict[str, set[str]]],
        datasets: list[CatalogDataset],
        metrics: list[CatalogMetric],
    ) -> None:
        self._valid_obf_fun = valid_obj_fun
        self._datasets = datasets
        self._metrics = metrics
        self._metric_idx = dict([(str(m.obj_id), m) for m in metrics])
        self._datasets_idx = dict([(str(d.obj_id), d) for d in datasets])

    @property
    def datasets(self) -> list[CatalogDataset]:
        return self._datasets

    @property
    def metrics(self) -> list[CatalogMetric]:
        return self._metrics

    def get_metric(self, metric_id: Union[str, ObjId]) -> Union[CatalogMetric, None]:
        """
        Gets metric by id. The id can be either an instance of ObjId or string containing serialized ObjId
        ('metric/some.metric.id') or contain just the id part ('some.metric.id').

        :param metric_id: fully qualified metric entity id (type/id) or just the identifier of metric entity

        :return: instance of CatalogMetric or None if no such metric in catalog

        :rtype: CatalogMetric
        """
        if isinstance(metric_id, ObjId):
            obj_id_str = str(metric_id)
        elif not metric_id.startswith("metric/"):
            obj_id_str = f"metric/{metric_id}"
        else:
            obj_id_str = metric_id

        return self._metric_idx[obj_id_str] if obj_id_str in self._metric_idx else None

    def get_dataset(self, dataset_id: Union[str, ObjId]) -> Union[CatalogDataset, None]:
        """
        Gets dataset by id. The id can be either an instance of ObjId or string containing serialized ``ObjId
        ('dataset/some.dataset.id')`` or contain just the id part (``some.dataset.id``).

        :param dataset_id: fully qualified dataset entity id (type/id) or just the identifier of dataset entity

        :return: instance of CatalogDataset or None if no such dataset in catalog

        :rtype: CatalogDataset
        """
        if isinstance(dataset_id, ObjId):
            obj_id_str = str(dataset_id)
        elif not dataset_id.startswith("dataset/"):
            obj_id_str = f"dataset/{dataset_id}"
        else:
            obj_id_str = dataset_id

        return self._datasets_idx[obj_id_str] if obj_id_str in self._datasets_idx else None

    def find_label_attribute(self, id_obj: IdObjType) -> Union[CatalogAttribute, None]:
        """Get attribute by label id."""
        for dataset in self._datasets:
            res = dataset.find_label_attribute(id_obj)

            if res is not None:
                return res

        return None

    def _valid_objects(self, ctx: ValidObjectsInputType) -> ValidObjects:
        return self._valid_obf_fun(ctx)

    def catalog_with_valid_objects(self, ctx: ValidObjectsInputType) -> CatalogWorkspaceContent:
        """
        Returns a new instance of catalog which contains only those datasets (attributes and facts) that are valid in
        the provided context. The context is composed of one more more entities of the semantic model and
        the filtered catalog will contain only those entities that can be safely added on top of that existing context.

        :param ctx: existing context. you can specify context in one of the following ways:

         - single item or list of items from the execution model
         - single item or list of items from catalog model; catalog fact, label or metric may be added
         - the entire execution definition that is used to compute analytics

        """
        valid_objects = self._valid_objects(ctx)

        new_datasets = list(filter(None, [d.filter_dataset(valid_objects) for d in self.datasets]))
        new_metrics = [m for m in self.metrics if m.id in valid_objects[m.type]]

        return CatalogWorkspaceContent(
            self._valid_obf_fun,
            datasets=new_datasets,
            metrics=new_metrics,
        )

    @classmethod
    def create_workspace_content_catalog(
        cls,
        valid_obj_fun: functools.partial[dict[str, set[str]]],
        datasets: AllPagedEntities,
        attributes: AllPagedEntities,
        metrics: AllPagedEntities,
    ) -> CatalogWorkspaceContent:
        catalog_datasets = [
            CatalogDataset.from_api(d, side_loads=datasets.included, related_entities=attributes) for d in datasets.data
        ]

        catalog_metrics = [CatalogMetric.from_api(metric) for metric in metrics.data]

        return cls(
            valid_obj_fun=valid_obj_fun,
            datasets=list(catalog_datasets),
            metrics=catalog_metrics,
        )

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(datasets={self.datasets})"
