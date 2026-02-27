#!/bin/bash
# (C) 2026 GoodData Corporation
# Discovers release versions for parallel doc generation.
# Outputs a JSON array suitable for GitHub Actions matrix strategy.
# Usage: discover-versions.sh [remote_name] [num_versions]
set -e

remote_name=${1:-origin}
num_versions=${2:-4}

git fetch "$remote_name" 2>/dev/null

# Build a map of section -> branch, keeping only the latest patch per section.
# Branches are three-part versions (e.g. rel/1.60.0). We strip the patch to get
# the section (e.g. 1.60), matching the original generate.sh behavior where
# ${target_section%.*} strips the patch component.
declare -A section_map
declare -a section_order

while IFS= read -r vers; do
    # Strip patch: 1.60.0 -> 1.60
    section="${vers%.*}"
    if [ -z "${section_map[$section]+x}" ]; then
        section_order+=("$section")
    fi
    # Later (higher patch) versions overwrite earlier ones for the same major.minor
    section_map["$section"]="rel/$vers"
done < <(git branch -rl "$remote_name/rel/*" | sed 's|.*/rel/||' | grep -E '^[0-9]+\.[0-9]+\.[0-9]+$' | sort -V | tail -n"$num_versions")

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
