# (C) 2021 GoodData Corporation
from __future__ import annotations

from typing import Optional

import gooddata_sdk as sdk


def _sanitize_str_for_postgres(string: str, used_names: Optional[dict[str, bool]] = None) -> str:
    # replace non-alpha-num stuff with underscores
    with_underscores = "".join(char if char.isalnum() else "_" for char in string.lower())

    # then get rid of sequences of underscores
    candidate = "_".join([s for s in with_underscores.split("_") if s != ""])

    if used_names is None:
        return candidate

    return _ensure_unique(candidate, used_names)


def _ensure_unique(candidate: str, used_names: dict[str, bool]) -> str:
    # ensure column name uniqueness - in a dumb way by appending some number
    if candidate in used_names:
        i = 1
        new_candidate = f"{candidate}_{i}"

        while new_candidate in used_names:
            i += 1
            new_candidate = f"{candidate}_{i}"

        return new_candidate

    return candidate


#
# Column naming during IMPORT SCHEMA is delegated to strategies. The idea is that we may want to support
# different strategies and let user select the desired one through OPTIONS during import.
#


class InsightTableNamingStrategy:
    def table_name_for_insight(self, insight: sdk.Visualization) -> str:
        raise NotImplementedError()


class DefaultInsightTableNaming(InsightTableNamingStrategy):
    def __init__(self) -> None:
        self._uniques: dict[str, bool] = dict()

    def table_name_for_insight(self, insight: sdk.Visualization) -> str:
        new_name = _sanitize_str_for_postgres(insight.title, self._uniques)
        self._uniques[new_name] = True

        return new_name


class InsightColumnNamingStrategy:
    def col_name_for_attribute(self, attr: sdk.VisualizationAttribute) -> str:
        raise NotImplementedError()

    def col_name_for_metric(self, attr: sdk.VisualizationMetric) -> str:
        raise NotImplementedError()


class DefaultInsightColumnNaming(InsightColumnNamingStrategy):
    def __init__(self) -> None:
        self._uniques: dict[str, bool] = dict()

    def col_name_for_attribute(self, attr: sdk.VisualizationAttribute) -> str:
        new_name = _sanitize_str_for_postgres(attr.label_id, self._uniques)
        self._uniques[new_name] = True

        return new_name

    def col_name_for_metric(self, metric: sdk.VisualizationMetric) -> str:
        # if simple measure, use the item identifier (nice, readable)
        # otherwise try alias
        # otherwise try title
        # otherwise use local_id (arbitrary, AD created local_ids are messy)
        # TODO: improve this heuristic to get better names for derived measures
        id_to_use = metric.item_id or metric.alias or metric.title or metric.local_id
        new_name = _sanitize_str_for_postgres(id_to_use, self._uniques)
        self._uniques[new_name] = True

        return new_name


class CatalogNamingStrategy:
    def col_name_for_label(self, attr: sdk.CatalogLabel) -> str:
        raise NotImplementedError()

    def col_name_for_fact(self, attr: sdk.CatalogFact) -> str:
        raise NotImplementedError()

    def col_name_for_metric(self, attr: sdk.CatalogMetric) -> str:
        raise NotImplementedError()


class DefaultCatalogNamingStrategy:
    def __init__(self) -> None:
        self._uniques: dict[str, bool] = dict()

    def _col_name_for_id_without_prefix(self, item_id: str, dataset: sdk.CatalogDataset) -> str:
        ds_prefix = f"{dataset.id}."
        # some of our tests project have convention where fact/label is as: dataset.dataset_something
        # that looks awkward in a table.. thus this funny stuff
        use_id = item_id if not item_id.startswith(f"{ds_prefix}{dataset.id}") else item_id[len(ds_prefix) :]
        new_name = _sanitize_str_for_postgres(use_id, self._uniques)
        self._uniques[new_name] = True

        return new_name

    def col_name_for_label(self, label: sdk.CatalogLabel, dataset: sdk.CatalogDataset) -> str:
        return self._col_name_for_id_without_prefix(label.id, dataset)

    def col_name_for_fact(self, fact: sdk.CatalogFact, dataset: sdk.CatalogDataset) -> str:
        return self._col_name_for_id_without_prefix(fact.id, dataset)

    def col_name_for_metric(self, metric: sdk.CatalogMetric) -> str:
        new_name = _sanitize_str_for_postgres(metric.id, self._uniques)
        self._uniques[new_name] = True

        return new_name
