#!/bin/bash
# (C) 2026 GoodData Corporation
# Generates documentation for a single version branch.
# This is the per-version logic extracted from generate.sh for parallel execution.
#
# Usage: generate-single-version.sh <full-branch-ref> <section>
# Example: generate-single-version.sh origin/rel/1.3 1
#
# Prerequisites:
#   - Repository checked out with the target branch fetched
#   - Python environment with script-requirements.txt installed from the TARGET branch
set -e

branch=$1
section=$2

if [ -z "$branch" ] || [ -z "$section" ]; then
    echo "Usage: generate-single-version.sh <full-branch-ref> <section>"
    echo "Example: generate-single-version.sh origin/rel/1.3 1"
    exit 1
fi

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT/docs"

content_dir=versioned_docs

mkdir -p "$content_dir/$section"

# Determine source content path on the branch
if git ls-tree -d "$branch" -- "content/en/docs" 2>/dev/null | grep -q "content/en/docs"; then
    src_section=docs
else
    src_section=latest
fi

# Extract documentation content from the branch
echo "Extracting docs from $branch for section $section (src=$src_section)"
# strip-components=3 removes content/en/{src_section} prefix
git archive "$branch" "content/en/$src_section" | tar xf - -C "$content_dir/$section" \
    --strip-components=3 "content/en/$src_section"

# Generate API reference if griffe_builder.py (or legacy json_builder.py) exists on the branch
GRIFFE_GEN_FILE="$branch:scripts/docs/griffe_builder.py"
LEGACY_GEN_FILE="$branch:scripts/docs/json_builder.py"
if git cat-file -e "$GRIFFE_GEN_FILE" 2>/dev/null || git cat-file -e "$LEGACY_GEN_FILE" 2>/dev/null; then
    echo "Generating API ref for section $section..."

    # Get api_spec.toml from the branch
    if git ls-tree --name-only "$branch" | grep -q "^api_spec.toml$"; then
        git checkout "$branch" -- api_spec.toml
    else
        echo "No api_spec.toml on $branch, removing local copy"
        rm -f api_spec.toml
    fi

    # Generate API introspection data using griffe (static analysis, no imports needed).
    # Always use the current branch's griffe_builder.py — it works on any branch's
    # source code via --search-path and doesn't require the SDK packages to be installed.
    python3 ../scripts/docs/griffe_builder.py \
        --search-path ../packages/gooddata-sdk/src \
        --search-path ../packages/gooddata-pandas/src \
        --output data.json \
        gooddata_sdk gooddata_pandas

    # Generate API reference markdown files and export links for method page renderer
    python3 ../scripts/docs/python_ref_builder.py api_spec.toml \
        data.json "$section" "$content_dir" \
        --export-links links.json

    # Pre-render method pages with api_ref directives.
    # Always use the current branch's renderer — old branches have Hugo shortcodes
    # (parameters-block, parameter) whose templates were removed.
    echo "Pre-rendering method pages for section $section..."
    python3 ../scripts/docs/method_page_renderer.py \
        data.json "$content_dir/$section" \
        --links-json links.json

    # Clean up intermediate files (no longer needed after pre-rendering)
    rm -f data.json links.json
else
    echo "No json_builder.py or griffe_builder.py on $branch, skipping API ref generation"
fi

echo "Done: section $section from $branch"
