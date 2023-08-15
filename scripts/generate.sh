#!/bin/bash
# (C) 2023 GoodData Corporation
set -e
shopt -s extglob

content_dir=versioned_docs
# Name of the remote hosting the main repo
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


git fetch "$remote_name"

# For every release branch, copy the docs to conetentDir/x.y
for branch in "$remote_name/master" $(git branch -rl "$remote_name/rel/*") ; do
    target_section=${branch#"$remote_name"/}
    target_section=${target_section#rel/}
    #target_section=${target_section%.*}
    # Python speciality, this generates the .json for API references

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
        echo "$API_GEN_FILE for branch:$branch exists."
        echo "Generating API ref"
        python3 ../scripts/docs/json_builder.py
        mv -f data.json ./versioned_docs/
        python3 ../scripts/docs/python_ref_builder.py ./versioned_docs/data.json ./versioned_docs/$target_section/api-reference --json_start_path sdk catalog --url_root "/$target_section/api-reference"
        mv -f links.json ./versioned_docs/
    fi
done
if [ "$keep_master" != "keep_master" ] ; then
    echo "master docs will not be published, removing"
    rm -rf "${content_dir}/docs"
fi
popd
