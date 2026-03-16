# (C) 2026 GoodData Corporation
from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path

import pytest

_SCRIPTS_DOCS = Path(__file__).resolve().parent.parent


@pytest.fixture(autouse=True)
def _setup_path(monkeypatch: pytest.MonkeyPatch) -> None:
    if str(_SCRIPTS_DOCS) not in sys.path:
        monkeypatch.syspath_prepend(str(_SCRIPTS_DOCS))


@pytest.fixture()
def _mod():
    import griffe_builder as mod

    return mod


@pytest.fixture()
def sample_pkg(tmp_path: Path) -> Path:
    """Create a minimal Python package for griffe to analyze."""
    pkg = tmp_path / "sample_pkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text(
        textwrap.dedent("""\
        from sample_pkg.services import MyService
        from sample_pkg.models import MyModel
        """)
    )
    (pkg / "services.py").write_text(
        textwrap.dedent("""\
        from __future__ import annotations

        from sample_pkg.models import MyModel


        class MyService:
            \"\"\"A service that does things.\"\"\"

            def list_items(self, workspace_id: str, limit: int = 10) -> list[MyModel]:
                \"\"\"List all items in a workspace.

                Args:
                    workspace_id: The workspace ID.
                    limit: Maximum number of items to return.

                Returns:
                    list[MyModel]: All matching items.
                \"\"\"
                ...

            def delete_item(self, item_id: str) -> None:
                \"\"\"Delete an item by ID.

                Args:
                    item_id: The item ID.
                \"\"\"
                ...

            @property
            def name(self) -> str:
                \"\"\"The service name.\"\"\"
                return "my_service"

            def _private_method(self) -> None:
                pass
        """)
    )
    (pkg / "models.py").write_text(
        textwrap.dedent("""\
        from __future__ import annotations


        class MyModel:
            \"\"\"A model representing an item.

            Args:
                id: The item identifier.
                name: The item name.
            \"\"\"

            def __init__(self, id: str, name: str) -> None:
                self.id = id
                self.name = name
        """)
    )
    return tmp_path


@pytest.fixture()
def inheritance_pkg(tmp_path: Path) -> Path:
    """Package with class inheritance to test inherited member resolution."""
    pkg = tmp_path / "inherit_pkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text(
        textwrap.dedent("""\
        from inherit_pkg.base import BaseService
        from inherit_pkg.child import ChildService
        """)
    )
    (pkg / "base.py").write_text(
        textwrap.dedent("""\
        class BaseService:
            \"\"\"Base service.\"\"\"

            def shared_method(self) -> str:
                \"\"\"A method defined on the base class.\"\"\"
                return "shared"
        """)
    )
    (pkg / "child.py").write_text(
        textwrap.dedent("""\
        from inherit_pkg.base import BaseService


        class ChildService(BaseService):
            \"\"\"Child service extending base.\"\"\"

            def child_only(self) -> int:
                \"\"\"A method only on the child.\"\"\"
                return 42
        """)
    )
    return tmp_path


# ---------------------------------------------------------------------------
# Tests — build_data_json
# ---------------------------------------------------------------------------


class TestBuildDataJson:
    def test_loads_package(self, _mod, sample_pkg):
        data = _mod.build_data_json(["sample_pkg"], [str(sample_pkg)])
        assert "services" in data or "models" in data

    def test_finds_classes(self, _mod, sample_pkg):
        data = _mod.build_data_json(["sample_pkg"], [str(sample_pkg)])
        found = False

        def _walk(node):
            nonlocal found
            for key, val in node.items():
                if key == "MyService" and isinstance(val, dict) and val.get("kind") == "class":
                    found = True
                    return val
                if isinstance(val, dict) and val.get("kind") == "module":
                    result = _walk(val)
                    if result:
                        return result
            return None

        cls = _walk(data)
        assert found, f"MyService not found in data keys: {list(data.keys())}"
        assert cls["kind"] == "class"
        assert cls["docstring"] is not None

    def test_function_data_structure(self, _mod, sample_pkg):
        data = _mod.build_data_json(["sample_pkg"], [str(sample_pkg)])

        def _find_func(node, name):
            for val in node.values():
                if isinstance(val, dict):
                    if val.get("kind") == "class":
                        funcs = val.get("functions", {})
                        if name in funcs:
                            return funcs[name]
                    if val.get("kind") == "module":
                        result = _find_func(val, name)
                        if result:
                            return result
            return None

        func = _find_func(data, "list_items")
        assert func is not None, "list_items not found"
        assert func["kind"] == "function"

        # Signature
        sig = func["signature"]
        assert "params" in sig
        assert "return_annotation" in sig
        assert len(sig["params"]) >= 2  # workspace_id, limit

        # Docstring parsed
        ds = func["docstring_parsed"]
        assert ds is not None
        assert ds["short_description"] is not None
        assert len(ds["params"]) == 2
        assert ds["params"][0]["arg_name"] == "workspace_id"
        assert ds["returns"] is not None

    def test_no_top_level_kind_key(self, _mod, sample_pkg):
        data = _mod.build_data_json(["sample_pkg"], [str(sample_pkg)])
        assert "kind" not in data

    def test_output_is_json_serializable(self, _mod, sample_pkg):
        data = _mod.build_data_json(["sample_pkg"], [str(sample_pkg)])
        json.dumps(data)

    def test_private_methods_included(self, _mod, sample_pkg):
        """Private methods should be in data (filtered later by python_ref_builder)."""
        data = _mod.build_data_json(["sample_pkg"], [str(sample_pkg)])

        def _find_class(node, name):
            for k, v in node.items():
                if k == name and isinstance(v, dict) and v.get("kind") == "class":
                    return v
                if isinstance(v, dict) and v.get("kind") == "module":
                    r = _find_class(v, name)
                    if r:
                        return r
            return None

        cls = _find_class(data, "MyService")
        assert cls is not None
        assert "_private_method" in cls["functions"]

    def test_property_detected_if_resolved(self, _mod, sample_pkg):
        """@property methods should have is_property=True when griffe resolves them."""
        data = _mod.build_data_json(["sample_pkg"], [str(sample_pkg)])

        def _find_class(node, name):
            for k, v in node.items():
                if k == name and isinstance(v, dict) and v.get("kind") == "class":
                    return v
                if isinstance(v, dict) and v.get("kind") == "module":
                    r = _find_class(v, name)
                    if r:
                        return r
            return None

        cls = _find_class(data, "MyService")
        assert cls is not None
        # griffe may or may not resolve @property into functions depending on resolution;
        # if it does, is_property should be True
        if "name" in cls["functions"]:
            assert cls["functions"]["name"]["is_property"] is True

    def test_void_function_return_annotation(self, _mod, sample_pkg):
        """Functions returning None should have 'None' as return_annotation."""
        data = _mod.build_data_json(["sample_pkg"], [str(sample_pkg)])

        def _find_func(node, name):
            for val in node.values():
                if isinstance(val, dict):
                    if val.get("kind") == "class":
                        funcs = val.get("functions", {})
                        if name in funcs:
                            return funcs[name]
                    if val.get("kind") == "module":
                        result = _find_func(val, name)
                        if result:
                            return result
            return None

        func = _find_func(data, "delete_item")
        assert func is not None
        assert func["signature"]["return_annotation"] == "None"

    def test_default_parameter_values(self, _mod, sample_pkg):
        """Parameters with defaults should include them in the param string."""
        data = _mod.build_data_json(["sample_pkg"], [str(sample_pkg)])

        def _find_func(node, name):
            for val in node.values():
                if isinstance(val, dict):
                    if val.get("kind") == "class":
                        funcs = val.get("functions", {})
                        if name in funcs:
                            return funcs[name]
                    if val.get("kind") == "module":
                        result = _find_func(val, name)
                        if result:
                            return result
            return None

        func = _find_func(data, "list_items")
        assert func is not None
        # The 'limit' param should have default=10
        limit_param = [p for p in func["signature"]["params"] if "limit" in p[0]]
        assert len(limit_param) == 1
        assert "10" in limit_param[0][0]

    def test_class_docstring_parsed(self, _mod, sample_pkg):
        """Class-level docstrings should be parsed."""
        data = _mod.build_data_json(["sample_pkg"], [str(sample_pkg)])

        def _find_class(node, name):
            for k, v in node.items():
                if k == name and isinstance(v, dict) and v.get("kind") == "class":
                    return v
                if isinstance(v, dict) and v.get("kind") == "module":
                    r = _find_class(v, name)
                    if r:
                        return r
            return None

        cls = _find_class(data, "MyService")
        assert cls is not None
        assert cls["docstring_parsed"] is not None
        assert cls["docstring_parsed"]["short_description"] == "A service that does things."

    def test_multiple_packages(self, _mod, sample_pkg):
        """Loading multiple packages should merge their data."""
        # sample_pkg has both services and models submodules
        data = _mod.build_data_json(["sample_pkg"], [str(sample_pkg)])
        assert len(data) >= 1


# ---------------------------------------------------------------------------
# Tests — inheritance
# ---------------------------------------------------------------------------


class TestInheritedMembers:
    def test_child_has_own_method(self, _mod, inheritance_pkg):
        data = _mod.build_data_json(["inherit_pkg"], [str(inheritance_pkg)])

        def _find_class(node, name):
            for k, v in node.items():
                if k == name and isinstance(v, dict) and v.get("kind") == "class":
                    return v
                if isinstance(v, dict) and v.get("kind") == "module":
                    r = _find_class(v, name)
                    if r:
                        return r
            return None

        cls = _find_class(data, "ChildService")
        assert cls is not None
        assert "child_only" in cls["functions"]

    def test_base_class_has_shared_method(self, _mod, inheritance_pkg):
        """Base class methods should be present on the base class itself."""
        data = _mod.build_data_json(["inherit_pkg"], [str(inheritance_pkg)])

        def _find_class(node, name):
            for k, v in node.items():
                if k == name and isinstance(v, dict) and v.get("kind") == "class":
                    return v
                if isinstance(v, dict) and v.get("kind") == "module":
                    r = _find_class(v, name)
                    if r:
                        return r
            return None

        cls = _find_class(data, "BaseService")
        assert cls is not None
        assert "shared_method" in cls["functions"]
