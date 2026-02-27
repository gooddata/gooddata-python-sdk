#!/bin/bash
# (C) 2026 GoodData Corporation
# Assembles version artifacts into the final versioned_docs structure.
# Run from the docs/ directory after downloading version artifacts.
#
# Expects:
#   - versioned_docs-raw/ directory with version-* subdirectories (from artifact download)
#   - content/en/ directory with master branch content (from current checkout)
set -e

content_dir=versioned_docs

# Start with clean versioned_docs
rm -rf "$content_dir"
mkdir -p "$content_dir"

# 1. Copy master/current branch content (provides versions page and root structure)
echo "Copying master content from content/en/"
cp -r content/en/. "$content_dir/"

# 2. Move version artifacts from download directory into versioned_docs
if [ -d "versioned_docs-raw" ]; then
    for dir in versioned_docs-raw/version-*/; do
        [ -d "$dir" ] || continue
        section=$(basename "$dir" | sed 's/^version-//')
        echo "Installing version artifact: $section"
        # Remove any existing content for this section (from master copy)
        rm -rf "${content_dir:?}/$section"
        mv "$dir" "$content_dir/$section"
    done
    rm -rf versioned_docs-raw
fi

# 3. Remove master's "latest" directory — it will be replaced by the highest numbered version
echo "Removing master's latest directory"
rm -rf "${content_dir:?}/latest"

# 4. Find the highest numbered version and promote it to "latest"
highest_version=$(ls -1 "./$content_dir/" | grep -E '^[0-9]+$' | sort -V | tail -n 1)

if [ -n "$highest_version" ]; then
    echo "Promoting version $highest_version to /latest"
    mv -f "./$content_dir/$highest_version" "./$content_dir/latest"

    # Update version references in links.json
    if [ -f "./$content_dir/latest/links.json" ]; then
        sed "s|${highest_version}|latest|g" "./$content_dir/latest/links.json" > temp_links.json
        mv temp_links.json "./$content_dir/latest/links.json"
    fi
else
    echo "WARNING: No numbered version directory found to promote to latest"
fi

echo "Assembly complete. Contents of $content_dir/:"
ls -la "$content_dir/"
