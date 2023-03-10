# dbt-gooddata
GoodData plugin for dbt. Reads dbt models and profiles, generates GoodData semantic model.

## Install

TODO, now only directly from git:
```shell
pip install git+https://github.com/jaceksan/dbt-gooddata.git
# Or add the following line to requirements.txt
-e git+https://github.com/jaceksan/dbt-gooddata.git
```

## Local development
```shell
# Creates virtualenv, installs dependencies
make dev
# Installs the package itself
make install
```

## Configuration, parametrization
Create `gooddata.yaml` file to configure so-called data products and environments.
Check [gooddata_example.yaml](gooddata_example.yaml) file for more details.

Parametrization of each execution can be done using environment variables / tool arguments.
Use main --help and --help for each use case to learn more.

Example setup of environment variables for local environment (running GoodData Community Edition locally):
```shell
export POSTGRES_HOST="localhost"
export POSTGRES_PORT=5432
export POSTGRES_USER="demouser"
export POSTGRES_PASS=demopass
export POSTGRES_DBNAME=demo
export INPUT_SCHEMA="input_stage"
export OUTPUT_SCHEMA="output_stage"

export DBT_PROFILE_DIR="profile"
export DBT_PROFILE="default"
export ELT_ENVIRONMENT="dev_local"

export GOODDATA_HOST="http://localhost:3000"
export GOODDATA_ENVIRONMENT_ID="development"
unset GOODDATA_UPPER_CASE
export GOODDATA_TOKEN="YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz"
```

## Use cases
```shell
dbt-gooddata --help
```
The plugin provides the following use cases:
- deploy_models
  - Reads dbt models and profiles
  - Scans data source (connection props from dbt profiles) through GoodData to get column data types (optional in dbt)
  - Registers data source in GoodData
  - Generates and stores PDM (Physical model) from dbt models and the result of the scan
  - Generates GoodData LDM(Logical Data Model) from dbt models. Can utilize custom gooddata-specific metadata, more below
- upload_notification
  - Invalidates caches for data source
- deploy_analytics
  - Reads content of `gooddata_layout` folder and deploys analytics model to GoodData
- store_analytics
  - Reads analytics model from GoodData instance and stores it to disk to `gooddata_layout` folder 
- test_insights
  - Lists all insights(reports) from GoodData instance, and executes each report to validate it

## Custom metadata in dbt models (optional)
If you want to generate optimal LDM from dbt models, sometimes you need to specify semantic metadata in dbt models.

In general, all GoodData metadata must be put to dbt models under `meta` key, except descriptions.

### Titles, descriptions
dbt supports only `description` field. For now, dbt-gooddata generates GoodData title/description from dbt description. 

Can be specified for both tables and columns.

### Model ID
Per table, you can specify `model_id`. When deploying models/analytics, you can include any subset of model_ids.
```yaml
models:
  - name: xxx
    meta:
      gooddata:
        model_id: my_id
```

### GoodData entities
By default, dbt-gooddata generates GoodData entities based on the following rules:
- data type = NUMERIC (decimal number) - fact
- data_type = DATE/TIMESTAMP/TIMESTAMPTZ - date dimension
- other data types = attributes

To override the default, specify custom GoodData meta this way:
```yaml
columns:
  - name: xxxx
    meta:
      gooddata:
        ldm_type: fact/attribute/label/date/reference/primary_key
        referenced_table: <table name, target of reference (FK)>
        label_type: TEXT/HYPERLINK/GEO(?) 
        attribute_column: <column name of attribute of this label>
```

