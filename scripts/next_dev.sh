#!/bin/bash
# (C) 2023 GoodData Corporation

set -e

latest_version=$( curl -L -s https://pypi.org/pypi/gooddata-sdk/json | jq -r '.releases | keys | .[]' | sort -r | awk 'NR==1 {print}')

if [[ $latest_version =~ ^[0-9]+\.[0-9]+\.[0-9]+\.dev[0-9]+$ ]]; then
    # split the version number string into its components
    IFS='.' read -r x y z dev_part <<< "$latest_version"

    # extract the numeric portion of the dev component
    dev_num="${dev_part#dev}"

    # increment the dev component and convert it back to a string
    ((dev_num++))

    # combine the components back into a single version number string
    echo "$x.$y.$z.dev$dev_num"
elif [[ $latest_version =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    # split the version number string into its components
    IFS='.' read -r x y z <<< "$latest_version"
    # increment the last version
    ((z++))
    echo "$x.$y.$z.dev1"
else
    echo "Error occurred $latest_version does not match N.N.N nor N.N.N.devN pattern."
    exit 1
fi
