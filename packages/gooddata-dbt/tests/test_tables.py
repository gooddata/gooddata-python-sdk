# (C) 2023 GoodData Corporation
import json
from pathlib import Path
from typing import Union

from gooddata_dbt.dbt.tables import DbtModelTables
from gooddata_sdk import CatalogDeclarativeModel, CatalogDeclarativeTables

_CURR_DIR = Path(__file__).parent
_MANIFEST_PATH = _CURR_DIR / "resources/dbt_target/manifest.json"
_PDM_PATH = _CURR_DIR / "resources/gooddata_layouts"
MODEL_ID = "github"


def _read_json(path: Union[str, Path]) -> dict:
    with open(path) as f:
        return json.load(f)


def test_load_tables():
    tables = DbtModelTables.from_local(upper_case=False, all_model_ids=[MODEL_ID], manifest_path=_MANIFEST_PATH)

    assert len(tables.tables) == 4
    assert len(tables.tables[0].columns) == 6

    assert tables.tables[0].name == "commits"
    assert tables.tables[0].columns["created_at"].name == "created_at"


def test_load_tables_upper_case():
    tables = DbtModelTables.from_local(upper_case=True, all_model_ids=[MODEL_ID], manifest_path=_MANIFEST_PATH)

    assert len(tables.tables) == 4
    assert len(tables.tables[0].columns) == 6

    assert tables.tables[0].name == "COMMITS"
    assert tables.tables[0].columns["created_at"].name == "CREATED_AT"


def test_make_ldm():
    tables = DbtModelTables.from_local(upper_case=False, all_model_ids=[MODEL_ID], manifest_path=_MANIFEST_PATH)
    scan_pdm = CatalogDeclarativeTables.load_from_disk(_PDM_PATH)
    tables.set_data_types(scan_pdm)
    data_source_id = "postgres"

    declarative_datasets = tables.make_declarative_datasets(data_source_id, [MODEL_ID])
    ldm = CatalogDeclarativeModel.from_dict({"ldm": declarative_datasets}, camel_case=False)

    assert len(ldm.ldm.datasets) == 4
    assert len(ldm.ldm.date_instances) == 4
