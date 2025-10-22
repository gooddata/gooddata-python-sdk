# (C) 2021 GoodData Corporation
FROM postgres:12.14-alpine

#
# Docker image that adds multicorn & gooddata-fdw on top of official PostgreSQL image.
#
# Note: multicorn has some issues building against PostgreSQL 13 so going with v12 for now
#

#
# There is also some funny stuff in the multicorn make file. Documented here:
#
# see: https://github.com/Segfault-Inc/Multicorn/issues/183
# see: https://gist.github.com/felixge/49c37dffb49efc8bc0911b1113231de0#file-dockerfile
#
# The preflight-check is removed because of this.
#

RUN apk add --no-cache --update wget make musl-dev llvm llvm-dev gcc clang python3 python3-dev py3-setuptools py3-pip \
     && pip3 --no-color --no-cache-dir -qq install pgxnclient \
     \
     && pgxnclient install foreign_table_exposer \
     \
     && wget http://api.pgxn.org/dist/multicorn/1.4.0/multicorn-1.4.0.zip && unzip multicorn-1.4.0 && cd multicorn-1.4.0 \
     && echo "" > preflight-check.sh && PYTHON_OVERRIDE=python3 make && PYTHON_OVERRIDE=python3 make install

#
# Add all required gooddata-python packages into the image
#
ADD gooddata-api-client /gd/gooddata-api-client
ADD packages/gooddata-sdk /gd/gooddata-sdk
ADD packages/gooddata-fdw /gd/gooddata-fdw

RUN cd /gd/gooddata-api-client  && pip install . \
     && cd /gd/gooddata-sdk && pip install . \
     && cd /gd/gooddata-fdw && pip install .

# Add sql files to be executed during start of container
# They register extensions and install helping sql procedures
ADD packages/gooddata-fdw/sql/create_extensions.sql /docker-entrypoint-initdb.d/create_extensions.sql
ADD packages/gooddata-fdw/sql/import_gooddata.sql /docker-entrypoint-initdb.d/import_gooddata.sql
