# (C) 2022 GoodData Corporation
from __future__ import annotations

import functools
from pathlib import Path
from typing import Any, Optional, Union

from gooddata_api_client.exceptions import NotFoundException

from gooddata_sdk.catalog.catalog_service_base import CatalogServiceBase
from gooddata_sdk.catalog.data_source.action_model.requests.ldm_request import (
    CatalogGenerateLdmRequest,
    CatalogPdmLdmRequest,
)
from gooddata_sdk.catalog.data_source.action_model.requests.scan_model_request import CatalogScanModelRequest
from gooddata_sdk.catalog.data_source.action_model.requests.scan_sql_request import ScanSqlRequest
from gooddata_sdk.catalog.data_source.action_model.responses.scan_sql_response import ScanSqlResponse
from gooddata_sdk.catalog.data_source.declarative_model.data_source import (
    BIGQUERY_TYPE,
    DATABRICKS_TYPE,
    CatalogDeclarativeDataSource,
    CatalogDeclarativeDataSources,
)
from gooddata_sdk.catalog.data_source.declarative_model.physical_model.pdm import (
    CatalogDeclarativeTables,
    CatalogScanResultPdm,
)
from gooddata_sdk.catalog.data_source.entity_model.data_source import CatalogDataSource
from gooddata_sdk.catalog.entity import ClientSecretCredentialsFromFile, TokenCredentialsFromFile
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.ldm import CatalogDeclarativeModel
from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.utils import get_ds_credentials, load_all_entities_dict, read_layout_from_file

_PDM_DEPRECATION_MSG = "This method is going to be deprecated due to PDM removal."


class CatalogDataSourceService(CatalogServiceBase):
    """_summary_

    Args:
        CatalogServiceBase (_type_): _description_
    """

    def __init__(self, api_client: GoodDataApiClient) -> None:
        super().__init__(api_client)

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

        # Both or neither of the two (type, url) have to be defined in single patch call
        attributes["type"] = attributes.get("type", current_ds.type)
        attributes["url"] = attributes.get("url", current_ds.url)

        self._entities_api.patch_entity_data_sources(
            data_source_id, CatalogDataSource.to_api_patch(data_source_id, attributes)
        )

    def list_data_sources(self) -> list[CatalogDataSource]:
        """Lists all data sources.

        Args:
            None

        Returns:
            list[CatalogDataSource]:
                List of all Data Sources in the whole organization.
        """
        get_data_sources = functools.partial(
            self._entities_api.get_all_entities_data_sources,
            _check_return_type=False,
        )
        data_sources = load_all_entities_dict(get_data_sources)
        return [CatalogDataSource.from_api(ds) for ds in data_sources["data"]]

    # Declarative methods are listed below

    def get_declarative_data_sources(self) -> CatalogDeclarativeDataSources:
        """Retrieve all data sources.

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
        config_file: Optional[Union[str, Path]] = None,
        test_data_sources: bool = False,
    ) -> None:
        """Set all data sources, including their related physical data model.

        Args:
            declarative_data_sources (CatalogDeclarativeDataSources):
                Declarative Data Source object. Can be retrieved by get_declarative_data_sources.
            credentials_path (Optional[Path], optional):
                Path to the Credentials. Optional, defaults to None.
            config_file (Optional[Union[str, Path]], optional):
                Path to the config file. Defaults to None.
            test_data_sources (bool, optional):
                If True, the connection of data sources is tested. Defaults to False.

        Returns:
            None
        """
        if test_data_sources:
            self.test_data_sources_connection(declarative_data_sources, credentials_path, config_file)
        credentials = self._credentials_from_file(credentials_path) if credentials_path is not None else None
        self._layout_api.put_data_sources_layout(
            declarative_data_sources.to_api(credentials=credentials, config_file=config_file)
        )

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
        config_file: Optional[Union[str, Path]] = None,
        test_data_sources: bool = False,
    ) -> None:
        """Loads and sets layouts stored using `store_declarative_data_sources`.

        This method combines `load_declarative_data_sources` and `put_declarative_data_sources`
        methods to load and set layouts stored using `store_declarative_data_sources`.

        Args:
            layout_root_path (Optional[Path], optional):
                Path to the root of the layout directory. Defaults to Path.cwd().
            credentials_path (Optional[Path], optional):
                Path to the credentials.
            config_file (Optional[Union[str, Path]], optional):
                Path to the config file.
            test_data_sources (bool, optional):
                If True, the connection of data sources is tested. Defaults to False.

        Returns:
            None
        """
        data_sources = self.load_declarative_data_sources(layout_root_path)
        self.put_declarative_data_sources(data_sources, credentials_path, config_file, test_data_sources)

    @staticmethod
    def store_pdm_to_disk(pdm: CatalogDeclarativeTables, path: Path = Path.cwd()) -> None:
        """Store the physical data model layout in the directory.

        The directory structure below shows the output for the path set to Path("pdm_location").
        pdm_location
            └── pdm
                ├── table_A.yaml
                └── table_B.yaml

        Args:
            pdm (CatalogDeclarativeTables):
                Declarative PDM definition to be persisted on disk.
            path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            None
        """
        pdm.store_to_disk(path)

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

    def scan_pdm_and_generate_logical_model(
        self,
        data_source_id: str,
        generate_ldm_request: Optional[CatalogGenerateLdmRequest] = None,
        scan_request: CatalogScanModelRequest = CatalogScanModelRequest(),
        report_warnings: bool = False,
    ) -> tuple[CatalogDeclarativeModel, CatalogScanResultPdm]:
        """Scan data source and use returned PDM to generate logical data model. If generate_ldm_request
        contains PDM already, PDM tables received from the scan are appended without deduplication.

        Args:
            data_source_id (str):
                Data Source identification string. e.g. "demo"
            generate_ldm_request (CatalogGenerateLdmRequest, optional):
                LDM options. Defaults to CatalogGenerateLdmRequest(separator="__", wdf_prefix="wdf")
            scan_request (CatalogScanModelRequest, optional):
                Options for the Scan Request. Defaults to CatalogScanModelRequest().
            report_warnings (bool, optional):
                Switch to turn on warnings. Defaults to False.


        Returns:
            CatalogDeclarativeModel:
                Object Containing declarative Logical Data Model
            CatalogScanResultPdm:
                An instance of CatalogScanResultPdm.
                Containing pdm itself and a list of warnings that occurred during scanning.
        """
        if not generate_ldm_request:
            generate_ldm_request = CatalogGenerateLdmRequest(separator="__", wdf_prefix="wdf")

        scan_result = self.scan_data_source(data_source_id, scan_request, report_warnings)
        if generate_ldm_request.pdm and generate_ldm_request.pdm.tables:
            generate_ldm_request.pdm.tables.extend(scan_result.pdm.tables)
        elif generate_ldm_request.pdm:
            generate_ldm_request.pdm.tables = scan_result.pdm.tables
        else:
            generate_ldm_request.pdm = CatalogPdmLdmRequest(tables=scan_result.pdm.tables)
        return CatalogDeclarativeModel.from_api(
            self._actions_api.generate_logical_model(data_source_id, generate_ldm_request.to_api())
        ), scan_result

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
        self,
        declarative_data_sources: CatalogDeclarativeDataSources,
        credentials_path: Optional[Path] = None,
        config_file: Optional[Union[str, Path]] = None,
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
            config_file (Optional[Union[str, Path]], optional):
                Path to the config file. Defaults to None.

        Raises:
            ValueError:
                Check API references for possible errors of data source connections.

        Returns:
            None
        """

        credentials = dict()
        if credentials_path is not None and config_file is not None:
            raise ValueError("Only one of credentials or config_file should be provided")
        if credentials_path is not None:
            credentials = self._credentials_from_file(credentials_path)
        if config_file is not None:
            credentials = get_ds_credentials(config_file)

        errors: dict[str, str] = dict()
        for declarative_data_source in declarative_data_sources.data_sources:
            if credentials.get(declarative_data_source.id) is not None:
                if declarative_data_source.type == BIGQUERY_TYPE:
                    token = TokenCredentialsFromFile.token_from_file(credentials[declarative_data_source.id])
                    response = self._actions_api.test_data_source_definition(
                        declarative_data_source.to_test_request(token=token)
                    )
                elif declarative_data_source.type == DATABRICKS_TYPE:
                    if declarative_data_source.client_id and declarative_data_source.client_id.strip():
                        client_secret = ClientSecretCredentialsFromFile.client_secret_from_file(
                            credentials[declarative_data_source.id]
                        )
                        response = self._actions_api.test_data_source_definition(
                            declarative_data_source.to_test_request(client_secret=client_secret)
                        )
                    else:
                        token = TokenCredentialsFromFile.token_from_file(
                            file_path=credentials[declarative_data_source.id], base64_encode=False
                        )
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
            raise ValueError("There are no pairs of data source id and credentials.")
        credentials = data["data_sources"]
        return credentials
