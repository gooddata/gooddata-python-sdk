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

# Generate API reference if json_builder.py exists on the branch
API_GEN_FILE="$branch:scripts/docs/json_builder.py"
if git cat-file -e "$API_GEN_FILE" 2>/dev/null; then
    echo "Generating API ref for section $section..."

    # Get api_spec.toml from the branch
    if git ls-tree --name-only "$branch" | grep -q "^api_spec.toml$"; then
        git checkout "$branch" -- api_spec.toml
    else
        echo "No api_spec.toml on $branch, removing local copy"
        rm -f api_spec.toml
    fi

    # Generate API introspection data from this version's SDK
    python3 ../scripts/docs/json_builder.py
    mv -f data.json "$content_dir/$section/"

    # Generate API reference markdown files
    python3 ../scripts/docs/python_ref_builder.py api_spec.toml \
        "./$content_dir/$section/data.json" "$section" "$content_dir"
else
    echo "No json_builder.py on $branch, skipping API ref generation"
fi

echo "Done: section $section from $branch"
