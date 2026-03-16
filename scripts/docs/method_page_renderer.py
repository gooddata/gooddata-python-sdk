# (C) 2026 GoodData Corporation
"""Pre-render method documentation pages from data.json.

For each markdown file with an ``api_ref`` frontmatter key, this script:
1. Resolves the method/function from data.json
2. Generates signature, description, parameters, and returns as HTML
3. Linkifies type names using the same links dictionary as python_ref_builder
4. Replaces everything between the frontmatter and the first ``## `` heading
   (typically ``## Example``) with the generated HTML
5. Preserves all hand-written content below that heading

Usage:
    python method_page_renderer.py DATA_JSON CONTENT_DIR [--api-ref-url URL_ROOT]

Example:
    python method_page_renderer.py data.json versioned_docs/1.3 \
        --api-ref-url /1.3/api-reference
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Link resolution (mirrors python_ref_builder.LinkResolver)
# ---------------------------------------------------------------------------


class LinkResolver:
    """Resolve type names to HTML hyperlinks using a name->path dict."""

    def __init__(self, links: dict[str, dict]) -> None:
        self.links = links

    def type_link(self, name: str) -> str:
        if not name:
            return name or ""
        orig = name
        clean = name.replace("]", "").replace("Optional[", "").replace("list[", "").replace("List[", "").strip()
        data = self.links.get(clean)
        if data and data.get("path"):
            return orig.replace(clean, f'<a href="{data["path"]}/">{clean}</a>')
        return orig


# ---------------------------------------------------------------------------
# Build links dict from data.json (mirrors python_ref_builder pass 1)
# ---------------------------------------------------------------------------


def build_links(data: dict, url_root: str) -> dict[str, dict]:
    """Walk data.json and build {name: {"path": url, "kind": str}} dict."""
    links: dict[str, dict] = {}

    def _walk(node: dict, api_ref_root: str) -> None:
        for name, obj in node.items():
            if not isinstance(obj, dict):
                continue
            kind = obj.get("kind")
            if kind == "module":
                if name not in links:
                    links[name] = {"path": f"{api_ref_root}/{name}".lower(), "kind": "module"}
                _walk(obj, f"{api_ref_root}/{name}")
            elif kind == "class":
                if name not in links:
                    links[name] = {"path": f"{api_ref_root}/{name}".lower(), "kind": "class"}
                _walk(obj, f"{api_ref_root}/{name}")
            elif name == "functions":
                for fname in obj:
                    if fname.startswith("_") or fname in links:
                        continue
                    links[fname] = {"path": f"{api_ref_root}/{fname}".lower(), "kind": "function"}

    _walk(data, url_root)
    return links


# ---------------------------------------------------------------------------
# Resolve method data from data.json
# ---------------------------------------------------------------------------


def resolve_method(data: dict, api_ref: str) -> dict[str, Any] | None:
    """Resolve ``ClassName.method_name`` from data.json.

    Walks the full tree looking for a class with matching name, then looks up
    the method in its ``functions`` dict.
    """
    parts = api_ref.split(".")
    if len(parts) != 2:
        return None
    class_name, method_name = parts

    def _find_class(node: dict) -> dict | None:
        for name, obj in node.items():
            if not isinstance(obj, dict):
                continue
            kind = obj.get("kind")
            if kind == "class" and name == class_name:
                return obj
            if kind == "module":
                result = _find_class(obj)
                if result is not None:
                    return result
        return None

    cls = _find_class(data)
    if cls is None:
        return None
    functions = cls.get("functions", {})
    return functions.get(method_name)


# ---------------------------------------------------------------------------
# HTML generation (matches shortcode output)
# ---------------------------------------------------------------------------


def _render_signature(func_data: dict, resolver: LinkResolver) -> str:
    """Build the ``name(params) -> return_type`` line."""
    ds = func_data.get("docstring_parsed")
    sig = func_data.get("signature", {})

    # Build parameter string from docstring params if available, else from signature
    if ds and ds.get("params"):
        parts: list[str] = []
        for p in ds["params"]:
            arg = p["arg_name"]
            t = p.get("type_name", "")
            if t:
                arg += f": {t}"
            parts.append(arg)
        param_str = ", ".join(parts)
    elif sig.get("params"):
        param_str = ", ".join(p[0] for p in sig["params"])
    else:
        param_str = ""

    ret_ann = sig.get("return_annotation", "")
    ret_link = resolver.type_link(ret_ann)
    return f"({param_str}) -&gt; {ret_link}" if ret_ann and ret_ann != "None" else f"({param_str})"


def _render_params_table(func_data: dict, resolver: LinkResolver) -> str:
    """Render the Parameters section HTML."""
    ds = func_data.get("docstring_parsed")
    sig = func_data.get("signature", {})

    doc_params = ds.get("params") if ds else None
    sig_params = sig.get("params", [])

    if doc_params:
        rows = ""
        for p in doc_params:
            name = p["arg_name"]
            ptype = resolver.type_link(p.get("type_name", ""))
            desc = p.get("description", "") or ""
            rows += f'<tr>\n<th padding="0px">{name}\n<th padding="0px">{ptype}\n<th>{desc}\n</tr>\n'
        return (
            "<h4>Parameters</h4>\n"
            '<table class="gd-docs-parameters-block">\n'
            "<thead>\n<tr>\n<th>name</th>\n<th>type</th>\n<th>description</th>\n</tr>\n</thead>\n"
            f"<tbody>\n{rows}</tbody>\n</table>"
        )
    elif sig_params:
        rows = ""
        for p in sig_params:
            name = p[0]
            ptype = resolver.type_link(p[1]) if len(p) > 1 else ""
            rows += f'<tr>\n<th padding="0px">{name}\n<th padding="0px">{ptype}\n<th>\n</tr>\n'
        return (
            "<h4>Parameters</h4>\n"
            '<table class="gd-docs-parameters-block">\n'
            "<thead>\n<tr>\n<th>name</th>\n<th>type</th>\n<th>description</th>\n</tr>\n</thead>\n"
            f"<tbody>\n{rows}</tbody>\n</table>"
        )
    else:
        return "<h4>Parameters</h4>\n<i>None</i>"


def _render_returns_table(func_data: dict, resolver: LinkResolver) -> str:
    """Render the Returns section HTML."""
    ds = func_data.get("docstring_parsed")
    sig = func_data.get("signature", {})
    ret_ann = sig.get("return_annotation", "")

    if not ds:
        return "<h4>Returns</h4>\n<i>No docs</i>"

    returns = ds.get("returns")
    if not returns:
        if ret_ann and ret_ann != "None":
            # Has return annotation but no docstring returns section
            return (
                "<h4>Returns</h4>\n"
                '<table class="gd-docs-parameters-block">\n'
                "<thead>\n<tr>\n<th>type</th>\n<th>description</th>\n</tr>\n</thead>\n"
                f'<tbody>\n<tr>\n<th padding="0px">{resolver.type_link(ret_ann)}\n'
                "<th>\n</tr>\n</tbody>\n</table>"
            )
        return "<h4>Returns</h4>\n<i>None</i>"

    type_name = returns.get("type_name") or ret_ann
    if not type_name or type_name == "None":
        return "<h4>Returns</h4>\n<i>None</i>"

    desc = returns.get("description", "") or ""
    return (
        "<h4>Returns</h4>\n"
        '<table class="gd-docs-parameters-block">\n'
        "<thead>\n<tr>\n<th>type</th>\n<th>description</th>\n</tr>\n</thead>\n"
        f'<tbody>\n<tr>\n<th padding="0px">{resolver.type_link(type_name)}\n'
        f"<th>{desc}\n</tr>\n</tbody>\n</table>"
    )


def render_method_html(method_name: str, func_data: dict, resolver: LinkResolver) -> str:
    """Render full method HTML block matching current shortcode output."""
    ds = func_data.get("docstring_parsed")
    sig_line = f"<p><code>{method_name}{_render_signature(func_data, resolver)}</code></p>"

    desc_html = ""
    if ds:
        short = ds.get("short_description", "") or ""
        long = ds.get("long_description", "") or ""
        if short or long:
            desc_html = '<div class="python-ref-description">\n'
            if short:
                desc_html += f"<p>{short}</p>\n"
            if long:
                desc_html += f"<p>{long}</p>\n"
            desc_html += "</div>"

    params_html = _render_params_table(func_data, resolver)
    returns_html = _render_returns_table(func_data, resolver)

    return (
        "<!-- AUTO-GENERATED FROM DOCSTRING — do not edit above this line -->\n\n"
        '<div class="python-ref">\n'
        f"{sig_line}\n"
        f"{desc_html}\n"
        f"{params_html}\n"
        f"{returns_html}\n"
        "</div>\n"
    )


# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r"^---\n(.*?\n)---\n", re.DOTALL)
_API_REF_RE = re.compile(r'^api_ref:\s*["\']?([^"\']+?)["\']?\s*$', re.MULTILINE)
# Match ## or ### headings that are NOT Parameters or Returns (those are auto-generated)
_HEADING_RE = re.compile(r"^#{2,3} (?!Parameters$|Returns$)", re.MULTILINE)


def parse_frontmatter(content: str) -> tuple[str, dict[str, str], str]:
    """Parse frontmatter, returning (frontmatter_block, kv_dict, rest_of_file)."""
    m = _FRONTMATTER_RE.match(content)
    if not m:
        return "", {}, content
    fm_block = m.group(0)
    fm_text = m.group(1)
    rest = content[m.end() :]

    kv: dict[str, str] = {}
    for line in fm_text.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            kv[key.strip()] = val.strip().strip("\"'")
    return fm_block, kv, rest


# ---------------------------------------------------------------------------
# Process a single file
# ---------------------------------------------------------------------------


def process_file(
    file_path: Path,
    data: dict,
    resolver: LinkResolver,
    *,
    dry_run: bool = False,
) -> bool:
    """Process a single markdown file. Returns True if the file was modified."""
    content = file_path.read_text(encoding="utf-8")
    fm_block, kv, rest = parse_frontmatter(content)

    api_ref = kv.get("api_ref")
    if not api_ref:
        return False

    func_data = resolve_method(data, api_ref)
    if func_data is None:
        print(f"WARN: Could not resolve api_ref={api_ref!r} in {file_path}")
        return False

    method_name = api_ref.split(".")[-1]
    html = render_method_html(method_name, func_data, resolver)

    # Find the first ## heading in rest to preserve hand-written content
    heading_match = _HEADING_RE.search(rest)
    preserved = rest[heading_match.start() :] if heading_match else ""

    new_content = fm_block + "\n" + html + "\n" + preserved

    if dry_run:
        print(f"Would update: {file_path}")
        return True

    if new_content != content:
        file_path.write_text(new_content, encoding="utf-8")
        return True
    return False


# ---------------------------------------------------------------------------
# Walk content directory
# ---------------------------------------------------------------------------


def process_directory(
    content_dir: Path,
    data: dict,
    resolver: LinkResolver,
    *,
    dry_run: bool = False,
) -> int:
    """Walk all .md files and process those with api_ref frontmatter."""
    count = 0
    for md_file in sorted(content_dir.rglob("*.md")):
        if md_file.name.startswith("_"):
            continue
        if process_file(md_file, data, resolver, dry_run=dry_run):
            count += 1
    return count


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="Pre-render method documentation pages from data.json")
    parser.add_argument("data_json", help="Path to data.json")
    parser.add_argument("content_dir", help="Path to content directory containing .md files")
    parser.add_argument(
        "--api-ref-url",
        default="/latest/api-reference",
        help="URL root for API reference links (default: /latest/api-reference)",
    )
    parser.add_argument(
        "--links-json",
        help="Path to links.json exported by python_ref_builder (preferred over --api-ref-url)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print what would change without writing")
    args = parser.parse_args()

    with open(args.data_json) as f:
        data = json.load(f)

    if args.links_json:
        with open(args.links_json) as f:
            links = json.load(f)
    else:
        links = build_links(data, args.api_ref_url)
    resolver = LinkResolver(links)

    content_dir = Path(args.content_dir)
    count = process_directory(content_dir, data, resolver, dry_run=args.dry_run)
    print(f"{'Would update' if args.dry_run else 'Updated'} {count} file(s) in {content_dir}")


if __name__ == "__main__":
    main()
