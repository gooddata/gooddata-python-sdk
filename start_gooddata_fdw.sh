#!/bin/bash

set -eu

docker build -t postgresql-gd .
docker run --rm -p 2543:5432 \
          -e POSTGRES_DB=gooddata \
          -e POSTGRES_USER=gooddata \
          -e POSTGRES_PASSWORD="${POSTGRES_PASSWORD}" \
          postgresql-gd postgres -c shared_preload_libraries='foreign_table_exposer'
