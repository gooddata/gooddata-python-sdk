#!/bin/bash

DIR=$(echo $(cd $(dirname "${BASH_SOURCE[0]}") && pwd -P))
ROOT_DIR="${DIR}/.."

CLIENT_DIR="${ROOT_DIR}/gooddata-afm-client"

rm -rf ${CLIENT_DIR}

#
# https://openapi-generator.tech/docs/generators/python/
#     --additional-properties=packageName=gooddata_afm_client \
#

docker run --rm \
    -v "${ROOT_DIR}:/local" \
    -u $(id -u ${USER}):$(id -g ${USER}) \
    openapitools/openapi-generator-cli generate \
    -g python \
    --package-name gooddata_afm_client \
    --additional-properties packageVersion=0.6.0,packageName=gooddata_afm_client \
    -i https://staging.anywhere.gooddata.com/api/schemas/afm \
    -o /local/gooddata-afm-client

rm -rf "${CLIENT_DIR}/.gitlab-ci.yml"
rm -rf "${CLIENT_DIR}/.travis.yml"
rm -rf "${CLIENT_DIR}/git_push.sh"
rm -rf "${CLIENT_DIR}/test"

#
# this here function in model_utils.py: convert_js_args_to_python_args
#
# gets messed up when our ObjectLinks are being parsed. that is because:
#
# - it uses _self as named parameter to a decorator function it creates; this function also has **kwargs
# - our ObjectLinks contain self (as in links.self); the generator for some of its internal workings also generates '_self' as key of some dict
# - the decorator function eventually gets called with this '_self' thing.. and things bomb because there are multiple values of a named argument
#
sed -i -e 's/_self/_self_sanitized/g' "${CLIENT_DIR}/gooddata_afm_client/model_utils.py"
