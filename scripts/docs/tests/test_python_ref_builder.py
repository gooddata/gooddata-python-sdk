# (C) 2026 GoodData Corporation
from __future__ import annotations

import sys
from pathlib import Path

import pytest

# The scripts/docs directory is not a package — add it to sys.path so we can import.
# The module also reads *_template.md at import time from cwd, so we chdir into docs/.
_SCRIPTS_DOCS = Path(__file__).resolve().parent.parent
_DOCS_DIR = _SCRIPTS_DOCS.parent.parent / "docs"


@pytest.fixture(autouse=True)
def _chdir_to_docs(monkeypatch: pytest.MonkeyPatch) -> None:
    """python_ref_builder reads template files relative to cwd at import time."""
    monkeypatch.chdir(_DOCS_DIR)
    if str(_SCRIPTS_DOCS) not in sys.path:
        monkeypatch.syspath_prepend(str(_SCRIPTS_DOCS))


@pytest.fixture()
def _mod():
    """Lazily import the module (after cwd/syspath are set)."""
    import python_ref_builder as mod

    return mod


# ---------------------------------------------------------------------------
# Sample data fixtures (mimic json_builder.py output structure)
# ---------------------------------------------------------------------------

SAMPLE_LINKS: dict[str, dict] = {
    "CatalogWorkspace": {"path": "/latest/api-reference/catalogworkspace", "kind": "class"},
    "CatalogDataSource": {"path": "/latest/api-reference/catalogdatasource", "kind": "class"},
    "some_util": {"path": "/latest/api-reference/some_util", "kind": "function"},
    "Insight": {"path": "/latest/api-reference/insight", "kind": "class"},
}

SAMPLE_FUNCTION_DATA: dict = {
    "kind": "function",
    "docstring": "List all workspaces.",
    "signature": {
        "params": [("workspace_id", "str"), ("name", "str")],
        "return_annotation": "list[CatalogWorkspace]",
    },
    "docstring_parsed": {
        "short_description": "Return a `CatalogWorkspace` list.",
        "long_description": "Fetches all workspaces from the server.",
        "params": [
            {"arg_name": "workspace_id", "type_name": "str", "description": "The workspace ID."},
            {"arg_name": "name", "type_name": "Optional[str]", "description": "Optional filter."},
        ],
        "returns": {
            "type_name": "list[CatalogWorkspace]",
            "description": "All matching `CatalogWorkspace` objects.",
        },
    },
}

SAMPLE_PROPERTY_DATA: dict = {
    "kind": "function",
    "is_property": True,
    "docstring": "The workspace name.",
    "signature": {"params": [], "return_annotation": "str"},
    "docstring_parsed": {
        "short_description": "The workspace name.",
        "long_description": "",
        "params": [],
        "returns": None,
    },
}

SAMPLE_CLASS_DATA: dict = {
    "kind": "class",
    "docstring": "Represents a workspace.",
    "docstring_parsed": {
        "short_description": "A catalog workspace object.",
        "long_description": "",
    },
    "functions": {
        "list_workspaces": SAMPLE_FUNCTION_DATA,
        "name": SAMPLE_PROPERTY_DATA,
        "_private": {"kind": "function"},
    },
}

SAMPLE_MODULE_DATA: dict = {
    "kind": "module",
    "CatalogWorkspace": {"kind": "class"},
    "some_util": {"kind": "function"},
}


# ===================================================================
# LinkResolver
# ===================================================================


class TestLinkResolver:
    def test_type_link_known_type(self, _mod):
        resolver = _mod.LinkResolver(SAMPLE_LINKS)
        result = resolver.type_link("CatalogWorkspace")
        assert result == '<a href="/latest/api-reference/catalogworkspace/">CatalogWorkspace</a>'

    def test_type_link_unknown_type(self, _mod):
        resolver = _mod.LinkResolver(SAMPLE_LINKS)
        assert resolver.type_link("UnknownType") == "UnknownType"

    def test_type_link_empty(self, _mod):
        resolver = _mod.LinkResolver(SAMPLE_LINKS)
        assert resolver.type_link("") == ""

    def test_type_link_none(self, _mod):
        resolver = _mod.LinkResolver(SAMPLE_LINKS)
        assert resolver.type_link(None) == ""

    def test_type_link_optional_wrapper(self, _mod):
        resolver = _mod.LinkResolver(SAMPLE_LINKS)
        result = resolver.type_link("Optional[CatalogWorkspace]")
        assert "Optional[" in result
        assert '<a href="/latest/api-reference/catalogworkspace/">CatalogWorkspace</a>' in result

    def test_type_link_list_wrapper(self, _mod):
        resolver = _mod.LinkResolver(SAMPLE_LINKS)
        result = resolver.type_link("list[CatalogWorkspace]")
        assert "list[" in result
        assert '<a href="/latest/api-reference/catalogworkspace/">CatalogWorkspace</a>' in result

    def test_all_links_backtick_name_without_underscore(self, _mod):
        resolver = _mod.LinkResolver(SAMPLE_LINKS)
        result = resolver.all_links("Returns a `CatalogWorkspace` object.")
        assert '<a href="/latest/api-reference/catalogworkspace/">CatalogWorkspace</a>' in result
        # Backticks around a resolved link should be stripped
        assert "`CatalogWorkspace`" not in result

    def test_all_links_name_with_underscore_in_backticks(self, _mod):
        resolver = _mod.LinkResolver(SAMPLE_LINKS)
        result = resolver.all_links("Call `some_util` for help.")
        assert '<a href="/latest/api-reference/some_util/">some_util</a>' in result

    def test_all_links_name_with_underscore_after_space(self, _mod):
        resolver = _mod.LinkResolver(SAMPLE_LINKS)
        result = resolver.all_links("Use some_util here.")
        assert '<a href="/latest/api-reference/some_util/">some_util</a>' in result

    def test_all_links_empty(self, _mod):
        resolver = _mod.LinkResolver(SAMPLE_LINKS)
        assert resolver.all_links("") == ""

    def test_all_links_none(self, _mod):
        resolver = _mod.LinkResolver(SAMPLE_LINKS)
        assert resolver.all_links(None) == ""

    def test_all_links_no_matches(self, _mod):
        resolver = _mod.LinkResolver(SAMPLE_LINKS)
        text = "Plain text with no type names."
        assert resolver.all_links(text) == text

    def test_all_links_multiple_names(self, _mod):
        resolver = _mod.LinkResolver(SAMPLE_LINKS)
        result = resolver.all_links("Returns `CatalogWorkspace` or `Insight`.")
        assert "catalogworkspace" in result
        assert "insight" in result


# ===================================================================
# TemplateReplacementSpec
# ===================================================================


class TestTemplateReplacementSpec:
    def test_render_replaces_all_tokens(self, _mod):
        spec = _mod.TemplateReplacementSpec(parent="sdk", name="MyClass", link="MyClass", content="<div>hello</div>")
        template = "PARENT.NAME (LINK)\nCONTENT"
        result = spec.render_template_to_str(template)
        assert result == "sdk.MyClass (MyClass)\n<div>hello</div>"

    def test_render_skips_none_tokens(self, _mod):
        spec = _mod.TemplateReplacementSpec(name="Foo")
        template = "PARENT.NAME"
        result = spec.render_template_to_str(template)
        # PARENT is None so left as-is
        assert result == "PARENT.Foo"


# ===================================================================
# _function_signature
# ===================================================================


class TestFunctionSignature:
    def test_with_docstring_params(self, _mod):
        result = _mod._function_signature(SAMPLE_FUNCTION_DATA)
        assert result == "workspace_id: str, name: Optional[str]"

    def test_without_docstring(self, _mod):
        data: dict = {"kind": "function", "signature": {"params": []}}
        assert _mod._function_signature(data) == ""

    def test_empty_params(self, _mod):
        data: dict = {"kind": "function", "docstring_parsed": {"params": []}}
        assert _mod._function_signature(data) == ""


# ===================================================================
# _object_partial_context
# ===================================================================


class TestObjectPartialContext:
    def test_function_context(self, _mod):
        resolver = _mod.LinkResolver(SAMPLE_LINKS)
        ctx = _mod._object_partial_context(SAMPLE_FUNCTION_DATA, ["sdk", "list_workspaces"], resolver)
        assert ctx["kind"] == "function"
        assert ctx["name"] == "list_workspaces"
        assert ctx["is_property"] is False
        assert "params" in ctx
        assert len(ctx["params"]) == 2
        assert isinstance(ctx["returns"], dict)
        assert ctx["returns"]["type"]  # should have a rendered link

    def test_property_context(self, _mod):
        resolver = _mod.LinkResolver(SAMPLE_LINKS)
        ctx = _mod._object_partial_context(SAMPLE_PROPERTY_DATA, ["CatalogWorkspace", "name"], resolver)
        assert ctx["is_property"] is True
        assert ctx["returns"] == "no_docs"

    def test_class_context(self, _mod):
        resolver = _mod.LinkResolver(SAMPLE_LINKS)
        ctx = _mod._object_partial_context(SAMPLE_CLASS_DATA, ["sdk", "CatalogWorkspace"], resolver)
        assert ctx["kind"] == "class"
        assert ctx["parent_name"] == "sdk"
        assert ctx["class_name"] == "CatalogWorkspace"
        assert ctx["docstring"] is True

    def test_class_context_no_docstring(self, _mod):
        resolver = _mod.LinkResolver(SAMPLE_LINKS)
        data: dict = {"kind": "class"}
        ctx = _mod._object_partial_context(data, ["mod", "Empty"], resolver)
        assert ctx["docstring"] is False


# ===================================================================
# HTML rendering functions
# ===================================================================


class TestRenderFunctionHtml:
    def test_produces_html(self, _mod):
        resolver = _mod.LinkResolver(SAMPLE_LINKS)
        html = _mod.render_function_html(SAMPLE_FUNCTION_DATA, "sdk.list_workspaces", resolver)
        assert '<div class="python-ref">' in html
        assert "list_workspaces" in html
        assert "Parameters" in html

    def test_property_no_parameters(self, _mod):
        resolver = _mod.LinkResolver(SAMPLE_LINKS)
        html = _mod.render_function_html(SAMPLE_PROPERTY_DATA, "CatalogWorkspace.name", resolver)
        assert "name" in html
        # Properties should not show a Parameters section
        assert "Parameters" not in html


class TestRenderClassHtml:
    def test_produces_html_with_methods_and_properties(self, _mod):
        resolver = _mod.LinkResolver(SAMPLE_LINKS)
        html = _mod.render_class_html(SAMPLE_CLASS_DATA, "sdk", "sdk.CatalogWorkspace", resolver)
        assert '<div class="python-ref">' in html
        assert "Properties" in html
        assert "Methods" in html
        # Private method should be excluded
        assert "_private" not in html

    def test_class_no_functions(self, _mod):
        resolver = _mod.LinkResolver(SAMPLE_LINKS)
        data: dict = {"kind": "class", "functions": {}}
        html = _mod.render_class_html(data, "sdk", "sdk.Empty", resolver)
        assert "Properties" in html
        assert "<i> None </i>" in html


class TestRenderModuleHtml:
    def test_produces_table(self, _mod):
        resolver = _mod.LinkResolver(SAMPLE_LINKS)
        html = _mod.render_module_html(SAMPLE_MODULE_DATA, resolver)
        assert '<div class="python-api-ref">' in html
        assert "class" in html
        assert "function" in html

    def test_skips_kind_key(self, _mod):
        resolver = _mod.LinkResolver(SAMPLE_LINKS)
        html = _mod.render_module_html(SAMPLE_MODULE_DATA, resolver)
        # The "kind" key on the module dict itself should not appear as an entry
        # 1 header row + 2 data rows = 3
        assert html.count("<tr>") == 3


# ===================================================================
# change_json_root
# ===================================================================


class TestChangeJsonRoot:
    def test_none_paths_returns_original(self, _mod):
        data = {"a": 1}
        assert _mod.change_json_root(data, None) is data

    def test_single_path(self, _mod):
        data = {"sdk": {"catalog": {"kind": "module"}}}
        result = _mod.change_json_root(data, ["sdk.catalog"])
        assert result == {"catalog": {"kind": "module"}}

    def test_multiple_paths(self, _mod):
        data = {
            "sdk": {"kind": "module", "cls": {"kind": "class"}},
            "pandas": {"kind": "module"},
        }
        result = _mod.change_json_root(data, ["sdk", "pandas"])
        assert "sdk" in result
        assert "pandas" in result


# ===================================================================
# create_file_structure (integration — uses tmp_path)
# ===================================================================


class TestCreateFileStructure:
    def test_creates_module_class_and_function_files(self, _mod, tmp_path):
        data = {
            "mymodule": {
                "kind": "module",
                "MyClass": {
                    "kind": "class",
                    "docstring": "A class.",
                    "docstring_parsed": {
                        "short_description": "A class.",
                        "long_description": "",
                    },
                    "functions": {
                        "do_stuff": {
                            "kind": "function",
                            "docstring": "Do stuff.",
                            "signature": {
                                "params": [],
                                "return_annotation": "None",
                            },
                            "docstring_parsed": {
                                "short_description": "Do stuff.",
                                "long_description": "",
                                "params": [],
                                "returns": None,
                            },
                        },
                        "_hidden": {"kind": "function"},
                    },
                },
            },
        }
        _mod.create_file_structure(data, tmp_path, "/latest/api-reference")

        # Module index
        module_index = tmp_path / "mymodule" / "_index.md"
        assert module_index.exists()
        content = module_index.read_text()
        assert "mymodule" in content

        # Class index
        class_index = tmp_path / "mymodule" / "MyClass" / "_index.md"
        assert class_index.exists()
        content = class_index.read_text()
        assert "MyClass" in content
        assert "python-ref" in content

        # Function page
        func_page = tmp_path / "mymodule" / "MyClass" / "do_stuff.md"
        assert func_page.exists()
        content = func_page.read_text()
        assert "do_stuff" in content

        # Private function should be skipped
        assert not (tmp_path / "mymodule" / "MyClass" / "_hidden.md").exists()

    def test_duplicate_names_skipped(self, _mod, tmp_path):
        data = {
            "mod1": {
                "kind": "module",
                "Shared": {"kind": "class", "functions": {}},
            },
            "mod2": {
                "kind": "module",
                "Shared": {"kind": "class", "functions": {}},
            },
        }
        # Should not raise — second "Shared" is skipped
        _mod.create_file_structure(data, tmp_path, "/latest/api-reference")
        assert (tmp_path / "mod1" / "Shared" / "_index.md").exists()
