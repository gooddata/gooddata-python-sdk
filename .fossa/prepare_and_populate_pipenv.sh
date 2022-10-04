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

cd ./gooddata-afm-client
pipenv install --skip-lock -r requirements.txt
cd ..

cd ./gooddata-metadata-client
pipenv install --skip-lock -r requirements.txt
cd ..

cd ./gooddata-scan-client
pipenv install --skip-lock -r requirements.txt
cd ..

cd ./gooddata-api-client
pipenv install --skip-lock -r requirements.txt
cd ..

cd ./gooddata-sdk
pipenv install --skip-lock ../gooddata-afm-client/ ../gooddata-metadata-client/ ../gooddata-scan-client/ ../gooddata-api-client/ \
-r requirements.txt
cd ..

cd ./gooddata-fdw
pipenv install --skip-lock ../gooddata-afm-client/ ../gooddata-metadata-client/ ../gooddata-scan-client/ ../gooddata-api-client/ \
../gooddata-sdk/ -r requirements.txt
cd ..

cd ./gooddata-pandas
pipenv install --skip-lock ../gooddata-afm-client/ ../gooddata-metadata-client/ ../gooddata-scan-client/ ../gooddata-api-client/ \
../gooddata-sdk/ -r requirements.txt
cd ..

cd $ORIG_WORK_DIR
