#!/bin/bash
# (C) 2021 GoodData Corporation
set -e
set -x

ORIG_WORK_DIR=$(pwd)
PROJ_HOME="/home/fossa/sources/gooddata-python-sdk"

pip3.9 install pipenv

echo "Building pipenv dependencies for projects"
export PIPENV_IGNORE_VIRTUALENVS=1
cd $PROJ_HOME


cd ./gooddata-api-client
pipenv install -r requirements.txt
cd ..

cd ./gooddata-sdk
pipenv install ../gooddata-api-client/ \
-r requirements.txt
cd ..

cd ./gooddata-fdw
pipenv install ../gooddata-api-client/ \
../gooddata-sdk/ -r requirements.txt
cd ..

cd ./gooddata-pandas
pipenv install ../gooddata-api-client/ \
../gooddata-sdk/ -r requirements.txt
cd ..

cd ./gooddata-dbt
pipenv install ../gooddata-api-client/ \
../gooddata-sdk/ -r requirements.txt
cd ..

cd ./gooddata-flight-server
pipenv install -r requirements.txt
cd ..

cd ./gooddata-flexfun
pipenv install ../gooddata-api-client/ \
../gooddata-sdk/ ../gooddata-flight-server/ -r requirements.txt
cd ..

cd $ORIG_WORK_DIR
