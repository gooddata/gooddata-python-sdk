#!/bin/bash

rm -rf gooddata_afm_client

#
# https://openapi-generator.tech/docs/generators/python/
#     --additional-properties=packageName=gooddata_afm_client \
#

docker run --rm \
    -v "${PWD}:/local" \
    -u $(id -u ${USER}):$(id -g ${USER}) \
    openapitools/openapi-generator-cli generate \
    -g python \
    --package-name gooddata_afm_client \
    -i https://staging.anywhere.gooddata.com/api/schemas/afm \
    -o /local/gooddata-afm-client

cd gooddata_afm_client
rm -rf .gitlab-ci.yml .travis.yml git_push.sh test
cd ..

#
# this here function in model_utils.py: convert_js_args_to_python_args
#
# gets messed up when our ObjectLinks are being parsed. that is because:
#
# - it uses _self as named parameter to a decorator function it creates; this function also has **kwargs
# - our ObjectLinks contain self (as in links.self); the generator for some of its internal workings also generates '_self' as key of some dict
# - the decorator function eventually gets called with this '_self' thing.. and things bomb because there are multiple values of a named argument
#
sed -i 's/_self/_self_loathing_/g' gooddata-afm-client/gooddata_afm_client/model_utils.py