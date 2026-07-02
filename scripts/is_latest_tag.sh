#!/bin/bash
# (C) 2026 GoodData Corporation
# Prints "true" if the given tag is the highest semver among all v*.*.* tags,
# otherwise "false". Requires the repository's tags to be present locally
# (callers should checkout with fetch-depth: 0).
# Usage: is_latest_tag.sh vX.Y.Z
set -e

tag="$1"
if [ -z "$tag" ]; then
    echo "Usage: is_latest_tag.sh vX.Y.Z" >&2
    exit 1
fi

highest=$(git tag -l 'v*.*.*' | sort -V | tail -1)
if [ "$tag" = "$highest" ]; then
    echo "true"
else
    echo "false"
fi
