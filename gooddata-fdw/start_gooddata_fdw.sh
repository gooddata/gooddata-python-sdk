#!/bin/bash

set -eu

# Note: image build requires access to the context of the entire repo in order to install the necessary
# GoodData packages located in the repo.
docker build -t postgresql-gd -f Dockerfile ..

docker run --rm -p 2543:5432 \
          -e POSTGRES_DB=gooddata \
          -e POSTGRES_USER=gooddata \
          -e POSTGRES_PASSWORD="${POSTGRES_PASSWORD}" \
          postgresql-gd postgres -c shared_preload_libraries='foreign_table_exposer'
