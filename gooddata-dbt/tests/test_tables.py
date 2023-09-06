# (C) 2023 GoodData Corporation
import json
from pathlib import Path
from typing import Dict, Union

from gooddata_dbt.dbt.tables import DbtModelTables

_CURR_DIR = Path(__file__).parent
_MANIFEST_PATH = _CURR_DIR / "resources/dbt_target/manifest.json"


def _read_json(path: Union[str, Path]) -> Dict:
    with open(path, "r") as f:
        return json.load(f)


def test_load_tables():
    tables = DbtModelTables.from_local(upper_case=False, all_model_ids=["github"], manifest_path=_MANIFEST_PATH)

    assert len(tables.tables) == 5
    assert len(tables.tables[0].columns) == 4

    assert tables.tables[0].name == "exchange_rate"
    assert tables.tables[0].columns["created_at"].name == "created_at"


def test_load_tables_upper_case():
    tables = DbtModelTables.from_local(upper_case=True, all_model_ids=["github"], manifest_path=_MANIFEST_PATH)

    assert len(tables.tables) == 5
    assert len(tables.tables[0].columns) == 4

    assert tables.tables[0].name == "EXCHANGE_RATE"
    assert tables.tables[0].columns["created_at"].name == "CREATED_AT"
