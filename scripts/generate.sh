#!/bin/bash
# (C) 2023 GoodData Corporation
set -e
shopt -s extglob

content_dir=versioned_docs
# Name of the remote hosting the main repo (gitlab.com/gooddata/gdc-tiger-docs)
remote_name=${1:-origin}
# target branch where changes will be applied (master, rel/0.7, ...)
target_branch=${2:-master}
# if set to "keep_master", the "docs" from master will be preserved (only for preview!)
keep_master=$3

echo "Validating target branch '$target_branch'"
case "$target_branch" in
    master)
        current_section=""
        src_dir="."
        ;;
    rel/@(+([[:digit:]]).+([[:digit:]])|cloud))
        current_section="${target_branch#rel/}"
        src_dir="docs"
        ;;
    *)
        echo "Unsupported target branch '$target_branch'"
        exit 1
esac

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# TODO: update when we move hugo to repo root
pushd "$REPO_ROOT/docs"

rm -rf ${content_dir:?}/*

# Add upstream if it doesn't exist
if ! git config remote.upstream.url >/dev/null; then
  git remote add upstream https://github.com/gooddata/gooddata-python-sdk
else
  echo "Upstream already exists, skipping add."
fi

git fetch "$remote_name"

# For every release branch, copy the docs to conetentDir/x.y
for branch in "$remote_name/master" $(git branch -rl "$remote_name/rel/*") ; do
    target_section=${branch#"$remote_name"/}
    target_section=${target_section#rel/}
    target_section=${target_section%.*}
    if [ "$target_section" == "master" ] ; then
        # handle master branch specially, all contents is copied, not just docs
        target_section=""
        # number of path segments to throw away by tar: content/en => 2
        strip_count=2
        src_section=""
    else
        # number of path segments to throw away by tar: content/en/x.y => 3
        strip_count=3
        src_section=docs
    fi
    if [ "$target_section" == "$current_section" ] ; then
        # copy the current docs to proper section
        echo "Getting data from workdir for $branch"
        cp -r "content/en/$src_dir" "$content_dir/$current_section"
    else
        echo "Getting data from remote $branch branch"
        # TODO: Update path and components when we move hugo to repo root
        mkdir -p "$content_dir/$target_section"
        git archive "$branch" "content/en/$src_section" | tar xf - -C "$content_dir/$target_section" \
            --strip-components=$strip_count "content/en/$src_section"
    fi
    API_GEN_FILE="$branch:scripts/docs/json_builder.py"
    if git cat-file -e $API_GEN_FILE; then
        echo "$API_GEN_FILE exists."
        echo "Generating API ref..."
        if [ "$target_section" == "" ] ; then
            echo "Skipping master api ref"
        else
            directories=$(ls -d ../gooddata-*)

            for dir in $directories; do
                git checkout "$branch" -- "$dir"
            done
            if git ls-tree --name-only "$branch" | grep -q "^api_spec.toml$"; then
                git checkout "$branch" -- api_spec.toml
            else
              echo "removing the API_spec"
              rm -rf api_spec.toml
            fi
            python3 ../scripts/docs/json_builder.py
            python3 ../scripts/docs/python_ref_builder.py api_spec.toml data.json "$target_section" versioned_docs
        fi
    fi
done


## Moving the highest version to latest
highest_version=$(ls ./versioned_docs/ | grep -E '^[0-9]+\.[0-9]+$' | sort -V | tail -n 1)
echo "Moving ${highest_version} to /latest"
mv -f ./versioned_docs/$highest_version ./versioned_docs/latest


if [ "$keep_master" != "keep_master" ] ; then
    echo "master docs will not be published, removing"
    rm -rf "${content_dir}/docs"
fi
popd

git reset --hard
