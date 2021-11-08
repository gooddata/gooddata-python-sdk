# GoodData.CN Foreign Data Wrapper

## Getting Started

For convenience a Dockerfile is in place which when started will run PostgreSQL 12 with multicorn and gooddata-fdw
installed. There is a [script in place](./start_gooddata_fdw.sh) to automate build and startup steps:

    POSTGRES_PASSWORD=... ./start_gooddata_fdw

You need to provide your own password via the `POSTGRES_PASSWORD` environmental variable. The command will build an
image containing official PostgreSQL v12 and install all the requirements and GoodData FDW into it. It will create
a new `gooddata` DB and `gooddata` user who will have access to this DB. The password for this user is what you have
entered in the `POSTGRES_PASSWORD` variable.

__Note on using GD.CN.CE and provided Postgre image in docker__:
In case you are about to run both components in docker, both should be connected to same docker network.
Then the containers are able to address each other via __hostnames that are equal to value of provided --name value__
as shown in the next excerpt:

``` shell
# create the network
docker network create tiger_network -d bridge

# pass --name and --network to both starting containers, eg.:
docker run --name gdcnce --network tiger_network -i -t -p 3000:3000 -p 5432:5432 -v gd-volume:/data gooddata/gooddata-cn-ce:latest

docker run --name multicorn --network tiger_network --rm -p 2543:5432 \
          -e POSTGRES_DB=gooddata \
          -e POSTGRES_USER=gooddata \
          -e POSTGRES_PASSWORD=$PASS \
          -e GOODDATA_SDK_HTTP_HEADERS='{"Host": "localhost"}' \
          postgresql-gd postgres -c shared_preload_libraries='foreign_table_exposer'
```

After the container starts, you can connect to the running PostgreSQL:

-   From console using `psql --host localhost --port 2543 --user gooddata gooddata`

    You will be asked to enter the password that you have specified when starting the script.

-   From any other client using JDBC string: `jdbc:postgresql://localhost:2543/gooddata`

    You will be asked to enter username (gooddata) and password.

Once connected you will be able to work with the GD.CN Foreign Data Wrapper. At first, you need to define your GD.CN
server in PostgreSQL:

```postgresql
CREATE SERVER multicorn_gooddata FOREIGN DATA WRAPPER multicorn
OPTIONS (
    wrapper 'gooddata_fdw.GoodDataForeignDataWrapper',
    host 'https://gdcnce:3000', -- host equal to name of container with GD.CN.CE 
    token 'auth_token'
);
```

Typically you have to do this once per GD.CN installation. You can add as many servers as you want/need.

**IMPORTANT**: do not forget to specify host including the schema (http or https).

## Import insights from your workspace

You can import insights created in GoodData.CN Analytical Designer as PostgreSQL foreign tables. You can import insights
from as many workspaces as you want. We recommend you to create schema per workspace otherwise you run risk of table
name clashes.

```postgresql
--
-- Schema to map insights into. This can be anything you want.
--
CREATE SCHEMA gooddata_workspace;

--
-- This maps all insights stored in GD.CN workspace into a schema of your choice.
--
-- Note: it is essential that you import from 'gooddata_insights'. That is the schema that the FDW uses to
-- identify that you actually want to map the workspace's insights
--
IMPORT FOREIGN SCHEMA gooddata_insights FROM SERVER multicorn_gooddata INTO gooddata_workspace OPTIONS (
    workspace 'workspace_id'
);
```

You will get couple of 'NOTICE' messages as the import progresses. You can then check the imported tables for instance
by executing:

```postgresql
SELECT * FROM information_schema.foreign_tables WHERE foreign_table_schema = 'gooddata_workspace';
```

## Free-form computations on top of Semantic Model

You can import your entire semantic model including MAQL metrics into a special `compute` **pseudo-table**. Doing SELECTs
from this table will trigger computation of analytics on your GoodData.CN server based on the columns that you have
specified on the SELECT.

Note that the `compute` is called pseudo-table for a reason. It does not adhere to the relational model. The columns
that you SELECT map to facts, metrics and labels in your semantic model. Computing results for the select will automatically
aggregate results on the columns that are mapped to labels in your semantic model. In other words cardinality of
the `compute` table changes based on the columns that you SELECT.

This is how you can import the semantic model:

```postgresql
--
-- Schema where the compute pseudo-table should be created. This can be any schema, even schema where you map the
-- insights.
--
CREATE SCHEMA gooddata_workspace;

--
-- This imports the semantic model into the 'compute' pseudo-table.
--
-- Note: it is essential that you import from 'gooddata_compute'. That is the schema that the FDW uses to
-- identify that you actually want to import the semantic layer.
--
IMPORT FOREIGN SCHEMA gooddata_compute FROM SERVER multicorn_gooddata INTO gooddata_workspace OPTIONS (
    workspace 'workspace_id'
);
```

**IMPORTANT**: Your semantic model may consist of multiple isolated segments that have no relationship between them. Attempting
to compute results from multiple isolated segments will result in errors.

## Custom reports as foreign tables

You can manually create your own foreign tables and map their columns to GoodData.CN semantic model. This is similar
to creating normal tables except you have to provide table and column OPTIONS to establish the correct mapping. For instance:

```postgresql
CREATE FOREIGN TABLE custom_report (
    some_label VARCHAR OPTIONS (id 'label/some_label'),
    some_fact_sum  NUMERIC(15,5) OPTIONS (id 'fact/some_fact', agg 'sum'),
    some_fact_avg  NUMERIC(15,5) OPTIONS (id 'fact/some_fact', agg 'avg'),
    some_metric  NUMERIC(15,5) OPTIONS (id 'metric/some_metric')
)
SERVER multicorn_gooddata
OPTIONS ( workspace 'workspace_id');
```

To explain:

-  OPTIONS on foreign table must contain identifier of workspace to map to
-  OPTIONS on each column must contain identifier of semantic model entity. The id is string but consisting
   of two parts `<entity_type>/<entity_id>`. Where `entity_type` is either label, fact or metric.

For columns that map to facts in your semantic model, you can also specify what aggregation function should be used when
aggregating the fact values for the labels in your custom report table. You can use the following aggregation functions:

-  `sum`
-  `avg`,
-  `min`,
-  `max`,
-  `median`

The `agg` key is optional. If you do not specify it, then default 'sum' aggregation will be used. The value of `agg` is
case insensitive.

Note: If you do not specify the required options, the CREATE command will fail. If you specify wrong entity IDs,
the failures will happen at SELECT time.
