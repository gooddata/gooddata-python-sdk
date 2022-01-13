#!/bin/bash
# (C) 2021 GoodData Corporation

set -e

DIR=$(echo $(cd $(dirname "${BASH_SOURCE[0]}") && pwd -P))
ROOT_DIR="${DIR}/.."
GD_SCHEMA_URL="http://localhost:3000"

function usage() {
  cat >/dev/stderr <<-EOT
Usage:
  $0 <api-client> [specific options]

api-client:
  gooddata-scan-client
  gooddata-metadata-client
  gooddata-afm-client

Options are:
  -u <schema-url> - OpenApi schema url (default: ${GD_SCHEMA_URL})
  -h - show help

Example:
  $0 gooddata-scan-client -u "https://gd.cn"
  $0 -h
EOT
  exit 1
}

POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
  case $1 in
    -u)
      GD_SCHEMA_URL="$2"
      shift # past argument
      shift # past value
      ;;
    -h|--help)
      usage
      ;;
    -*|--*)
      echo "Unknown option $1"
      usage
      ;;
    *)
      POSITIONAL_ARGS+=("$1") # save positional arg
      shift # past argument
      ;;
  esac
done

set -- "${POSITIONAL_ARGS[@]}" # restore positional parameters

GD_API_CLIENT=$1
CLIENT_DIR="${ROOT_DIR}/${GD_API_CLIENT}"

case "$GD_API_CLIENT" in
  gooddata-scan-client)
    GD_API_URI_PATH="${GD_SCHEMA_URL}/api/schemas/scan"
    CLIENT_SRC_ROOT="${CLIENT_DIR}/gooddata_scan_client"
    ;;
  gooddata-metadata-client)
    GD_API_URI_PATH="${GD_SCHEMA_URL}/api/schemas/metadata"
    CLIENT_SRC_ROOT="${CLIENT_DIR}/gooddata_metadata_client"
    ;;
  gooddata-afm-client)
    GD_API_URI_PATH="${GD_SCHEMA_URL}/api/schemas/afm"
    CLIENT_SRC_ROOT="${CLIENT_DIR}/gooddata_afm_client"
    ;;
  *)
    usage
    ;;
esac

echo "GD_API_CLIENT   = ${GD_API_CLIENT}"
echo "GD_API_URI_PATH = ${GD_API_URI_PATH}"
echo "CLIENT_DIR      = ${CLIENT_DIR}"

if [[ -d ${CLIENT_DIR} ]]; then
  echo "CLIENT_DIR exists, triggering generate command"
else
  echo "Creating CLIENT_DIR and preparing it's content for generate command"
  mkdir ${CLIENT_DIR}
  cp ${ROOT_DIR}/.openapi-generator/configs/.openapi-generator-ignore ${CLIENT_DIR}
  ln -s "../OSS LICENSES/LICENSE (${GD_API_CLIENT}).txt" "${CLIENT_DIR}/LICENSE.txt"
fi

docker run --rm \
    -v "${ROOT_DIR}:/local" \
    -u $(id -u ${USER}):$(id -g ${USER}) \
    openapitools/openapi-generator-cli:v5.3.1 generate \
    -c "/local/.openapi-generator/configs/${GD_API_CLIENT}.yaml" \
    -i "${GD_API_URI_PATH}" \
    -o "/local/${GD_API_CLIENT}"

#
# this here function in model_utils.py: convert_js_args_to_python_args
#
# gets messed up when our ObjectLinks are being parsed. that is because:
#
# - it uses _self as named parameter to a decorator function it creates; this function also has **kwargs
# - our ObjectLinks contain self (as in links.self); the generator for some of its internal workings also generates '_self' as key of some dict
# - the decorator function eventually gets called with this '_self' thing.. and things bomb because there are multiple values of a named argument
#
sed -i -e 's/_self/_self_sanitized/g' "${CLIENT_SRC_ROOT}/model_utils.py"
