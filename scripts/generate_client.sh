#!/bin/bash
# (C) 2021 GoodData Corporation

set -e

DIR=$(echo $(cd $(dirname "${BASH_SOURCE[0]}") && pwd -P))
ROOT_DIR="${DIR}/.."
GD_SCHEMA_URL="http://localhost:3000"
GD_SCHEMA_FILE=""
API_VERSION="v1"

function usage() {
  cat >/dev/stderr <<-EOT
Usage:
  $0 <api-client> [specific options]

api-client:
  gooddata-api-client

Options are:
  -u <schema-url> - OpenApi schema url (default: ${GD_SCHEMA_URL}), this option in not supported for gooddata-api-client
  -f <schema-file> - OpenApi schema file, has precedence before -u if present
  -n <docker-network> - Name of docker network to connect to so that schema URL
                        is reachable. If not specified, no network is connected.
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
    -n)
      DOCKER_NETWORK_NAME="$2"
      shift # past argument
      shift # past value
      ;;
    -f)
      GD_SCHEMA_FILE="$2"
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
    GD_API_URI_PATH="${GD_SCHEMA_URL}/api/${API_VERSION}/schemas/scan"
    CLIENT_SRC_ROOT="${CLIENT_DIR}/gooddata_scan_client"
    ;;
  gooddata-metadata-client)
    GD_API_URI_PATH="${GD_SCHEMA_URL}/api/${API_VERSION}/schemas/metadata"
    CLIENT_SRC_ROOT="${CLIENT_DIR}/gooddata_metadata_client"
    ;;
  gooddata-afm-client)
    GD_API_URI_PATH="${GD_SCHEMA_URL}/api/${API_VERSION}/schemas/afm"
    CLIENT_SRC_ROOT="${CLIENT_DIR}/gooddata_afm_client"
    ;;
  gooddata-api-client)
      CLIENT_SRC_ROOT="${CLIENT_DIR}/gooddata_api_client"
      ;;
  *)
    usage
    ;;
esac

if [[ "${GD_SCHEMA_FILE}" != "" ]]; then
  GD_API_URI_PATH="${GD_SCHEMA_FILE}"
fi

echo "GD_API_CLIENT   = ${GD_API_CLIENT}"
echo "GD_API_URI_PATH = ${GD_API_URI_PATH}"
echo "CLIENT_DIR      = ${CLIENT_DIR}"
echo "DOCKER_NETWORK  = ${DOCKER_NETWORK_NAME:-NOT_SET}"

if [[ -d ${CLIENT_DIR} ]]; then
  echo "CLIENT_DIR exists, preparing client directory for a new content"
  OA_GEN_FILE_LOG="${CLIENT_DIR}/.openapi-generator/FILES"
  if [[ -f ${OA_GEN_FILE_LOG} ]]; then
    echo "Removing originally generated files based on ${OA_GEN_FILE_LOG}"
    pushd ${CLIENT_DIR}
    cat ${OA_GEN_FILE_LOG} | xargs rm -f
    popd
  else
    echo "File ${OA_GEN_FILE_LOG} does not exist. Skipping original content cleanup"
  fi
else
  echo "Creating CLIENT_DIR and preparing it's content for generate command"
  mkdir ${CLIENT_DIR}
  ln -s "../OSS LICENSES/LICENSE (${GD_API_CLIENT}).txt" "${CLIENT_DIR}/LICENSE.txt"
fi
# always put .openapi-generator-ignore to the directory, it is one of generated files
cp ${ROOT_DIR}/.openapi-generator/configs/.openapi-generator-ignore ${CLIENT_DIR}

if [[ -z "${DOCKER_NETWORK_NAME+x}" ]]; then
  CONN_NETWORK_ARG=""
else
  CONN_NETWORK_ARG="--network ${DOCKER_NETWORK_NAME}"
fi

docker run --rm \
    -v "${ROOT_DIR}:/local" \
    -u $(id -u ${USER}):$(id -g ${USER}) \
    ${CONN_NETWORK_ARG} \
    openapitools/openapi-generator-cli:v6.6.0 generate \
    -c "/local/.openapi-generator/configs/${GD_API_CLIENT}.yaml" \
    -i "${GD_API_URI_PATH}" \
    -o "/local/${GD_API_CLIENT}"
