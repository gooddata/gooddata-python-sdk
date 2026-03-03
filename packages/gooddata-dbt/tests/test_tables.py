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

    assert ldm.ldm is not None
    assert len(ldm.ldm.datasets) == 4
    assert len(ldm.ldm.date_instances) == 4


FAA_MODEL_ID = "faa"


def test_make_ldm_geo_area():
    """Test that GEO_AREA label type is parsed and included in the LDM."""
    tables = DbtModelTables.from_local(upper_case=False, all_model_ids=[FAA_MODEL_ID], manifest_path=_MANIFEST_PATH)
    scan_pdm = CatalogDeclarativeTables.load_from_disk(_PDM_PATH)
    tables.set_data_types(scan_pdm)
    data_source_id = "postgres"

    declarative_datasets = tables.make_declarative_datasets(data_source_id, [FAA_MODEL_ID])
    ldm = CatalogDeclarativeModel.from_dict({"ldm": declarative_datasets}, camel_case=False)

    assert ldm.ldm is not None
    # airports is referenced twice (origin/destination), find either one
    airports = [ds for ds in ldm.ldm.datasets if ds.id == "airports_origin"]
    assert len(airports) == 1
    airports_ds = airports[0]
    # Find the code attribute (which has geo labels)
    code_attrs = [a for a in airports_ds.attributes if a.id == "code_origin"]
    assert len(code_attrs) == 1
    labels = code_attrs[0].labels
    label_types = {label.id: label.value_type for label in labels}
    assert label_types["latitude_origin"] == "GEO_LATITUDE"
    assert label_types["longitude_origin"] == "GEO_LONGITUDE"
    assert label_types["country_origin"] == "GEO_AREA"
