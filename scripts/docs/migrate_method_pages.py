#!/usr/bin/env python3
# (C) 2026 GoodData Corporation
"""One-time migration: convert hand-written method pages to api_ref directive format.

For each method page under docs/content/:
1. Reads the frontmatter to determine the superheading (e.g. "catalog_data_source.")
2. Maps superheading to the SDK class name (e.g. CatalogDataSourceService)
3. Adds ``api_ref: "ClassName.method_name"`` to frontmatter
4. Strips the manually written signature, description, and parameter/returns blocks
5. Preserves the ## Example section and everything below

Usage:
    python migrate_method_pages.py CONTENT_DIR [--dry-run]

Example:
    python migrate_method_pages.py docs/content/en/latest --dry-run
    python migrate_method_pages.py docs/content/en/latest
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

# Mapping from superheading prefix to SDK service class name.
# Derived from GoodDataSdk service attributes.
SUPERHEADING_TO_CLASS: dict[str, str] = {
    "catalog_data_source": "CatalogDataSourceService",
    "catalog_workspace": "CatalogWorkspaceService",
    "catalog_workspace_content": "CatalogWorkspaceContentService",
    "catalog_user": "CatalogUserService",
    "catalog_permission": "CatalogPermissionService",
    "catalog_organization": "CatalogOrganizationService",
    "compute": "ComputeService",
    "export": "ExportService",
    "tables": "TableService",
    "visualizations": "VisualizationService",
    "support": "SupportService",
}

_FRONTMATTER_RE = re.compile(r"^---\n(.*?\n)---\n", re.DOTALL)
# Match ## or ### headings that are NOT Parameters or Returns (those are auto-generated)
_PRESERVE_HEADING_RE = re.compile(r"^#{2,3} (?!Parameters$|Returns$)", re.MULTILINE)


def migrate_file(file_path: Path, *, dry_run: bool = False) -> bool:
    """Migrate a single method page. Returns True if the file was modified."""
    content = file_path.read_text(encoding="utf-8")

    fm_match = _FRONTMATTER_RE.match(content)
    if not fm_match:
        return False

    fm_text = fm_match.group(1)
    rest = content[fm_match.end() :]

    # Skip files that already have api_ref
    if "api_ref:" in fm_text:
        return False

    # Extract superheading
    sh_match = re.search(r'^superheading:\s*["\']?([^"\']+?)["\']?\s*$', fm_text, re.MULTILINE)
    if not sh_match:
        return False

    superheading = sh_match.group(1).rstrip(".")
    class_name = SUPERHEADING_TO_CLASS.get(superheading)
    if not class_name:
        print(f"WARN: Unknown superheading {superheading!r} in {file_path}")
        return False

    # Extract method name from title
    title_match = re.search(r'^title:\s*["\']?([^"\']+?)["\']?\s*$', fm_text, re.MULTILINE)
    if not title_match:
        return False
    method_name = title_match.group(1)

    api_ref = f"{class_name}.{method_name}"

    # Add api_ref to frontmatter (before the closing ---)
    new_fm_text = fm_text.rstrip("\n") + f'\napi_ref: "{api_ref}"\n'
    new_fm_block = f"---\n{new_fm_text}---\n"

    # Find the first ## heading that isn't Parameters/Returns to preserve hand-written content
    heading_match = _PRESERVE_HEADING_RE.search(rest)
    preserved = rest[heading_match.start() :] if heading_match else ""

    new_content = new_fm_block + "\n" + preserved

    if dry_run:
        print(f'Would migrate: {file_path} -> api_ref: "{api_ref}"')
        return True

    if new_content != content:
        file_path.write_text(new_content, encoding="utf-8")
        print(f'Migrated: {file_path} -> api_ref: "{api_ref}"')
        return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Migrate method pages to api_ref directive format")
    parser.add_argument("content_dir", help="Path to content directory (e.g. docs/content/en/latest)")
    parser.add_argument("--dry-run", action="store_true", help="Print what would change without writing")
    args = parser.parse_args()

    content_dir = Path(args.content_dir)
    count = 0
    skipped = 0

    for md_file in sorted(content_dir.rglob("*.md")):
        if md_file.name.startswith("_"):
            continue
        # Skip non-method pages (no superheading = not a method page)
        text = md_file.read_text(encoding="utf-8")
        if "superheading:" not in text:
            skipped += 1
            continue
        if migrate_file(md_file, dry_run=args.dry_run):
            count += 1

    action = "Would migrate" if args.dry_run else "Migrated"
    print(f"\n{action} {count} file(s), skipped {skipped} non-method file(s)")


if __name__ == "__main__":
    main()
