# (C) 2023 GoodData Corporation
import copy
import json
import re
from pathlib import Path
from typing import Optional, Union

import attrs
from gooddata_sdk import CatalogDeclarativeColumn, CatalogDeclarativeTable, CatalogDeclarativeTables
from gooddata_sdk.utils import safeget

from gooddata_dbt.dbt.base import (
    DATE_GRANULARITIES,
    DATETIME_DATA_TYPES,
    DBT_PATH_TO_MANIFEST,
    DBT_TARGET_DIR,
    NUMERIC_DATA_TYPES,
    TIMESTAMP_DATA_TYPES,
    TIMESTAMP_GRANULARITIES,
    Base,
    GoodDataLabelType,
    GoodDataLdmType,
    GoodDataSortDirection,
)
from gooddata_dbt.dbt.cloud import DbtConnection


@attrs.define(auto_attribs=True, kw_only=True)
class DbtModelMetaGoodDataTableProps(Base):
    model_id: Optional[str] = None


@attrs.define(auto_attribs=True, kw_only=True)
class DbtModelMetaGoodDataColumnProps(Base):
    id: Optional[str] = None
    ldm_type: Optional[GoodDataLdmType] = None
    referenced_table: Optional[str] = None
    label_type: Optional[GoodDataLabelType] = None
    attribute_column: Optional[str] = None
    sort_column: Optional[str] = None
    sort_direction: Optional[GoodDataSortDirection] = None
    default_view: Optional[bool] = None

    @property
    def gooddata_ref_table_ldm_id(self) -> Optional[str]:
        if self.referenced_table:
            return self.referenced_table.lower()
        return None

    def upper_case_names(self) -> None:
        if self.referenced_table:
            self.referenced_table = self.referenced_table.upper()
        if self.attribute_column:
            self.attribute_column = self.attribute_column.upper()
        if self.sort_column:
            self.sort_column = self.sort_column.upper()


@attrs.define(auto_attribs=True, kw_only=True)
class DbtModelMetaGoodDataTable(Base):
    gooddata: DbtModelMetaGoodDataTableProps = attrs.field(factory=DbtModelMetaGoodDataTableProps)


@attrs.define(auto_attribs=True, kw_only=True)
class DbtModelMetaGoodDataColumn(Base):
    gooddata: DbtModelMetaGoodDataColumnProps = attrs.field(factory=DbtModelMetaGoodDataColumnProps)


@attrs.define(auto_attribs=True, kw_only=True)
class DbtModelBase(Base):
    name: str
    description: str
    tags: list[str]
    # If 2+ references point to the same table, the table plays multiple roles,
    # it must be generated as multiple datasets
    role_name: Optional[str] = None

    # TODO - duplicate of backend logic.
    # Solution: use result of generateLdm as a master template, and override based on dbt metadata only if necessary
    @staticmethod
    def beautify_title(name: str) -> str:
        re_invalid_chars = re.compile(r"[^a-z0-9 ]", re.I)
        re_spaces = re.compile(r"\s+")
        if name == name.upper():
            # Snowflake-like DBs expose upper-case by default
            name = name.lower()
        name = re_invalid_chars.sub(" ", name)
        name = re_spaces.sub(" ", name)
        return name.capitalize()

    # Title is not supported by dbt, we fill it here
    @property
    def title(self) -> str:
        return self.description or self.beautify_title(self.name)

    @property
    def gooddata_ldm_id(self) -> str:
        if self.role_name:
            return f"{self.name.lower()}_{self.role_name.lower()}"
        else:
            return self.name.lower()

    @property
    def gooddata_ldm_title(self) -> str:
        if self.role_name:
            return f"{self.title} ({self.role_name.lower()})"
        else:
            return self.title

    @property
    def gooddata_ldm_description(self) -> str:
        if self.role_name and self.description:
            return f"{self.description} ({self.role_name.lower()})"
        else:
            return self.description

    def upper_case_name(self) -> None:
        self.name = self.name.upper()


@attrs.define(auto_attribs=True, kw_only=True)
class DbtModelColumn(DbtModelBase):
    data_type: Optional[str]
    meta: DbtModelMetaGoodDataColumn = attrs.field(factory=DbtModelMetaGoodDataColumn)

    # Enable to override LDM ID for LDM entities derived from columns (attributes, ...)
    # TODO - does it work for PK/references in combination with roles?
    @property
    def ldm_id(self) -> str:
        return self.meta.gooddata.id or self.gooddata_ldm_id

    @property
    def ldm_type(self) -> Optional[str]:
        if self.meta.gooddata.ldm_type is None:
            return None
        else:
            return self.meta.gooddata.ldm_type.value

    @property
    def label_type(self) -> Optional[str]:
        if self.meta.gooddata.label_type is None:
            return None
        else:
            return self.meta.gooddata.label_type.value

    @property
    def sort_direction(self) -> Optional[str]:
        if self.meta.gooddata.sort_direction is None:
            return None
        else:
            return self.meta.gooddata.sort_direction.value

    def gooddata_is_fact(self) -> bool:
        return (self.meta.gooddata.ldm_type == GoodDataLdmType.FACT) or self.is_number()

    def gooddata_is_attribute(self) -> bool:
        valid_ldm_types = [GoodDataLdmType.ATTRIBUTE, GoodDataLdmType.PRIMARY_KEY]
        # Without GD metadata, attribute is default unless it is DATETIME/NUMBER(FLOAT) data type
        return self.meta.gooddata.ldm_type in valid_ldm_types or (
            self.meta.gooddata.ldm_type is None and not self.is_date() and not self.is_number()
        )

    def gooddata_is_label(self, attribute_column_name: str) -> bool:
        return (
            self.meta.gooddata.ldm_type == GoodDataLdmType.LABEL
            and attribute_column_name == self.meta.gooddata.attribute_column
        )

    def is_date(self) -> bool:
        if self.data_type is None:
            return False
        gooddata_date = self.meta.gooddata.ldm_type == GoodDataLdmType.DATE
        return gooddata_date or self.data_type.upper() in DATETIME_DATA_TYPES

    def is_number(self) -> bool:
        if self.data_type is None:
            return False
        return self.data_type.upper() in NUMERIC_DATA_TYPES

    def is_reference(self) -> bool:
        return self.meta.gooddata.ldm_type == GoodDataLdmType.REFERENCE


@attrs.define(auto_attribs=True, kw_only=True)
class DbtModelTable(DbtModelBase):
    schema: str
    columns: dict[str, DbtModelColumn]
    meta: DbtModelMetaGoodDataTable = attrs.field(factory=DbtModelMetaGoodDataTable)


class DbtModelTables:
    """
    TODO:
        * add 2 class method – from_cloud, from_local
        * DbtModelTables should accept tables only
        * check dbt Cloud if it gives data type
            * if yes get rid off LDM if possible and other fun
        * column_type – Optional if missing call  scan
    """

    def __init__(self, tables: list[DbtModelTable], upper_case: bool) -> None:
        self.upper_case = upper_case
        self.tables = tables

    @classmethod
    def from_cloud(
        cls,
        dbt_conn: DbtConnection,
        run_id: str,
        upper_case: bool,
        all_model_ids: list[str],
        path: Union[str, Path] = DBT_TARGET_DIR,
    ) -> "DbtModelTables":
        path = path if isinstance(path, Path) else Path(path)
        dbt_conn.download_manifest(run_id=run_id, path=path)
        with open(path / "manifest.json") as fp:
            dbt_catalog = json.load(fp)
        tables = cls.read_dbt_models(dbt_catalog, upper_case, all_model_ids)
        return cls(tables, upper_case)

    @classmethod
    def from_local(
        cls, upper_case: bool, all_model_ids: list[str], manifest_path: Union[str, Path] = DBT_PATH_TO_MANIFEST
    ) -> "DbtModelTables":
        with open(manifest_path) as fp:
            dbt_catalog = json.load(fp)
        tables = cls.read_dbt_models(dbt_catalog, upper_case, all_model_ids)
        return cls(tables, upper_case)

    @staticmethod
    def read_dbt_models(dbt_catalog: dict, upper_case: bool, all_model_ids: list[str]) -> list[DbtModelTable]:
        tables = []
        for model_def in dbt_catalog["nodes"].values():
            model_id = safeget(model_def, ["meta", "gooddata", "model_id"])
            if model_id in all_model_ids:
                tables.append(DbtModelTable.from_dict(model_def))

        if len(tables) == 0:
            raise Exception("No tables labelled by gooddata meta flag found in the data source")

        if upper_case:
            for table in tables:
                table.upper_case_name()
                for column in table.columns.values():
                    column.upper_case_name()
                    column.meta.gooddata.upper_case_names()
        return tables

    def set_data_types(self, scan_pdm: CatalogDeclarativeTables, dry_run: bool = False) -> None:
        if dry_run:
            for table in self.tables:
                for column in table.columns.values():
                    column.data_type = "STRING"
        else:
            for table in self.tables:
                scan_table = self.get_scan_table(scan_pdm, table.name)
                for column in table.columns.values():
                    # dbt does not provide data types in manifest.json
                    # get it from GoodData scan API
                    scan_column = self.get_scan_column(scan_table, column.name)
                    column.data_type = scan_column.data_type

    @property
    def schema_name(self) -> str:
        schemas = set([t.schema for t in self.tables if t.schema])
        if len(schemas) > 1:
            raise Exception(f"Unsupported feature: GoodData does not support multiple schemas - {schemas=}")
        elif len(schemas) < 1:
            raise Exception("No schema found")
        else:
            schema_name = next(iter(schemas))
            if self.upper_case:
                return schema_name.upper()
            else:
                return schema_name

    @staticmethod
    def get_scan_table(scan_pdm: CatalogDeclarativeTables, table_name: str) -> CatalogDeclarativeTable:
        for table in scan_pdm.tables:
            if table.id.lower() == table_name.lower():
                return table
        scan_tables = [s.id for s in scan_pdm.tables]
        raise Exception(f"get_scan_table table={table_name} not found in scan! {scan_tables=}")

    @staticmethod
    def get_scan_column(table: CatalogDeclarativeTable, column_name: str) -> CatalogDeclarativeColumn:
        for column in table.columns:
            if column.name.lower() == column_name.lower():
                return column
        scan_columns = [s.name for s in table.columns]
        raise Exception(f"get_scan_column table={table.id} column={column_name} not found in scan. {scan_columns=}")

    @staticmethod
    def get_ldm_title(column: DbtModelColumn) -> str:
        return column.description or column.name

    @staticmethod
    def is_primary_key(column: DbtModelColumn) -> bool:
        result = False
        # TODO - constraints are stored in special nodes
        # for test in column.tests:
        #     if DbtTests.PRIMARY_KEY.value in test:
        #         result = True
        if column.meta.gooddata.ldm_type == GoodDataLdmType.PRIMARY_KEY:
            result = True
        return result

    def make_grain(self, table: DbtModelTable) -> list[dict]:
        grain = [
            {"id": column.ldm_id, "type": "attribute"}
            for column in table.columns.values()
            if self.is_primary_key(column)
        ]
        return grain

    # TODO - constraints are stored in special nodes
    # @staticmethod
    # def get_dbt_foreign_key(column: DbtModelColumn) -> Optional[str]:
    #     referenced_object_id = None
    #     if column.meta.gooddata.ldm_type == GoodDataLdmType.REFERENCE:
    #         referenced_object_id = column.meta.gooddata.gooddata_ref_table_ldm_id
    #     else:
    #         for test in column.tests:
    #             if DbtTests.FOREIGN_KEY.value in test:
    #                 referenced_object_id = test[DbtTests.FOREIGN_KEY.value][DbtTests.FOREIGN_KEY_REF.value]
    #     return referenced_object_id

    @staticmethod
    def find_role_playing_tables(tables: list[DbtModelTable]) -> dict:
        return {
            referenced_object_id: columns
            for table in tables
            for column in table.columns.values()
            if column.is_reference()
            for referenced_table in [column.meta.gooddata.referenced_table]
            if referenced_table is not None
            for referenced_object_id, columns in {
                referenced_table: [
                    col.name
                    for col in table.columns.values()
                    if col.is_reference() and col.meta.gooddata.referenced_table == referenced_table
                ]
            }.items()
            if len(columns) > 1
        }

    def make_references(self, table: DbtModelTable, role_playing_tables: dict) -> list[dict]:
        references = []
        for column in table.columns.values():
            referenced_object_id = None
            if column.is_reference():
                referenced_object_id = column.meta.gooddata.gooddata_ref_table_ldm_id
                referenced_object_name = referenced_object_id
                if referenced_object_name is not None:
                    if self.upper_case:
                        referenced_object_name = referenced_object_name.upper()
                    if referenced_object_name in role_playing_tables:
                        referenced_object_id = f"{referenced_object_id}_{column.ldm_id}"
            elif column.is_date():
                referenced_object_id = column.ldm_id
            if referenced_object_id is not None:
                references.append(
                    {
                        "identifier": {"id": referenced_object_id, "type": "dataset"},
                        "multivalue": False,
                        "source_columns": [column.name],
                        "source_column_data_types": [column.data_type],
                    }
                )
        return references

    @staticmethod
    def make_facts(table: DbtModelTable) -> list[dict]:
        facts = [
            {
                "id": column.ldm_id,
                # TODO - all titles filled from dbt descriptions, incorrect! No title in dbt models.
                "title": column.gooddata_ldm_title,
                "description": column.gooddata_ldm_description,
                "source_column": column.name,
                "source_column_data_type": column.data_type,
                "tags": [table.gooddata_ldm_title] + column.tags,
            }
            for column in table.columns.values()
            if column.gooddata_is_fact()
        ]
        return facts

    @staticmethod
    def make_labels(table: DbtModelTable, attribute_column: DbtModelColumn) -> tuple[list[dict], Optional[dict]]:
        labels = []
        default_view = None
        for column in table.columns.values():
            if column.gooddata_is_label(attribute_column.name):
                labels.append(
                    {
                        "id": column.ldm_id,
                        "title": column.gooddata_ldm_title,
                        "description": column.gooddata_ldm_description,
                        "source_column": column.name,
                        "source_column_data_type": column.data_type,
                        "value_type": column.label_type,
                        "tags": [table.gooddata_ldm_title] + column.tags,
                    }
                )
                if column.meta.gooddata.default_view:
                    default_view = {
                        "id": column.ldm_id,
                        "type": "label",
                    }
        return labels, default_view

    def make_attributes(self, table: DbtModelTable) -> list[dict]:
        attributes = []
        for column in table.columns.values():
            # Default is attribute
            if column.gooddata_is_attribute():
                labels, default_view = self.make_labels(table, column)
                attributes.append(
                    {
                        "id": column.ldm_id,
                        "title": column.gooddata_ldm_title,
                        "description": column.gooddata_ldm_description,
                        "source_column": column.name,
                        "source_column_data_type": column.data_type,
                        "tags": [table.gooddata_ldm_title] + column.tags,
                        "labels": labels,
                        "sort_column": column.meta.gooddata.sort_column,
                        "sort_direction": column.sort_direction,
                        "default_view": default_view,
                    }
                )
        return attributes

    @staticmethod
    def make_date_datasets(table: DbtModelTable, existing_date_datasets: list[dict]) -> list[dict]:
        date_datasets = []
        for column in table.columns.values():
            existing_dataset_ids = [d["id"] for d in existing_date_datasets]
            if column.is_date() and column.gooddata_ldm_id not in existing_dataset_ids:
                if column.data_type in TIMESTAMP_DATA_TYPES:
                    granularities = DATE_GRANULARITIES + TIMESTAMP_GRANULARITIES
                else:
                    granularities = DATE_GRANULARITIES
                date_datasets.append(
                    {
                        "id": column.ldm_id,
                        "title": column.gooddata_ldm_title,
                        "description": column.description,
                        # Put them all to a dedicated tag(folder).
                        # Date dims are not put to the corresponding folder in our Analytical Designer.
                        # Also, the same date dim can be created from multiple columns (shared date dims).
                        # So the tagging is useless here now, we should think about it in the future.
                        "tags": ["Date dimensions"],
                        "granularities": granularities,
                        "granularities_formatting": {
                            "title_base": "",
                            "title_pattern": "%titleBase - %granularityTitle",
                        },
                    }
                )
        return date_datasets

    def make_dataset(self, data_source_id: str, table: DbtModelTable, role_playing_tables: dict, result: dict) -> dict:
        grain = self.make_grain(table)
        references = self.make_references(table, role_playing_tables)
        facts = self.make_facts(table)
        attributes = self.make_attributes(table)

        result["datasets"].append(
            {
                "id": table.gooddata_ldm_id,
                "title": table.gooddata_ldm_title,
                "description": table.description,
                "tags": [table.gooddata_ldm_title] + table.tags,
                "data_source_table_id": {
                    "data_source_id": data_source_id,
                    # TODO - add support for multiple schemas
                    #  would have to be reflected in LDM IDs too
                    "id": table.name,
                    "path": [self.schema_name, table.name],
                    "type": "dataSource",
                },
                "grain": grain,
                "references": references,
                "facts": facts,
                "attributes": attributes,
            }
        )

        date_datasets = self.make_date_datasets(table, result["date_instances"])
        result["date_instances"] = result["date_instances"] + date_datasets
        return result

    @staticmethod
    def populate_role_playing_tables(tables: list[DbtModelTable], role_playing_tables: dict) -> list[DbtModelTable]:
        result = []
        for table in tables:
            if table.name in role_playing_tables:
                for role_column in role_playing_tables[table.name]:
                    new_table = copy.deepcopy(table)
                    new_table.role_name = role_column
                    for column in new_table.columns.values():
                        column.role_name = role_column
                    result.append(new_table)
            else:
                result.append(table)
        return result

    def make_declarative_datasets(self, data_source_id: str, model_ids: Optional[list[str]]) -> dict:
        result: dict[str, list] = {"datasets": [], "date_instances": []}
        model_tables = [t for t in self.tables if not model_ids or t.meta.gooddata.model_id in model_ids]
        role_playing_tables = self.find_role_playing_tables(model_tables)
        model_tables_with_roles = self.populate_role_playing_tables(model_tables, role_playing_tables)

        for table in model_tables_with_roles:
            result = self.make_dataset(data_source_id, table, role_playing_tables, result)
        return result

    def get_entity_type(self, table_name: str, column_name: str) -> Optional[str]:
        comp_table_name = table_name
        if self.upper_case:
            comp_table_name = table_name.upper()
        comp_column_name = column_name
        if self.upper_case:
            comp_column_name = column_name.upper()
        for table in self.tables:
            if table.name == comp_table_name:
                for column in table.columns.values():
                    if column.name == comp_column_name:
                        return column.ldm_type
        return None
