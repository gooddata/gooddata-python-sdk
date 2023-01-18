# (C) 2022 GoodData Corporation
from __future__ import annotations

import functools
from pathlib import Path
from typing import List, Optional, Union

import gooddata_api_client.models as afm_models
from gooddata_sdk.catalog.catalog_service_base import CatalogServiceBase
from gooddata_sdk.catalog.data_source.validation.data_source import DataSourceValidator
from gooddata_sdk.catalog.types import ValidObjects
from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.analytics_model import (
    CatalogDeclarativeAnalytics,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.ldm import CatalogDeclarativeModel
from gooddata_sdk.catalog.workspace.declarative_model.workspace.workspace import LAYOUT_WORKSPACES_DIR
from gooddata_sdk.catalog.workspace.entity_model.content_objects.dataset import (
    CatalogAttribute,
    CatalogFact,
    CatalogLabel,
)
from gooddata_sdk.catalog.workspace.entity_model.content_objects.metric import CatalogMetric
from gooddata_sdk.catalog.workspace.entity_model.graph_objects.graph import (
    CatalogDependentEntitiesRequest,
    CatalogDependentEntitiesResponse,
)
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


class CatalogWorkspaceContentService(CatalogServiceBase):
    # Note on the disabled checking:
    # generated client has issues parsing the vis objects; .. have to avoid return type checks
    #
    # note: the parsing is done lazily so it does not necessarily bomb on the next line but when trying to
    #  access returned object's properties

    def __init__(self, api_client: GoodDataApiClient) -> None:
        super(CatalogWorkspaceContentService, self).__init__(api_client)

    # Entities methods

    def get_full_catalog(self, workspace_id: str) -> CatalogWorkspaceContent:
        """Retrieves catalog for a workspace. Catalog contains all data sets and metrics defined in that workspace.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"

        Returns:
            CatalogWorkspaceContent:
                Object containing all data sets and metrics.
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

    def get_attributes_catalog(self, workspace_id: str) -> list[CatalogAttribute]:
        """Retrieve all attributes in a given workspace.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"

        Returns:
            list[CatalogAttribute]:
                List of all attributes in a given workspace.
        """
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
        """Retrieve all labels in a given workspace.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"

        Returns:
            list[CatalogLabel]:
                List of all labels in a given workspace.
        """
        get_labels = functools.partial(
            self._entities_api.get_all_entities_labels,
            workspace_id,
            _check_return_type=False,
        )
        labels = load_all_entities(get_labels)
        catalog_labels = [CatalogLabel(label) for label in labels.data]
        return catalog_labels

    def get_metrics_catalog(self, workspace_id: str) -> list[CatalogMetric]:
        """Retrieve all Metrics in a given workspace.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"

        Returns:
            list[CatalogMetric]:
                List of all metrics in a given workspace.
        """
        get_metrics = functools.partial(
            self._entities_api.get_all_entities_metrics, workspace_id, _check_return_type=False
        )
        metrics = load_all_entities(get_metrics)
        catalog_metrics = [CatalogMetric(metric) for metric in metrics.data]
        return catalog_metrics

    def get_facts_catalog(self, workspace_id: str) -> list[CatalogFact]:
        """Retrieve all facts in a given workspace.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"

        Returns:
            list[CatalogFact]:
                List of all facts in a given workspace.
        """
        get_facts = functools.partial(self._entities_api.get_all_entities_facts, workspace_id, _check_return_type=False)
        facts = load_all_entities(get_facts)
        catalog_facts = [CatalogFact(fact) for fact in facts.data]
        return catalog_facts

    def get_dependent_entities_graph(self, workspace_id: str) -> CatalogDependentEntitiesResponse:
        """There are dependencies among all catalog objects, the chain is the following:
        `fact/attribute/label → dataset → metric → visualization → dashboard`
        Some steps can be skipped, e.g. `fact → visualization`
        We do not support `table → dataset` dependency yet.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"

        Returns:
            CatalogDependentEntitiesResponse:
                TODO hkad98
        """
        return CatalogDependentEntitiesResponse.from_api(
            self._actions_api.get_dependent_entities_graph(workspace_id=workspace_id)
        )

    def get_dependent_entities_graph_from_entry_points(
        self, workspace_id: str, dependent_entities_request: CatalogDependentEntitiesRequest
    ) -> CatalogDependentEntitiesResponse:
        """Extends get_dependent_entities_graph with the entry point from which the graph is created.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"
            dependent_entities_request (CatalogDependentEntitiesRequest):
                TODO hkad98

        Returns:
            CatalogDependentEntitiesResponse:
                TODO hkad98
        """
        return CatalogDependentEntitiesResponse.from_api(
            self._actions_api.get_dependent_entities_graph_from_entry_points(
                workspace_id=workspace_id, dependent_entities_request=dependent_entities_request.to_api()
            )
        )

    # Declarative methods for logical data model

    def get_declarative_ldm(self, workspace_id: str) -> CatalogDeclarativeModel:
        """Retrieve a logical model layout. On CatalogDeclarativeModel user can call
        ``modify_mapped_data_source(data_source_mapping: dict)`` method,
        which substitutes data source id in datasets.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"

        Returns:
            CatalogDeclarativeModel:
                TODO hkad98
        """
        return CatalogDeclarativeModel.from_api(self._layout_api.get_logical_model(workspace_id))

    def put_declarative_ldm(
        self, workspace_id: str, ldm: CatalogDeclarativeModel, validator: Optional[DataSourceValidator] = None
    ) -> None:
        """Set declarative logical data model for a given workspace.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"
            ldm (CatalogDeclarativeModel):
                TODO hkad98
            validator (Optional[DataSourceValidator], optional):
                TODO. Defaults to None.

        Returns:
            None
        """
        if validator is not None:
            validator.validate_ldm(ldm)
        self._layout_api.set_logical_model(workspace_id, ldm.to_api())

    def store_declarative_ldm(self, workspace_id: str, layout_root_path: Path = Path.cwd()) -> None:
        """Store declarative logical data model for a given workspace in directory hierarchy.
            This method ties the LDM to the workspace and organization, thus it is recommended
            for backups. If you want to move LDM between workspaces or organizations, use store_ldm_to_disk.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            None
        """
        workspace_folder = self.layout_workspace_folder(workspace_id, layout_root_path)
        self.store_ldm_to_disk(workspace_id, workspace_folder)

    def load_declarative_ldm(self, workspace_id: str, layout_root_path: Path = Path.cwd()) -> CatalogDeclarativeModel:
        """Load declarative Logical Data Model, which was stored using store_declarative_workspaces

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            CatalogDeclarativeModel:
                TODO hkad98
        """
        workspace_folder = self.layout_workspace_folder(workspace_id, layout_root_path)
        return self.load_ldm_from_disk(workspace_folder)

    def load_and_put_declarative_ldm(
        self,
        workspace_id: str,
        layout_root_path: Path = Path.cwd(),
        validator: Optional[DataSourceValidator] = None,
    ) -> None:
        """This method combines load_declarative_ldm and put_declarative_ldm
        methods to load and set layouts stored using store_declarative_ldm.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().
            validator (Optional[DataSourceValidator], optional):
                TODO hkad98. Defaults to None.

        Returns:
            None
        """
        declarative_ldm = self.load_declarative_ldm(workspace_id, layout_root_path)
        self.put_declarative_ldm(workspace_id, declarative_ldm, validator)

    def store_ldm_to_disk(self, workspace_id: str, path: Path = Path.cwd()) -> None:
        """Store declarative logical data model for a given workspace in directory hierarchy.
            This method does not tie the LDM to the workspace and organization, thus it is recommended
            for migration between organizations. If you want to backup LDM use store_declarative_ldm.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"
            path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            None
        """
        self.get_declarative_ldm(workspace_id).store_to_disk(path)

    @staticmethod
    def load_ldm_from_disk(path: Path = Path.cwd()) -> CatalogDeclarativeModel:
        """Loads the Logical Data Model, which was stored using store_ldm_to_disk.

        Args:
            path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            CatalogDeclarativeModel:
                TODO hkad98
        """
        return CatalogDeclarativeModel.load_from_disk(path)

    # Declarative methods for analytics model

    def get_declarative_analytics_model(self, workspace_id: str) -> CatalogDeclarativeAnalytics:
        """Retrieves declarative analytics model. The model is tied to the workspace and organization.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"

        Returns:
            CatalogDeclarativeAnalytics:
                TODO hkad98
        """
        return CatalogDeclarativeAnalytics.from_api(self._layout_api.get_analytics_model(workspace_id))

    def put_declarative_analytics_model(self, workspace_id: str, analytics_model: CatalogDeclarativeAnalytics) -> None:
        """Sets the declarative analytics model for a given workspace.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"
            analytics_model (CatalogDeclarativeAnalytics):
                TODO hkad98

        Returns:
            None
        """
        self._layout_api.set_analytics_model(workspace_id, analytics_model.to_api())

    def store_declarative_analytics_model(self, workspace_id: str, layout_root_path: Path = Path.cwd()) -> None:
        """Store declarative analytics model for a given workspace in directory hierarchy.
            This method ties the declarative analytics model to the workspace and organization, thus it is
            recommended for backups. If you want to move declarative analytics model between workspaces or
            organizations, use store_analytics_model_to_disk.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            None
        """
        workspace_folder = self.layout_workspace_folder(workspace_id, layout_root_path)
        self.store_analytics_model_to_disk(workspace_id, workspace_folder)

    def load_declarative_analytics_model(
        self, workspace_id: str, layout_root_path: Path = Path.cwd()
    ) -> CatalogDeclarativeAnalytics:
        """Loads the declarative analytics model, which was stored using store_declarative_analytics_model.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            CatalogDeclarativeAnalytics:
                TODO hkad98
        """
        workspace_folder = self.layout_workspace_folder(workspace_id, layout_root_path)
        return self.load_analytics_model_from_disk(workspace_folder)

    def load_and_put_declarative_analytics_model(self, workspace_id: str, layout_root_path: Path = Path.cwd()) -> None:
        """This method combines load_declarative_analytics_model and put_analytics_model methods
        to load and set layouts stored using store_declarative_analytics_model.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            None
        """
        declarative_analytics_model = self.load_declarative_analytics_model(workspace_id, layout_root_path)
        self.put_declarative_analytics_model(workspace_id, declarative_analytics_model)

    def store_analytics_model_to_disk(self, workspace_id: str, path: Path = Path.cwd()) -> None:
        """Store analytics model for a given workspace in directory hierarchy.This method does not tie the declarative
            analytics model to the workspace and organization, thus it is recommended for migration between workspaces.
            If you want to migrate analytics model between workspaces, use store_analytics_model_to_disk.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"
            path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            None
        """
        self.get_declarative_analytics_model(workspace_id).store_to_disk(path)

    @staticmethod
    def load_analytics_model_from_disk(path: Path = Path.cwd()) -> CatalogDeclarativeAnalytics:
        """Loads the analytics model, which was stored using store_analytics_model_to_disk.

        Args:
            path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            CatalogDeclarativeAnalytics:
                TODO hkad98
        """
        return CatalogDeclarativeAnalytics.load_from_disk(path)

    # Help methods

    def layout_workspace_folder(self, workspace_id: str, layout_root_path: Path) -> Path:
        """Ties the LDM or Analytics Model to the Organization and workspaces in the store methods.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"
            layout_root_path (Path):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            Path:
                Path to the root of the layout directory for store methods.
        """
        return self.layout_organization_folder(layout_root_path) / LAYOUT_WORKSPACES_DIR / workspace_id

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

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"
            ctx (ValidObjectsInputType):
                items already in context. you can specify context in one of the following ways:

        Returns:
            ValidObjects:
                type of available object is used as key in the dict,
                the value is a set containing id's of available items
        """
        if isinstance(ctx, ExecutionDefinition):
            afm = compute_model_to_api_model(attributes=ctx.attributes, metrics=ctx.metrics, filters=ctx.filters)
        else:
            _ctx = ctx if isinstance(ctx, list) else [ctx]
            afm = self._prepare_afm_for_availability(_ctx)

        query = afm_models.AfmValidObjectsQuery(afm=afm, types=["facts", "attributes", "measures"])
        response = self._actions_api.compute_valid_objects(workspace_id=workspace_id, afm_valid_objects_query=query)

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
