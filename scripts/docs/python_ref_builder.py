# (C) 2023 GoodData Corporation
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import TextIO

import attr
import toml
from attr import define
from jinja2 import Environment, FileSystemLoader

_SCRIPT_DIR = Path(__file__).resolve().parent

MODULE_TEMPLATE_STRING = Path("module_template.md").read_text()
CLASS_TEMPLATE_STRING = Path("class_template.md").read_text()
FUNCTION_TEMPLATE_STRING = Path("function_template.md").read_text()

_JINJA_ENV = Environment(
    loader=FileSystemLoader(_SCRIPT_DIR / "templates"),
    autoescape=False,
    keep_trailing_newline=True,
)
_OBJECT_PARTIAL_TPL = _JINJA_ENV.get_template("object_partial.html.j2")
_FUNCTION_TPL = _JINJA_ENV.get_template("function.html.j2")
_CLASS_TPL = _JINJA_ENV.get_template("class.html.j2")
_MODULE_TPL = _JINJA_ENV.get_template("module.html.j2")


@attr.s(auto_attribs=True)
class RefHolder:
    """ """

    url: str
    packages: list[str] = attr.Factory(list)
    directory: str = ""


@define
class TemplateReplacementSpec:
    """
    Specification for replacing tokens in a template. Tokens currently in use are:
        PARENT - name of the parent object
        NAME - name of the object
        LINK - link title of the object
        CONTENT - pre-rendered HTML content
    """

    parent: None | str = None
    name: None | str = None
    link: None | str = None
    path: None | str = None
    content: None | str = None

    def render_template_to_str(self, template: str) -> str:
        """
        Replace the variables in markdown templates and return the new content string.
        """
        for token, replacement in [
            ("PARENT", self.parent),
            ("NAME", self.name),
            ("LINK", self.link),
            ("PATH", self.path),
            ("CONTENT", self.content),
        ]:
            if replacement is not None:
                template = template.replace(token, replacement)
        return template

    def render_template_to_file(self, template: str, file: TextIO):
        rendered_string = self.render_template_to_str(template)
        file.write(rendered_string)


# ---------------------------------------------------------------------------
# Link resolution (replaces Hugo link partials)
# ---------------------------------------------------------------------------


class LinkResolver:
    """Pre-compiled resolver that converts type names to HTML links.

    Builds two combined regexes (one for names containing ``_``, one for the
    rest) so that docstring link resolution is O(1) per name instead of
    O(n) iteration over all links.
    """

    def __init__(self, links: dict[str, dict]) -> None:
        self.links = links
        names_with_us: list[str] = []
        names_without_us: list[str] = []
        for name, data in links.items():
            if data.get("path"):
                if "_" in name:
                    names_with_us.append(name)
                else:
                    names_without_us.append(name)

        self._regex_with: re.Pattern[str] | None = None
        self._regex_without: re.Pattern[str] | None = None

        if names_with_us:
            alt = "|".join(re.escape(n) for n in sorted(names_with_us, key=len, reverse=True))
            # Names with _ may be surrounded by [, `, or space (left) and ], `, ., or space (right)
            self._regex_with = re.compile(rf"([\[` ])({alt})([\]`. ])")
        if names_without_us:
            alt = "|".join(re.escape(n) for n in sorted(names_without_us, key=len, reverse=True))
            # Names without _ must be inside backticks or square brackets
            self._regex_without = re.compile(rf"([\[`])({alt})([\]`])")

    def type_link(self, name: str) -> str:
        """Replicate ``api-ref-link-partial.html``: resolve a single type to a hyperlink."""
        if not name:
            return name or ""
        orig = name
        clean = name.replace("]", "").replace("Optional[", "").replace("list[", "").replace("List[", "").strip()
        data = self.links.get(clean)
        if data and data.get("path"):
            return orig.replace(clean, f'<a href="{data["path"]}/">{clean}</a>')
        return orig

    def all_links(self, text: str) -> str:
        """Replicate ``api-ref-link-all-partial.html``: linkify all known type names."""
        if not text:
            return text or ""

        def _repl(m: re.Match[str]) -> str:
            data = self.links.get(m.group(2))
            if data and data.get("path"):
                return f'{m.group(1)}<a href="{data["path"]}/">{m.group(2)}</a>{m.group(3)}'
            return m.group(0)

        result = text
        if self._regex_with:
            result = self._regex_with.sub(_repl, result)
        if self._regex_without:
            result = self._regex_without.sub(_repl, result)
        # Remove backticks around links
        return result.replace("`<a", "<a").replace("</a>`", "</a>")


# ---------------------------------------------------------------------------
# Template context builders
# ---------------------------------------------------------------------------


def _function_signature(func_data: dict) -> str:
    """Build the ``arg: type, arg: type`` parameter string."""
    ds = func_data.get("docstring_parsed")
    if ds and ds.get("params"):
        return ", ".join(f"{p['arg_name']}: {p['type_name']}" for p in ds["params"])
    return ""


def _object_partial_context(obj_data: dict, path: list[str], resolver: LinkResolver) -> dict:
    """Build the Jinja2 context dict for ``object_partial.html.j2``."""
    kind = obj_data.get("kind", "")
    ctx: dict = {"kind": kind}

    if kind == "function":
        ret_ann = obj_data.get("signature", {}).get("return_annotation", "")
        ds = obj_data.get("docstring_parsed")

        ctx["name"] = path[-1]
        ctx["is_property"] = bool(obj_data.get("is_property"))
        ctx["signature"] = _function_signature(obj_data)
        ctx["return_link"] = resolver.type_link(ret_ann)
        ctx["docstring"] = bool(ds)

        if ds:
            ctx["short_description"] = resolver.all_links(ds.get("short_description", "") or "")
            ctx["long_description"] = resolver.all_links(ds.get("long_description", "") or "")

        # Parameters
        sig_params = obj_data.get("signature", {}).get("params") or []
        doc_params = ds.get("params") if ds else None
        if doc_params and len(doc_params) > 0:
            ctx["params"] = [
                {
                    "name": p["arg_name"],
                    "type": resolver.type_link(p.get("type_name", "")),
                    "description": resolver.all_links(p.get("description", "") or ""),
                }
                for p in doc_params
            ]
        elif sig_params:
            ctx["sig_params"] = [{"name": sp[0], "type": resolver.type_link(sp[1])} for sp in sig_params]

        # Returns
        if ds:
            returns = ds.get("returns")
            if not returns:
                ctx["returns"] = "no_docs"
            elif returns.get("type_name") or ret_ann != "None":
                type_name = returns.get("type_name") or obj_data.get("signature", {}).get("return_type", "")
                description = returns.get("description", "")
                ctx["returns"] = {
                    "type": resolver.type_link(type_name),
                    "description": resolver.all_links(description) if description else "",
                }
            else:
                ctx["returns"] = "none"
        else:
            ctx["returns"] = "no_docs"

    elif kind == "class":
        ctx["parent_name"] = path[-2] if len(path) >= 2 else ""
        ctx["class_name"] = path[-1]
        ds = obj_data.get("docstring_parsed")
        ctx["docstring"] = bool(ds)
        if ds:
            ctx["short_description"] = resolver.all_links(ds.get("short_description", "") or "")
            ctx["long_description"] = resolver.all_links(ds.get("long_description", "") or "")

    return ctx


# ---------------------------------------------------------------------------
# HTML rendering via Jinja2 templates
# ---------------------------------------------------------------------------


def render_function_html(func_data: dict, import_path: str, resolver: LinkResolver) -> str:
    """Render a function page — replicates the ``api-ref`` shortcode."""
    path = import_path.split(".")
    obj_html = _OBJECT_PARTIAL_TPL.render(**_object_partial_context(func_data, path, resolver))
    return _FUNCTION_TPL.render(object_partial=obj_html)


def render_class_html(class_data: dict, parent_name: str, import_path: str, resolver: LinkResolver) -> str:
    """Render a class page — replicates the ``api-ref-class`` shortcode."""
    path = import_path.split(".")
    functions = class_data.get("functions", {})

    properties: list[dict] = []
    methods: list[dict] = []
    for fname, fdata in functions.items():
        if fname.startswith("_") or not isinstance(fdata, dict):
            continue
        fds = fdata.get("docstring_parsed")
        desc = resolver.all_links(fds.get("short_description", "")) if fds else ""
        if fdata.get("is_property"):
            properties.append({"name_link": resolver.type_link(fname), "description": desc})
        else:
            methods.append(
                {
                    "name_link": resolver.type_link(fname),
                    "signature": _function_signature(fdata),
                    "description": desc,
                }
            )

    obj_html = _OBJECT_PARTIAL_TPL.render(**_object_partial_context(class_data, path, resolver))
    return _CLASS_TPL.render(object_partial=obj_html, properties=properties, methods=methods)


def render_module_html(module_data: dict, resolver: LinkResolver) -> str:
    """Render a module page — replicates the ``api-ref-module`` shortcode."""
    entries: list[dict] = []
    for obj_name, obj_data in module_data.items():
        if obj_name == "kind" or not isinstance(obj_data, dict):
            continue
        entries.append({"kind": obj_data.get("kind", ""), "name_link": resolver.type_link(obj_name)})
    return _MODULE_TPL.render(entries=entries)


# ---------------------------------------------------------------------------
# Page spec — collected during pass 1, rendered during pass 2
# ---------------------------------------------------------------------------


@define
class _PageSpec:
    kind: str  # "module", "class", "function"
    name: str
    parent_name: str
    import_path: str
    file_path: Path
    data: dict


# ---------------------------------------------------------------------------
# File structure creation (two-pass)
# ---------------------------------------------------------------------------


def read_json_file(file_path: str) -> dict:
    """Load JSON data from a file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: Parsed JSON data.
    """
    with open(file_path) as json_file:
        return json.load(json_file)


def create_file_structure(data: dict, root: Path, url_root: str) -> dict[str, dict]:
    """Create file structure based on JSON data using a two-pass approach.

    Pass 1 — walk the data tree, build the ``links`` dict and collect page
    specs (directory structure is created here too).
    Pass 2 — render HTML for every page using the *complete* links dict.

    Args:
        data (dict): JSON data representing the object.
        root (Path): Path to the root directory.
        url_root (str): URL root path for the API reference.

    Returns:
        dict[str, dict]: The links dictionary mapping type names to URL paths.
    """
    links: dict[str, dict] = {}
    pages: list[_PageSpec] = []

    # ------------------------------------------------------------------
    # Pass 1: build links + directory tree + page specs
    # ------------------------------------------------------------------
    def _pass1(data_root: dict, dir_root: Path, api_ref_root: str, module_import_path: str) -> None:
        dir_root.mkdir(exist_ok=True)
        for name, obj in data_root.items():
            if not isinstance(obj, dict):
                continue

            kind = obj.get("kind", None)
            obj_module_import_path = module_import_path + f".{name}" if module_import_path != "" else name
            if ".functions" in obj_module_import_path:
                obj_module_import_path = obj_module_import_path.replace(".functions", "")

            if kind == "module":
                if name not in links:
                    (dir_root / name).mkdir(exist_ok=True)
                    links[name] = {"path": f"{api_ref_root}/{name}".lower(), "kind": "function"}
                    pages.append(
                        _PageSpec(
                            kind="module",
                            name=name,
                            parent_name="",
                            import_path=obj_module_import_path,
                            file_path=dir_root / name / "_index.md",
                            data=obj,
                        )
                    )

            elif kind == "class":
                if name not in links:
                    (dir_root / name).mkdir(exist_ok=True)
                    links[name] = {"path": f"{api_ref_root}/{name}".lower(), "kind": "class"}
                    pages.append(
                        _PageSpec(
                            kind="class",
                            name=name,
                            parent_name=module_import_path.split(".")[-1],
                            import_path=obj_module_import_path,
                            file_path=dir_root / name / "_index.md",
                            data=obj,
                        )
                    )

            elif name == "functions":
                for func_name in obj:
                    if func_name.startswith("_") or func_name in links:
                        continue
                    links[func_name] = {
                        "path": f"{api_ref_root}/{func_name}".lower(),
                        "kind": "function",
                    }
                    pages.append(
                        _PageSpec(
                            kind="function",
                            name=func_name,
                            parent_name=module_import_path.split(".")[-1],
                            import_path=obj_module_import_path + f".{func_name}",
                            file_path=dir_root / f"{func_name}.md",
                            data=obj[func_name],
                        )
                    )
                continue

            else:
                continue

            _pass1(obj, dir_root / name, f"{api_ref_root}/{name}", obj_module_import_path)

    _pass1(data, root, url_root, "")

    # ------------------------------------------------------------------
    # Pass 2: render HTML and write markdown files
    # ------------------------------------------------------------------
    resolver = LinkResolver(links)

    for page in pages:
        if page.kind == "module":
            content = render_module_html(page.data, resolver)
            spec = TemplateReplacementSpec(name=page.name, link=page.name, content=content)
            template = MODULE_TEMPLATE_STRING
        elif page.kind == "class":
            content = render_class_html(page.data, page.parent_name, page.import_path, resolver)
            spec = TemplateReplacementSpec(name=page.name, link=page.name, parent=page.parent_name, content=content)
            template = CLASS_TEMPLATE_STRING
        elif page.kind == "function":
            content = render_function_html(page.data, page.import_path, resolver)
            spec = TemplateReplacementSpec(name=page.name, link=page.name, parent=page.parent_name, content=content)
            template = FUNCTION_TEMPLATE_STRING
        else:
            continue

        with page.file_path.open("w") as f:
            spec.render_template_to_file(template, f)

    return links


def change_json_root(data: dict, json_start_paths: list[str] | None) -> dict:
    """Change the root of the JSON data to the specified path.

    Args:
        data (dict): Dict with the module data.
        json_start_paths (List[str] | None): Paths to the object in the JSON data.

    Returns:
        dict: Modified JSON data.
    """
    if json_start_paths is None:
        return data

    new_json = {}
    for json_start_path in json_start_paths:
        new_root_data = data
        for part in json_start_path.split("."):
            new_root_data = new_root_data[part]
        new_json[json_start_path.split(".")[-1]] = new_root_data
    return new_json


def parse_toml(toml_path: str, version: str, root_directory: str) -> list[RefHolder]:
    references = []
    # In case of missing toml_file, we need a default for the api-references
    if not os.path.exists(toml_path):
        return [
            RefHolder(
                url=f"/{version}/api-reference",
                packages=["sdk", "catalog"],
                directory=f"{root_directory}/{version}/api-reference",
            )
        ]
    parsed_toml = toml.load(toml_path)
    for name in parsed_toml:
        packages = parsed_toml[name]["packages"]
        directory = f"{root_directory}/{version}/{parsed_toml[name]['directory']}"
        url = f"/{version}/{parsed_toml[name]['directory']}"
        references.append(RefHolder(url, packages, directory))
    return references


def main():
    parser = argparse.ArgumentParser(description="Process a JSON file")
    parser.add_argument("toml_file", metavar="FILE", help="Paths to toml config file", default="api_spec.toml")
    parser.add_argument("json_file", metavar="FILE", help="Paths to json data file", default="data.json")
    parser.add_argument("version", metavar="str", help="Current Version", default="latest")
    parser.add_argument("root_directory", metavar="str", help="Current Version", default="versioned_docs")
    parser.add_argument("--export-links", metavar="FILE", help="Export links dict as JSON for method_page_renderer")

    args = parser.parse_args()

    all_links: dict[str, dict] = {}
    references = parse_toml(args.toml_file, args.version, args.root_directory)
    for ref in references:
        print(f"Parsing: {ref.url}")
        data = read_json_file(args.json_file)
        data = change_json_root(data, ref.packages)
        links = create_file_structure(data, Path(ref.directory), url_root=ref.url)
        all_links.update(links)

    if args.export_links:
        with open(args.export_links, "w") as f:
            json.dump(all_links, f)
        print(f"Exported {len(all_links)} links to {args.export_links}")


if __name__ == "__main__":
    main()
