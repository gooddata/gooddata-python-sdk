# (C) 2022 GoodData Corporation
from __future__ import annotations

import functools
from pathlib import Path
from typing import Any, List, Optional

from gooddata_api_client.exceptions import NotFoundException
from gooddata_api_client.model.declarative_pdm import DeclarativePdm
from gooddata_sdk.catalog.catalog_service_base import CatalogServiceBase
from gooddata_sdk.catalog.data_source.action_model.requests.ldm_request import CatalogGenerateLdmRequest
from gooddata_sdk.catalog.data_source.action_model.requests.scan_model_request import CatalogScanModelRequest
from gooddata_sdk.catalog.data_source.action_model.requests.scan_sql_request import ScanSqlRequest
from gooddata_sdk.catalog.data_source.action_model.responses.scan_sql_response import ScanSqlResponse
from gooddata_sdk.catalog.data_source.declarative_model.data_source import (
    BIGQUERY_TYPE,
    CatalogDeclarativeDataSource,
    CatalogDeclarativeDataSources,
)
from gooddata_sdk.catalog.data_source.declarative_model.physical_model.pdm import (
    CatalogDeclarativeTables,
    CatalogScanResultPdm,
)
from gooddata_sdk.catalog.data_source.entity_model.content_objects.table import CatalogDataSourceTable
from gooddata_sdk.catalog.data_source.entity_model.data_source import CatalogDataSource
from gooddata_sdk.catalog.entity import TokenCredentialsFromFile
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.ldm import CatalogDeclarativeModel
from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.utils import load_all_entities_dict, read_layout_from_file


class CatalogDataSourceService(CatalogServiceBase):
    """_summary_

    Args:
        CatalogServiceBase (_type_): _description_
    """

    def __init__(self, api_client: GoodDataApiClient) -> None:
        super(CatalogDataSourceService, self).__init__(api_client)

    # Entities methods are listed below

    def create_or_update_data_source(
        self,
        data_source: CatalogDataSource,
    ) -> None:
        """Pushes the Data Source to the GoodData environment.

        Automatically decides, whether to create or update.

        Args:
            data_source (CatalogDataSource):
                Catalog Data Source object

        Returns:
            None
        """
        try:
            self._entities_api.get_entity_data_sources(data_source.id)
            self._entities_api.update_entity_data_sources(
                data_source.id,
                data_source.to_api(),
            )
        except NotFoundException:
            self._entities_api.create_entity_data_sources(data_source.to_api())

    def get_data_source(self, data_source_id: str) -> CatalogDataSource:
        """Retrieve Data Source entity using data source id.

        Args:
            data_source_id (str): Data Source identification string e.g. "demo"

        Returns:
            CatalogDataSource: Data Source Object
        """
        return CatalogDataSource.from_api(
            self._entities_api.get_entity_data_sources(data_source_id).data.to_dict(camel_case=False)
        )

    def delete_data_source(self, data_source_id: str) -> None:
        """Delete data source using Data Source id.

        Args:
            data_source_id (str):
                Data Source identification string. e.g. "demo"

        Returns:
            None
        """
        self._entities_api.delete_entity_data_sources(data_source_id)

    def patch_data_source_attributes(self, data_source_id: str, attributes: dict) -> None:
        """Applies changes to the specified data source.

        Args:
            data_source_id (str):
                Data Source identification string. e.g. "demo"
            attributes (dict):
                A dictionary containing attributes of the data source to be changed.

        Returns:
            None
        """
        # TODO - workaround solution getting data source type from backend
        #      - once backend accepts empty value in this field (enum), remove this code
        current_ds = self.get_data_source(data_source_id)
        attributes["type"] = attributes.get("type", current_ds.type)

        self._entities_api.patch_entity_data_sources(
            data_source_id, CatalogDataSource.to_api_patch(data_source_id, attributes)
        )

    def list_data_sources(self) -> List[CatalogDataSource]:
        """Lists all data sources.

        Args:
            None

        Returns:
            List[CatalogDataSource]:
                List of all Data Sources in the whole organization.
        """
        get_data_sources = functools.partial(
            self._entities_api.get_all_entities_data_sources,
            _check_return_type=False,
        )
        data_sources = load_all_entities_dict(get_data_sources)
        return [CatalogDataSource.from_api(ds) for ds in data_sources["data"]]

    def list_data_source_tables(self, data_source_id: str) -> List[CatalogDataSourceTable]:
        """Lists all the data source tables for a given data source.

        Args:
            data_source_id (str):
                Data Source identification string. e.g. "demo"

        Returns:
            List[CatalogDataSourceTable]:
                List of Data Source Table objects
        """
        get_data_source_tables = functools.partial(
            self._entities_api.get_all_entities_data_source_tables,
            data_source_id,
            _check_return_type=False,
        )
        data_source_tables = load_all_entities_dict(get_data_source_tables, camel_case=False)
        return [CatalogDataSourceTable.from_dict(dst, camel_case=False) for dst in data_source_tables["data"]]

    # Declarative methods are listed below

    def get_declarative_data_sources(self) -> CatalogDeclarativeDataSources:
        """Retrieve all data sources, including their related physical data model.

        Args:
            None

        Returns:
            CatalogDeclarativeDataSources:
                Declarative Data Sources, including physical data model.
        """
        return CatalogDeclarativeDataSources.from_api(self._layout_api.get_data_sources_layout())

    def put_declarative_data_sources(
        self,
        declarative_data_sources: CatalogDeclarativeDataSources,
        credentials_path: Optional[Path] = None,
        test_data_sources: bool = False,
    ) -> None:
        """Set all data sources, including their related physical data model.

        Args:
            declarative_data_sources (CatalogDeclarativeDataSources):
                Declarative Data Source object. Can be retrieved by get_declarative_data_sources.
            credentials_path (Optional[Path], optional):
                Path to the Credentials. Optional, defaults to None.
            test_data_sources (bool, optional):
                If True, the connection of data sources is tested. Defaults to False.

        Returns:
            None
        """
        if test_data_sources:
            self.test_data_sources_connection(declarative_data_sources, credentials_path)
        credentials = self._credentials_from_file(credentials_path) if credentials_path is not None else dict()
        self._layout_api.put_data_sources_layout(declarative_data_sources.to_api(credentials))

    def store_declarative_data_sources(self, layout_root_path: Path = Path.cwd()) -> None:
        """Store data sources layouts in a directory hierarchy.

            gooddata_layouts
            └── organization_id
                    └── data_sources
                            ├── data_source_a
                            │       ├── pdm
                            │       │   ├── table_A.yaml
                            │       │   └── table_B.yaml
                            │       └── data_source_a.yaml
                            └── data_source_b
                                    └── pdm
                                    │   ├── table_X.yaml
                                    │   └── table_Y.yaml
                                    └── data_source_b.yaml

        Args:
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            None
        """
        self.get_declarative_data_sources().store_to_disk(self.layout_organization_folder(layout_root_path))

    def load_declarative_data_sources(self, layout_root_path: Path = Path.cwd()) -> CatalogDeclarativeDataSources:
        """Load declarative data sources layout, which was stored using store_declarative_data_sources.

        Args:
            layout_root_path (Optional[Path], optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            CatalogDeclarativeDataSources:
                Declarative Data Sources object
        """
        return CatalogDeclarativeDataSources.load_from_disk(self.layout_organization_folder(layout_root_path))

    def load_and_put_declarative_data_sources(
        self,
        layout_root_path: Path = Path.cwd(),
        credentials_path: Optional[Path] = None,
        test_data_sources: bool = False,
    ) -> None:
        """Loads and sets layouts stored using `store_declarative_data_sources`.

        This method combines `load_declarative_data_sources` and `put_declarative_data_sources`
        methods to load and set layouts stored using `store_declarative_data_sources`.

        Args:
            layout_root_path (Optional[Path], optional):
                Path to the root of the layout directory. Defaults to Path.cwd().
            credentials_path (Optional[Path], optional):
                Path to the credentials. Defaults to Path.cwd().
            test_data_sources (bool, optional):
                If True, the connection of data sources is tested. Defaults to False.

        Returns:
            None
        """
        data_sources = self.load_declarative_data_sources(layout_root_path)
        self.put_declarative_data_sources(data_sources, credentials_path, test_data_sources)

    def get_declarative_pdm(self, data_source_id: str) -> CatalogDeclarativeTables:
        """Retrieve physical data model for a given data source.

        Args:
            data_source_id (str):
                Data Source identification string. e.g. "demo"

        Returns:
            CatalogDeclarativeTables:
                Physical Data Model object.
        """
        return CatalogDeclarativeTables.from_api(self._layout_api.get_pdm_layout(data_source_id).get("pdm"))

    def put_declarative_pdm(self, data_source_id: str, declarative_tables: CatalogDeclarativeTables) -> None:
        """Set physical data model for a given data source.

        Args:
            data_source_id (str):
                Data Source identification string. e.g. "demo"
            declarative_tables (CatalogDeclarativeTables):
                Physical Data Model object. Can be obtained via get_declarative_pdm.

        Returns:
            None
        """
        declarative_pdm = DeclarativePdm(pdm=declarative_tables.to_api())
        self._layout_api.set_pdm_layout(data_source_id, declarative_pdm)

    def store_declarative_pdm(self, data_source_id: str, layout_root_path: Path = Path.cwd()) -> None:
        """Store physical data model layout in directory hierarchy for a given data source.

        gooddata_layouts
        └── organization_id
                └── data_sources
                        └── data_source_a
                                └── pdm
                                    ├── table_A.yaml
                                    └── table_B.yaml

        Args:
            data_source_id (str):
                Data Source identification string. e.g. "demo"
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            None
        """
        data_source_folder = self.data_source_folder(data_source_id, layout_root_path)
        self.get_declarative_pdm(data_source_id).store_to_disk(data_source_folder)

    def load_declarative_pdm(
        self, data_source_id: str, layout_root_path: Path = Path.cwd()
    ) -> CatalogDeclarativeTables:
        """Load declarative physical data model layout.

        Load declarative physical data model layout, which was stored using
        `store_declarative_pdm` for a given data source.

        Args:
            data_source_id (str):
                Data Source identification string. e.g. "demo"
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            CatalogDeclarativeTables: Physical Data Model object.
        """
        data_source_folder = self.data_source_folder(data_source_id, layout_root_path)
        return CatalogDeclarativeTables.load_from_disk(data_source_folder)

    def load_and_put_declarative_pdm(self, data_source_id: str, layout_root_path: Path = Path.cwd()) -> None:
        """Loads and sets layouts stored using `store_declarative_pdm`.

        This method combines load_declarative_pdm and `put_declarative_pdm` methods
        to load and set layouts stored using `store_declarative_pdm`.

        Args:
            data_source_id (str):
                Data Source identification string. e.g. "demo"
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            None
        """
        self.put_declarative_pdm(data_source_id, self.load_declarative_pdm(data_source_id, layout_root_path))

    def store_pdm_to_disk(self, datasource_id: str, path: Path = Path.cwd()) -> None:
        """Store the physical data model layout in the directory for a given data source.

        The directory structure below shows the output for the path set to Path("pdm_location").
        pdm_location
            └── pdm
                ├── table_A.yaml
                └── table_B.yaml

        Args:
            datasource_id (str):
                Data Source identification string. e.g. "demo"
            path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            None
        """
        self.get_declarative_pdm(datasource_id).store_to_disk(path)

    @staticmethod
    def load_pdm_from_disk(path: Path = Path.cwd()) -> CatalogDeclarativeTables:
        """This method is used to load pdm stored to disk using method store_pdm_to_disk.

        Args:
            path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            CatalogDeclarativeTables:
                Physical Data Model object.
        """
        return CatalogDeclarativeTables.load_from_disk(path)

    # Actions methods are listed below

    def generate_logical_model(
        self,
        data_source_id: str,
        generate_ldm_request: CatalogGenerateLdmRequest = CatalogGenerateLdmRequest(separator="__", wdf_prefix="wdf"),
    ) -> CatalogDeclarativeModel:
        """Generate logical data model for a data source.

        Args:
            data_source_id (str):
                Data Source identification string. e.g. "demo"
            generate_ldm_request (CatalogGenerateLdmRequest, optional):
                LDM options. Defaults to CatalogGenerateLdmRequest(separator="__", wdf_prefix="wdf")

        Returns:
            CatalogDeclarativeModel:
                Object Containing declarative Logical Data Model
        """
        return CatalogDeclarativeModel.from_api(
            self._actions_api.generate_logical_model(data_source_id, generate_ldm_request.to_api())
        )

    def register_upload_notification(self, data_source_id: str) -> None:
        """Invalidate cache of your computed reports to force your analytics to be recomputed.

        Args:
            data_source_id (str):
                Data Source identification string. e.g. "demo"

        Returns:
            None
        """
        self._actions_api.register_upload_notification(data_source_id)

    def scan_data_source(
        self,
        data_source_id: str,
        scan_request: CatalogScanModelRequest = CatalogScanModelRequest(),
        report_warnings: bool = False,
    ) -> CatalogScanResultPdm:
        """Scan data source specified by its id and optionally by specified scan request.

        CatalogScanResultPdm contains PDM and warnings. Warnings contain information about
        columns which were not added to the PDM because their data types are not supported.
        Additional parameter report_warnings can be passed to suppress or to report warnings.
        By default warnings are returned but not reported to STDOUT. If you set report_warnings
        to True, warnings are reported to STDOUT.

        Args:
            data_source_id (str):
                Data Source identification string. e.g. "demo"
            scan_request (CatalogScanModelRequest, optional):
                Options for the Scan Request. Defaults to CatalogScanModelRequest().
            report_warnings (bool, optional):
                Switch to turn on warnings. Defaults to False.

        Returns:
            CatalogScanResultPdm:
                An instance of CatalogScanResultPdm.
                Containing pdm itself and a list of warnings that occurred during scanning.
        """
        scan_result = CatalogScanResultPdm.from_api(
            self._actions_api.scan_data_source(data_source_id, scan_request.to_api())
        )
        if report_warnings:
            self.report_warnings(scan_result.warnings)
        return scan_result

    def scan_and_put_pdm(
        self, data_source_id: str, scan_request: CatalogScanModelRequest = CatalogScanModelRequest()
    ) -> None:
        """This method combines scan_data_source and put_declarative_pdm methods.

        Args:
            data_source_id (str):
                Data Source identification string. e.g. "demo"
            scan_request (CatalogScanModelRequest, optional):
                Options for the Scan Request. Defaults to CatalogScanModelRequest().

        Returns:
            None
        """
        self.put_declarative_pdm(data_source_id, self.scan_data_source(data_source_id, scan_request).pdm)

    def scan_schemata(self, data_source_id: str) -> list[str]:
        """Returns a list of schemas that exist in the database.

        Can be configured in the data source entity. Data source
        managers like Dremio or Drill can work with multiple schemas
        and schema names can be injected into scan_request to filter
        out tables stored in the different schemas.

        Args:
            data_source_id (str):
                Data Source identification string. e.g. "demo"

        Returns:
            list[str]:
                List of schema names for the given data source specified by its id.
        """
        response = self._actions_api.get_data_source_schemata(data_source_id)
        return response.get("schema_names", [])

    def scan_sql(self, data_source_id: str, sql_request: ScanSqlRequest) -> ScanSqlResponse:
        """Analyze SELECT SQL query in a given request.

        Return description of SQL result-set as list of column names with GoodData data types
        and list of example data returned by SELECT query.

        Args:
            data_source_id (str):
                Data Source identification string. e.g. "demo"
            sql_request (ScanSqlRequest):
                SELECT SQL query to analyze

        Returns:
            ScanSqlResponse:
                SELECT query analysis result
        """
        return ScanSqlResponse.from_api(self._actions_api.scan_sql(data_source_id, sql_request.to_api()))

    def test_data_sources_connection(
        self, declarative_data_sources: CatalogDeclarativeDataSources, credentials_path: Optional[Path] = None
    ) -> None:
        """Tests connection to declarative data sources.

        If `credentials_path` is omitted then the connection
        is tested with empty credentials. In case some connection
        failed the `ValueError` is raised with information about why
        the connection to the data source failed, e.g. host
        unreachable or invalid login or password.

        Args:
            declarative_data_sources (CatalogDeclarativeDataSources):
                Declarative Data Sources object
            credentials_path (Optional[Path], optional):
                Path to the credentials. Defaults to None.

        Raises:
            ValueError:
                Check API references for possible errors of data source connections.

        Returns:
            None
        """
        credentials = self._credentials_from_file(credentials_path) if credentials_path is not None else dict()
        errors: dict[str, str] = dict()
        for declarative_data_source in declarative_data_sources.data_sources:
            if credentials.get(declarative_data_source.id) is not None:
                if declarative_data_source.type == BIGQUERY_TYPE:
                    token = TokenCredentialsFromFile.token_from_file(credentials[declarative_data_source.id])
                    response = self._actions_api.test_data_source_definition(
                        declarative_data_source.to_test_request(token=token)
                    )
                else:
                    response = self._actions_api.test_data_source_definition(
                        declarative_data_source.to_test_request(password=credentials[declarative_data_source.id])
                    )
            else:
                response = self._actions_api.test_data_source_definition(declarative_data_source.to_test_request())
            if not response.successful:
                errors[declarative_data_source.id] = response.error
        if len(errors) != 0:
            message = []
            for k, v in errors.items():
                message.append(f"Test connection for data source id {k} ended with the following error {v}.")
            raise ValueError("\n".join(message))

    # Help methods are listed below

    @staticmethod
    def report_warnings(warnings: list[dict]) -> None:
        if warnings:
            print("Scan produced the following warnings: ")
            for warning in warnings:
                table_name = warning["name"]
                table_message = warning["message"]
                if "columns" in warning:
                    for column_warning in warning["columns"]:
                        column_name = column_warning["name"]
                        column_message = column_warning["message"]
                        print(f"table_name={table_name} column_name={column_name} column_message={column_message}")
                else:
                    print(f"table_name={table_name} table_message={table_message}")

    def data_source_folder(self, data_source_id: str, layout_root_path: Path) -> Path:
        """TODO

        Args:
            data_source_id (str):
                Data Source identification string. e.g. "demo"
            layout_root_path (Path):
                ...

        Returns:
            Path:
                Path to the source folder.
        """
        layout_organization_folder = self.layout_organization_folder(layout_root_path)
        data_sources_folder = CatalogDeclarativeDataSources.data_sources_folder(layout_organization_folder)
        return CatalogDeclarativeDataSource.data_source_folder(data_sources_folder, data_source_id)

    @staticmethod
    def _credentials_from_file(credentials_path: Path) -> dict[str, Any]:
        data = read_layout_from_file(credentials_path)
        if data.get("data_sources") is None:
            raise ValueError("The file has a wrong structure. There should be a root key 'data_sources'.")
        if len(data["data_sources"]) == 0:
            raise ValueError("There are no pairs of data source id and token.")
        credentials = data["data_sources"]
        return credentials
