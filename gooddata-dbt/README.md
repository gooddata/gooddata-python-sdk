# gooddata-dbt
GoodData plugin for dbt. Reads dbt models and profiles, generates GoodData semantic model.

## Install

```shell
pip install gooddata-dbt
# Or add the corresponding line to requirements.txt
# Or install specific version
pip install gooddata-dbt==1.0.0
```

You can also install optional dependencies:
```shell
# To allow sending comments to GitHub pull requests
pip install PyGithub
# To allow automatic translation of GoodData metadata
pip install deep-translator
```

## Configuration, parametrization
Create `gooddata.yaml` file to configure so-called data products and environments.
Check [gooddata_example.yml](gooddata_example.yml) file for more details.

Parametrization of each execution can be done using environment variables / tool arguments.
Use main --help and --help for each use case to learn more.

Alternatively, you can configure everything with environment variables.
You can directly set env variables in a shell session, or store them to .env file(s).
We provide the following example:
- [.env.dev](.env.dev)
- [.env.custom.dev](.env.custom.dev) is loaded from the above file and contains sensitive variables.
  Add `.env.custom.*` to .gitignore!

Then load .env files:
```bash
source .env.local
```

## Use cases
```shell
gooddata-dbt --help
```
The plugin provides the following use cases:
- provision_workspaces
  - Provisions workspaces to GoodData based on gooddata.yaml file
- register_data_sources
  - Registers data source in GoodData for each relevant dbt profile
- deploy_ldm
  - Reads dbt models and profiles
  - Scans data source (connection props from dbt profiles) through GoodData to get column data types (optional in dbt)
  - Generates GoodData LDM(Logical Data Model) from dbt models. Can utilize custom gooddata-specific metadata, more below
- upload_notification
  - Invalidates caches for data source
- deploy_analytics
  - Reads content of `gooddata_layout` folder and deploys analytics model to GoodData
- store_analytics
  - Reads analytics model from GoodData instance and stores it to disk to `gooddata_layout` folder
- test_visualizations
  - Lists all visualizations execution from GoodData instance, and executes each report to validate it
- dbt_cloud
  - Runs dbt cloud job through their API. Alternative to running dbt-core locally.
  - If running in CI pipeline, it can also notify about performance degradations in a form of GitHub/Gitlab comment.
- dbt_cloud_stats
  - Esp. for testing purposes. It's triggered from dbt_cloud as well. It collects stats and reports perf degradations.
  - Check [.env.dev](.env.dev)/[.env.custom.dev](.env.custom.dev) files for how to set related env variables.

## Custom metadata in dbt models (optional)
If you want to generate optimal LDM from dbt models, sometimes you need to specify semantic metadata in dbt models.

In general, all GoodData metadata must be put to dbt models under `meta` key, except descriptions.

### Titles, descriptions
dbt supports only `description` field. For now, gooddata-dbt generates GoodData title/description from dbt description.

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
By default, gooddata-dbt generates GoodData entities based on the following rules:
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
        referenced_table: <table name, target of reference (FK), if ldm_type=reference>
        label_type: TEXT/HYPERLINK/GEO_LATITUDE/GEO_LONGITUDE
        attribute_column: <column name of attribute of label, if ldm_type=label>
        sort_column: "<any column in the same table, may not be exposed as LDM object>"
        sort_direction: "DESC"
        # Only for labels, this label will be displayed by default in reports
        default_view: true
```
