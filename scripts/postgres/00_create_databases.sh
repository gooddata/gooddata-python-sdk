#!/usr/bin/env bash
# (C) 2024 GoodData Corporation
#
# PostgreSQL init script for GoodData multi-service architecture.
# Creates all required databases for GoodData microservices.
#
# This script is executed by PostgreSQL container during initialization
# (mounted to /docker-entrypoint-initdb.d/).

set -e
set -u

echo "Creating database 'md' (metadata-api)"
createdb md

echo "Creating database 'dex' (authentication)"
createdb dex

echo "Creating database 'execution' (afm-exec-api)"
createdb execution

echo "Creating database 'automation' (scheduling/alerting)"
createdb automation

echo "Creating database 'gw' (api-gateway)"
createdb gw

# For test workspaces - each workspace is stored in a separate schema
# using the data-loader tool with --no-schema-versioning flag
echo "Creating database 'tiger' (test data)"
createdb tiger

echo "All required databases created successfully!"
