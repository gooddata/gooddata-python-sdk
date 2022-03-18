# (C) 2022 GoodData Corporation
from __future__ import annotations

import functools
from pathlib import Path
from typing import List, Union

import yaml

import gooddata_afm_client.apis as afm_apis
import gooddata_afm_client.models as afm_models
import gooddata_metadata_client.apis as metadata_apis
from gooddata_metadata_client.exceptions import NotFoundException
from gooddata_sdk.catalog.types import ValidObjects
from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.analytics_model import (
    CatalogDeclarativeAnalytics,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.ldm import CatalogDeclarativeModel
from gooddata_sdk.catalog.workspace.declarative_model.workspace.workspace import (
    CatalogDeclarativeWorkspaceModel,
    CatalogDeclarativeWorkspaces,
)
from gooddata_sdk.catalog.workspace.entity_model.content_objects.dataset import (
    CatalogAttribute,
    CatalogFact,
    CatalogLabel,
)
from gooddata_sdk.catalog.workspace.entity_model.content_objects.metric import CatalogMetric
from gooddata_sdk.catalog.workspace.entity_model.workspace import CatalogWorkspace
from gooddata_sdk.catalog.workspace.model_container import CatalogWorkspaceContent
from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.compute.model.attribute import Attribute
from gooddata_sdk.compute.model.execution import ExecutionDefinition, compute_model_to_api_model
from gooddata_sdk.compute.model.filter import Filter
from gooddata_sdk.compute.model.metric import Metric
from gooddata_sdk.utils import load_all_entities

ValidObjectTypes = Union[Attribute, Metric, Filter, CatalogLabel, CatalogFact, CatalogMetric]

# Use typing collection types to support python < py3.9
ValidObjectsInputType = Union[ValidObjectTypes, List[ValidObjectTypes], ExecutionDefinition]


class CatalogWorkspaceService:
    def __init__(self, api_client: GoodDataApiClient) -> None:
        self._client = api_client
        self._entities_api = metadata_apis.EntitiesApi(api_client.metadata_client)
        self._layout_api = metadata_apis.LayoutApi(api_client.metadata_client)

    def list_workspaces(self) -> List[CatalogWorkspace]:
        get_workspaces = functools.partial(
            self._entities_api.get_all_entities_workspaces,
            include=["workspaces"],
            _check_return_type=False,
        )
        workspaces = load_all_entities(get_workspaces)
        return [CatalogWorkspace.from_api(w) for w in workspaces.data]

    def create_or_update(self, workspace: CatalogWorkspace) -> None:
        try:
            found_workspace = self.get_workspace(workspace.id)
            # Update of parent is not allowed
            if found_workspace.parent_id == workspace.parent_id:
                self._entities_api.update_entity_workspaces(
                    workspace.id,
                    workspace.to_api(),
                )
            else:
                raise ValueError(
                    f"Workspace parent can not be update. "
                    f"Original parent {found_workspace.parent_id}, wanted parent {workspace.parent_id}."
                )
        except NotFoundException:
            self._entities_api.create_entity_workspaces(workspace.to_api())

    def get_workspace(self, workspace_id: str) -> CatalogWorkspace:
        """
        Gets workspace content and returns it as CatalogWorkspace object.
        :param workspace_id: An input string parameter of workspace id.
        :return: CatalogWorkspace object containing structure of workspace.
        """
        return CatalogWorkspace.from_api(
            self._entities_api.get_entity_workspaces(workspace_id, include=["workspaces"]).data
        )

    def delete_workspace(self, workspace_id: str) -> None:
        """
        This method is implemented according to our implementation of delete workspace,
        which returns HTTP 204 no matter if the workspace_id exists.
        """
        workspaces = self.list_workspaces()
        if workspace_id not in [w.id for w in workspaces]:
            raise ValueError(f"Can not delete {workspace_id} workspace. This workspace does not exist.")
        children = [w.id for w in workspaces if w.parent_id == workspace_id]
        if children:
            raise ValueError(
                f"Can not delete {workspace_id} workspace. "
                f"This workspace is parent of the following workspaces: {', '.join(children)}. "
            )
        self._entities_api.delete_entity_workspaces(workspace_id)

    def get_declarative_workspace(self, workspace_id: str) -> CatalogDeclarativeWorkspaceModel:
        return CatalogDeclarativeWorkspaceModel.from_api(self._layout_api.get_workspace_layout(workspace_id))

    def put_declarative_workspace(self, workspace_id: str, workspace: CatalogDeclarativeWorkspaceModel) -> None:
        self._layout_api.put_workspace_layout(workspace_id, workspace.to_api())

    def get_declarative_workspaces(self) -> CatalogDeclarativeWorkspaces:
        return CatalogDeclarativeWorkspaces.from_api(self._layout_api.get_workspaces_layout())

    def put_declarative_workspaces(self, workspace: CatalogDeclarativeWorkspaces) -> None:
        self._layout_api.set_workspaces_layout(workspace.to_api())

    def store_declarative_workspaces(self, path: Path) -> None:
        workspaces = self._layout_api.get_workspaces_layout()
        workspace_data_filters = workspaces.workspace_data_filters
        with open(path / "workspace_data_filters.yaml", "w+") as fp:
            yaml.safe_dump([w.to_dict() for w in workspace_data_filters], fp, indent=2, sort_keys=True)
        for workspace in workspaces.workspaces:
            workspace_path = path / f"{workspace.id}.yaml"
            with open(workspace_path, "w+") as fp:
                yaml.safe_dump(workspace.to_dict(), fp, indent=2, sort_keys=True)

    def load_and_put_declarative_workspaces(self, path: Path) -> None:
        workspace_data_filters_path = path / "workspace_data_filters.yaml"
        if not workspace_data_filters_path.is_file():
            raise ValueError(f"Path {workspace_data_filters_path} is not valid.")
        workspace_files_path = path.glob("*.yaml")
        if not workspace_files_path:
            raise ValueError(f"There are no .yaml files in {workspace_files_path}.")
        with open(workspace_data_filters_path, "r") as f:
            workspace_data_filters = yaml.safe_load(f)
        workspaces = []
        for workspace in workspace_files_path:
            if workspace.stem != "workspace_data_filters":
                with open(workspace, "r") as f:
                    workspaces.append(yaml.safe_load(f))

        self.put_declarative_workspaces(
            CatalogDeclarativeWorkspaces.from_api(
                {"workspaces": workspaces, "workspace_data_filters": workspace_data_filters}
            )
        )


class CatalogWorkspaceContentService:
    # Note on the disabled checking:
    # generated client has issues parsing the vis objects; .. have to avoid return type checks
    #
    # note: the parsing is done lazily so it does not necessarily bomb on the next line but when trying to
    #  access returned object's properties

    def __init__(self, api_client: GoodDataApiClient) -> None:
        self._client = api_client
        self._entities_api = metadata_apis.EntitiesApi(api_client.metadata_client)
        self._afm_actions_api = afm_apis.ActionsApi(api_client.afm_client)
        self._layout_api = metadata_apis.LayoutApi(api_client.metadata_client)

    def get_attributes_catalog(self, workspace_id: str) -> list[CatalogAttribute]:
        get_attributes = functools.partial(
            self._entities_api.get_all_entities_attributes,
            workspace_id,
            _check_return_type=False,
        )
        attributes = load_all_entities(get_attributes)
        # Empty labels list is set. It will be changed in the future.
        catalog_attributes = [CatalogAttribute(attribute, []) for attribute in attributes.data]
        return catalog_attributes

    def get_labels_catalog(self, workspace_id: str) -> list[CatalogLabel]:
        get_labels = functools.partial(
            self._entities_api.get_all_entities_labels,
            workspace_id,
            _check_return_type=False,
        )
        labels = load_all_entities(get_labels)
        catalog_labels = [CatalogLabel(label) for label in labels.data]
        return catalog_labels

    def get_metrics_catalog(self, workspace_id: str) -> list[CatalogMetric]:
        get_metrics = functools.partial(
            self._entities_api.get_all_entities_metrics, workspace_id, _check_return_type=False
        )
        metrics = load_all_entities(get_metrics)
        catalog_metrics = [CatalogMetric(metric) for metric in metrics.data]
        return catalog_metrics

    def get_facts_catalog(self, workspace_id: str) -> list[CatalogFact]:
        get_facts = functools.partial(self._entities_api.get_all_entities_facts, workspace_id, _check_return_type=False)
        facts = load_all_entities(get_facts)
        catalog_facts = [CatalogFact(fact) for fact in facts.data]
        return catalog_facts

    def get_full_catalog(self, workspace_id: str) -> CatalogWorkspaceContent:
        """
        Retrieves catalog for a workspace. Catalog contains all data sets and metrics defined in that workspace.

        :param workspace_id: workspace identifier
        :return:
        """
        get_datasets = functools.partial(
            self._entities_api.get_all_entities_datasets,
            workspace_id,
            include=["attributes", "facts"],
            _check_return_type=False,
        )

        get_attributes = functools.partial(
            self._entities_api.get_all_entities_attributes,
            workspace_id,
            include=["labels"],
            _check_return_type=False,
        )

        get_metrics = functools.partial(
            self._entities_api.get_all_entities_metrics, workspace_id, _check_return_type=False
        )

        attributes = load_all_entities(get_attributes)
        datasets = load_all_entities(get_datasets)
        metrics = load_all_entities(get_metrics)

        valid_obj_fun = functools.partial(self.compute_valid_objects, workspace_id)

        return CatalogWorkspaceContent.create_workspace_content_catalog(valid_obj_fun, datasets, attributes, metrics)

    @staticmethod
    def _prepare_afm_for_availability(items: list[ValidObjectTypes]) -> afm_models.AFM:
        attributes = []
        metrics = []
        filters = []

        for item in items:
            if isinstance(item, Attribute):
                attributes.append(item)
            elif isinstance(item, Metric):
                metrics.append(item)
            elif isinstance(item, Filter):
                filters.append(item)
            elif isinstance(item, CatalogLabel):
                attributes.append(item.as_computable())
            elif isinstance(item, (CatalogFact, CatalogMetric)):
                metrics.append(item.as_computable())

        return compute_model_to_api_model(attributes=attributes, metrics=metrics, filters=filters)

    def compute_valid_objects(self, workspace_id: str, ctx: ValidObjectsInputType) -> ValidObjects:
        """
        Returns attributes, facts, and metrics which are valid to add to a context that already
        contains some entities from the semantic model. The entities are typically used to compute analytics and
        come from the execution definition. You may, however, specify the entities through different layers of
        convenience.

        :param workspace_id: workspace identifier
        :param ctx: items already in context. you can specify context in one of the following ways:
            - single item or list of items from the execution model
            - single item or list of items from catalog model; catalog fact, label or metric may be added
            - the entire execution definition that is used to compute analytics

        :return: a dict of sets; type of available object is used as key in the dict,
            the value is a set containing id's of available items
        """
        if isinstance(ctx, ExecutionDefinition):
            afm = compute_model_to_api_model(attributes=ctx.attributes, metrics=ctx.metrics, filters=ctx.filters)
        else:
            _ctx = ctx if isinstance(ctx, list) else [ctx]
            afm = self._prepare_afm_for_availability(_ctx)

        query = afm_models.AfmValidObjectsQuery(afm=afm, types=["facts", "attributes", "measures"])
        response = self._afm_actions_api.compute_valid_objects(workspace_id=workspace_id, afm_valid_objects_query=query)

        by_type: dict[str, set[str]] = dict()

        for available in response.items:
            _type = available["type"]

            if _type not in by_type:
                items_of_type: set[str] = set()
                by_type[_type] = items_of_type
            else:
                items_of_type = by_type[_type]

            items_of_type.add(available["id"])

        return by_type

    def get_declarative_ldm(self, workspace_id: str) -> CatalogDeclarativeModel:
        return CatalogDeclarativeModel.from_api(self._layout_api.get_logical_model(workspace_id))

    def store_declarative_ldm(self, workspace_id: str, path: Path) -> None:
        declarative_ldm = self._layout_api.get_logical_model(workspace_id)
        with open(path / f"declarative_ldm_{workspace_id}.yaml", "w+") as fp:
            yaml.safe_dump(declarative_ldm.to_dict(), fp, indent=2, sort_keys=True)

    def load_and_put_declarative_ldm(self, workspace_id: str, path: Path) -> None:
        with open(path / f"declarative_ldm_{workspace_id}.yaml", "r") as f:
            declarative_ldm = CatalogDeclarativeModel.from_api(yaml.safe_load(f))
        self.put_declarative_ldm(workspace_id, declarative_ldm)

    def put_declarative_ldm(self, workspace_id: str, ldm: CatalogDeclarativeModel) -> None:
        self._layout_api.set_logical_model(workspace_id, ldm.to_api())

    def get_declarative_analytics_model(self, workspace_id: str) -> CatalogDeclarativeAnalytics:
        return CatalogDeclarativeAnalytics.from_api(self._layout_api.get_analytics_model(workspace_id))

    def put_declarative_analytics_model(self, workspace_id: str, analytics_model: CatalogDeclarativeAnalytics) -> None:
        self._layout_api.set_analytics_model(workspace_id, analytics_model.to_api())

    def store_declarative_analytics_model(self, workspace_id: str, path: Path) -> None:
        declarative_analytics_model = self._layout_api.get_analytics_model(workspace_id)
        with open(path / f"declarative_analytics_model_{workspace_id}.yaml", "w+") as fp:
            yaml.safe_dump(declarative_analytics_model.to_dict(), fp, indent=2, sort_keys=True)

    def load_and_put_declarative_analytics_model(self, workspace_id: str, path: Path) -> None:
        with open(path / f"declarative_analytics_model_{workspace_id}.yaml", "r") as f:
            declarative_analytics_model = CatalogDeclarativeAnalytics.from_api(yaml.safe_load(f))
        self.put_declarative_analytics_model(workspace_id, declarative_analytics_model)
