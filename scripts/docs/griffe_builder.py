# (C) 2026 GoodData Corporation
"""Build data.json from Python source using griffe (static AST analysis).

Drop-in replacement for json_builder.py — produces an identical JSON schema
but does NOT require importing the target packages at runtime.

Usage:
    python griffe_builder.py [--search-path PATH ...] [--output FILE] PACKAGE [PACKAGE ...]

Example:
    python griffe_builder.py \
        --search-path packages/gooddata-sdk/src \
        --search-path packages/gooddata-pandas/src \
        --output data.json \
        gooddata_sdk gooddata_pandas
"""

from __future__ import annotations

import argparse
import json
import os
from typing import Any

import griffe
from griffe import (
    Attribute,
    Class,
    Docstring,
    DocstringParameter,
    DocstringReturn,
    DocstringSectionKind,
    Function,
    Module,
)

# ---------------------------------------------------------------------------
# Docstring helpers
# ---------------------------------------------------------------------------


def _parse_docstring_params(docstring: Docstring | None) -> list[dict[str, Any]]:
    """Extract parameter info from a parsed Google-style docstring."""
    if docstring is None:
        return []
    params: list[dict[str, Any]] = []
    for section in docstring.parsed:
        if section.kind is DocstringSectionKind.parameters:
            for p in section.value:
                assert isinstance(p, DocstringParameter)
                params.append(
                    {
                        "arg_name": p.name,
                        "default": str(p.default) if p.default else None,
                        "is_optional": None,
                        "type_name": str(p.annotation) if p.annotation else None,
                        "description": p.description or None,
                    }
                )
    return params


def _parse_docstring_returns(docstring: Docstring | None) -> dict[str, Any] | None:
    """Extract return info from a parsed Google-style docstring."""
    if docstring is None:
        return None
    for section in docstring.parsed:
        if section.kind is DocstringSectionKind.returns:
            for r in section.value:
                assert isinstance(r, DocstringReturn)
                return {
                    "type_name": str(r.annotation) if r.annotation else None,
                    "description": r.description or None,
                    "return_name": r.name or None,
                }
    return None


def _short_description(docstring: Docstring | None) -> str | None:
    if docstring is None:
        return None
    for section in docstring.parsed:
        if section.kind is DocstringSectionKind.text:
            text = section.value
            # First paragraph = short description
            idx = text.find("\n\n")
            return text[:idx].strip() if idx != -1 else text.strip()
    return None


def _long_description(docstring: Docstring | None) -> str | None:
    if docstring is None:
        return None
    for section in docstring.parsed:
        if section.kind is DocstringSectionKind.text:
            text = section.value
            idx = text.find("\n\n")
            if idx != -1:
                return text[idx:].strip()
            return None
    return None


def _examples_str(docstring: Docstring | None) -> str:
    if docstring is None:
        return "[]"
    for section in docstring.parsed:
        if section.kind is DocstringSectionKind.examples:
            return str(section.value)
    return "[]"


def _docstring_data(docstring: Docstring | None) -> dict[str, Any] | None:
    """Build the docstring_parsed dict matching json_builder output."""
    if docstring is None:
        return None
    return {
        "params": _parse_docstring_params(docstring),
        "long_description": _long_description(docstring),
        "short_description": _short_description(docstring),
        "examples": _examples_str(docstring),
        "returns": _parse_docstring_returns(docstring),
    }


# ---------------------------------------------------------------------------
# Object converters
# ---------------------------------------------------------------------------


def _annotation_str(annotation: Any) -> str:
    """Convert a griffe annotation to the string form json_builder would produce."""
    if annotation is None:
        return "None"
    return str(annotation)


def _function_data(func: Function) -> dict[str, Any]:
    """Build function dict matching json_builder.FunctionData."""
    sig_params: list[list[str]] = []
    for param in func.parameters:
        if param.name == "self":
            continue
        param_str = str(param.name)
        if param.annotation is not None:
            param_str += f": {param.annotation}"
        if param.default is not None:
            param_str += f" = {param.default}"
        ann_str = _annotation_str(param.annotation)
        sig_params.append([param_str, ann_str])

    is_property = "property" in func.labels
    docstring = func.docstring
    # Parse with Google style
    if docstring is not None:
        docstring.parse("google")

    return {
        "kind": "function",
        "docstring": docstring.value if docstring else None,
        "signature": {
            "params": sig_params,
            "return_annotation": _annotation_str(func.annotation),
        },
        "is_property": is_property,
        "docstring_parsed": _docstring_data(docstring),
    }


def _class_data(cls: Class, package_name: str) -> dict[str, Any]:
    """Build class dict matching json_builder.ClassData."""
    docstring = cls.docstring
    if docstring is not None:
        docstring.parse("google")

    functions: dict[str, Any] = {}
    # Use all_members to include inherited methods (matches inspect.getmembers behavior)
    for name, member in cls.all_members.items():
        if member.is_alias:
            try:
                resolved = member.resolve_target()
                if isinstance(resolved, Function):
                    functions[name] = _function_data(resolved)
            except Exception:
                pass
        elif isinstance(member, Function):
            functions[name] = _function_data(member)
        elif (
            isinstance(member, Attribute)
            and "property" in member.labels
            and hasattr(member, "getter")
            and member.getter is not None
        ):
            functions[name] = _function_data(member.getter)

    return {
        "kind": "class",
        "docstring": docstring.value if docstring else None,
        "docstring_parsed": _docstring_data(docstring),
        "functions": functions,
    }


def _module_data(module: Module, package_name: str) -> dict[str, Any]:
    """Build module dict matching json_builder.module_data."""
    data: dict[str, Any] = {"kind": "module"}
    for name, member in module.members.items():
        if isinstance(member, Class):
            # Filter: only classes defined in this package
            if member.is_alias:
                try:
                    target = member.resolve_target()
                    if package_name not in str(target.canonical_path):
                        continue
                except Exception:
                    continue
            data[name] = _class_data(member, package_name)
        elif isinstance(member, Module):
            if member.is_alias:
                try:
                    target = member.resolve_target()
                    if package_name not in str(target.canonical_path):
                        continue
                except Exception:
                    continue
            data[name] = _module_data(member, package_name)
    return data


def _parse_package(module: Module, package_name: str) -> dict[str, Any]:
    """Walk the package tree and build the data dict."""
    data: dict[str, Any] = {"kind": "module"}
    for name, member in module.members.items():
        if isinstance(member, Module):
            if member.is_alias:
                try:
                    target = member.resolve_target()
                    if package_name not in str(target.canonical_path):
                        continue
                except Exception:
                    continue
            if member.is_subpackage:
                data[name] = _parse_package(member, package_name)
            else:
                data[name] = _module_data(member, package_name)
    return data


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def build_data_json(packages: list[str], search_paths: list[str]) -> dict[str, Any]:
    """Load packages via griffe and produce the combined data dict."""
    output: dict[str, Any] = {}
    for pkg_name in packages:
        pkg = griffe.load(
            pkg_name,
            search_paths=search_paths,
            docstring_parser="google",
        )
        output.update(_parse_package(pkg, pkg_name))
    # Remove the top-level "kind" keys that _parse_package adds
    output.pop("kind", None)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Build data.json using griffe (static AST analysis)")
    parser.add_argument("packages", nargs="+", help="Package names to analyze (e.g. gooddata_sdk)")
    parser.add_argument(
        "--search-path",
        action="append",
        default=[],
        dest="search_paths",
        help="Directories to search for packages (repeatable)",
    )
    parser.add_argument("--output", default="data.json", help="Output JSON file path")
    args = parser.parse_args()

    search_paths = args.search_paths or ["."]
    output = build_data_json(args.packages, search_paths)

    with open(args.output, "w") as f:
        json.dump(output, f)

    print(f"Saved data.json ({len(output)} top-level keys) to {os.path.abspath(args.output)}")


if __name__ == "__main__":
    main()
