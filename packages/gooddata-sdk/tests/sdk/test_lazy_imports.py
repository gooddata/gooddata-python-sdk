# (C) 2025 GoodData Corporation
"""Guards for the lazy import layout of ``gooddata_sdk``.

``gooddata_sdk/__init__.py`` re-exports its public API lazily (PEP 562) and the SDK imports
individual generated model/API modules instead of the ``gooddata_api_client.models`` and
``gooddata_api_client.apis`` aggregates. Both are easy to undo by accident with a single
convenience import, so they are asserted here.
"""

import subprocess
import sys
from pathlib import Path

import gooddata_sdk
import pytest
from gooddata_sdk import _apis, _models

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_all_lazy_exports_resolve():
    """Catches a stale module path -- the strings are data, so a moved module fails only here."""
    for name in gooddata_sdk.__all__:
        assert getattr(gooddata_sdk, name) is not None, name


def test_lazy_import_tables_are_in_sync_with_the_type_checking_block():
    """The generated tables must match their source of truth, or a new export silently vanishes.

    ``test_all_lazy_exports_resolve`` only checks names that made it into the map; this checks
    that the map itself still matches the ``TYPE_CHECKING`` imports it is generated from.
    """
    script = REPO_ROOT / "scripts/sync_lazy_imports.py"
    result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_unknown_attribute_raises_attribute_error():
    with pytest.raises(AttributeError):
        gooddata_sdk.ThisDoesNotExist


@pytest.mark.parametrize(
    "expression",
    [
        "gooddata_sdk.utils",
        "gooddata_sdk.sdk",
        "gooddata_sdk.catalog",
        "gooddata_sdk.catalog.workspace",
        "gooddata_sdk.catalog.workspace.entity_model",
        "gooddata_sdk.compute",
        "gooddata_sdk.compute.model",
        "gooddata_sdk.compute.model.filter",
        "gooddata_sdk.visualization",
        "gooddata_sdk.table",
    ],
)
def test_submodules_are_still_reachable_as_attributes(expression):
    """``import gooddata_sdk`` used to populate the whole tree; attribute access must still work.

    Each expression runs in a fresh interpreter on purpose -- sharing one would let an earlier
    expression import the tree and mask a missing lazy hook in a subpackage.
    """
    subprocess.run([sys.executable, "-c", f"import gooddata_sdk\n{expression}\n"], check=True)


def test_missing_dependency_inside_a_submodule_is_not_masked_as_attribute_error():
    """A broken submodule must keep its ModuleNotFoundError, not look like a typo."""
    code = (
        "import sys, types\n"
        "import gooddata_sdk\n"
        "broken = types.ModuleType('gooddata_sdk.catalog.broken')\n"
        "class Finder:\n"
        "    def find_spec(self, name, path=None, target=None):\n"
        "        if name == 'gooddata_sdk.catalog.broken':\n"
        "            raise ModuleNotFoundError('No module named nonexistent_dep',"
        " name='nonexistent_dep')\n"
        "        return None\n"
        "sys.meta_path.insert(0, Finder())\n"
        "try:\n"
        "    gooddata_sdk.catalog.broken\n"
        "except ModuleNotFoundError as e:\n"
        "    assert e.name == 'nonexistent_dep', e.name\n"
        "else:\n"
        "    raise AssertionError('ModuleNotFoundError was swallowed')\n"
    )
    subprocess.run([sys.executable, "-c", code], check=True)


@pytest.mark.parametrize(
    "statement",
    [
        "import gooddata_sdk",
        "from gooddata_sdk import GoodDataSdk",
        "from gooddata_sdk.visualization import Visualization",
    ],
)
def test_aggregate_api_client_modules_are_not_imported(statement):
    """The aggregates import ~1400 model classes / ~130 API classes; the SDK needs a few dozen."""
    code = (
        f"{statement}\n"
        "import sys\n"
        "assert 'gooddata_api_client.models' not in sys.modules, 'models aggregate imported'\n"
        "assert 'gooddata_api_client.apis' not in sys.modules, 'apis aggregate imported'\n"
    )
    subprocess.run([sys.executable, "-c", code], check=True)


def test_importing_gooddata_sdk_does_not_import_the_whole_sdk():
    code = (
        "import sys\n"
        "import gooddata_sdk\n"
        "assert 'gooddata_sdk.sdk' not in sys.modules, 'gooddata_sdk.sdk imported eagerly'\n"
    )
    subprocess.run([sys.executable, "-c", code], check=True)


def test_reexport_modules_expose_exactly_their_all():
    for module in (_models, _apis):
        for name in module.__all__:
            assert hasattr(module, name), f"{module.__name__}.{name}"
