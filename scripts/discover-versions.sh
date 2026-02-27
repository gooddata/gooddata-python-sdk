#!/bin/bash
# (C) 2026 GoodData Corporation
# Discovers release versions for parallel doc generation.
# Outputs a JSON array suitable for GitHub Actions matrix strategy.
# Usage: discover-versions.sh [remote_name] [num_versions]
set -e

remote_name=${1:-origin}
num_versions=${2:-4}

git fetch "$remote_name" 2>/dev/null

# Build a map of section -> branch, keeping only the latest minor per section.
# Associative arrays preserve last-write-wins semantics, matching the original
# generate.sh behavior where later branches overwrite earlier ones.
declare -A section_map
declare -a section_order

while IFS= read -r vers; do
    section="${vers%.*}"
    if [ -z "${section_map[$section]+x}" ]; then
        section_order+=("$section")
    fi
    # Later (higher minor) versions overwrite earlier ones for the same major
    section_map["$section"]="rel/$vers"
done < <(git branch -rl "$remote_name/rel/*" | sed 's|.*/rel/||' | grep -E '^[0-9]+\.[0-9]+$' | sort -t. -k1,1n -k2,2n | tail -n"$num_versions")

# Add dev branch if it exists
if git branch -rl "$remote_name/rel/dev" | grep -q "rel/dev"; then
    if [ -z "${section_map[dev]+x}" ]; then
        section_order+=("dev")
    fi
    section_map["dev"]="rel/dev"
fi

# Output as JSON array
echo -n "["
first=true
for section in "${section_order[@]}"; do
    branch="${section_map[$section]}"
    if [ "$first" = true ]; then
        first=false
    else
        echo -n ","
    fi
    echo -n "{\"branch\":\"$branch\",\"section\":\"$section\"}"
done
echo "]"
