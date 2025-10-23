Foreign Tables
**************

Import GoodData Objects into PostgreSQL Schema
==============================================

You can import insights created in GoodData.CN Analytical Designer as PostgreSQL foreign tables.
You can import insights from as many workspaces and/or GoodData.CN instances (servers) as you want.

You can also import your entire semantic model including MAQL metrics into a special ``compute`` *pseudo-table*.
Doing SELECTs from this table will trigger computation of analytics on your GoodData.CN server based on the columns
that you have specified on the SELECT.

.. note::
   The ``compute`` is called pseudo-table for a reason. It does not adhere to the relational model. The columns
   that you SELECT map to facts, metrics and labels in your semantic model. Computing results for the select will automatically
   aggregate results on the columns that are mapped to labels in your semantic model. In other words cardinality of
   the ``compute`` table changes based on the columns that you SELECT.

For your convenience we prepared a stored procedure, which:

-  (re)creates target schema
-  imports currently existing insights and/or entire semantic model

You can re-execute the procedure to update foreign tables.

.. code-block:: postgresql

   -- This maps all insights stored in GoodData.CN workspace `workspace_id` into the PostgreSQL schema named `workspace_id`
   CALL import_gooddata('workspace_id', 'insights');

   -- By utilizing the third parameter you can override the name of the target PostgreSQL schema
   CALL import_gooddata('workspace_id', 'insights', 'custom_schema');

   -- This imports the semantic model into the 'compute' pseudo-table.
   CALL import_gooddata('workspace_id', 'compute');

   -- This imports both insights and compute
   CALL import_gooddata('workspace_id', 'all');

   -- This is how you can extend max size of numeric columns in foreign tables (basically to support larger numbers)
   CALL import_gooddata(workspace := 'goodsales', object_type := 'all', numeric_max_size := 24);

   -- Specify custom foreign server name - this enables you importing from multiple servers into the same FDW instance
   CALL import_gooddata(workspace := 'goodsales', object_type := 'all', foreign_server := 'multicorn_gooddata_stg');

Default max numeric size is 18, default digits after decimal point is 2 unless metric format defines more.

You will get a couple of 'NOTICE' messages as the import progresses. You can then check the imported tables
by executing:

.. code-block:: postgresql

   SELECT * FROM information_schema.foreign_tables WHERE foreign_table_schema = 'workspace_id';


**IMPORTANT**: Your semantic model may consist of multiple isolated segments that have no relationship between them. Attempting
to compute results from multiple isolated segments will result in errors.

.. warning::

    Imported tables reflect state of the workspace and insights in time of import. Any later change to the workspace
    can result in failing SQL queries against imported tables. The state can be fixed by re-importing the workspace
    insights and/or compute.

Create Foreign Tables
=====================

You can manually create your own foreign tables and map their columns to GoodData.CN semantic model. This is similar
to creating normal tables except you have to provide table and column OPTIONS to establish the correct mapping. For instance:

.. code-block:: postgresql

   CREATE FOREIGN TABLE custom_report (
       some_label VARCHAR OPTIONS (id 'label/some_label'),
       some_fact_sum  NUMERIC(15,5) OPTIONS (id 'fact/some_fact', agg 'sum'),
       some_fact_avg  NUMERIC(15,5) OPTIONS (id 'fact/some_fact', agg 'avg'),
       some_metric  NUMERIC(15,5) OPTIONS (id 'metric/some_metric')
   )
   SERVER multicorn_gooddata
   OPTIONS ( workspace 'workspace_id');

To explain:

-  OPTIONS on foreign table must contain identifier of workspace to map to
-  OPTIONS on each column must contain identifier of semantic model entity. The id is string but consisting
   of two parts ``<entity_type>/<entity_id>``. Where ``entity_type`` is either label, fact or metric.

For columns that map to facts in your semantic model, you can also specify what aggregation function should be used when
aggregating the fact values for the labels in your custom report table. You can use the following aggregation functions:

-  ``sum``
-  ``avg``
-  ``min``
-  ``max``
-  ``median``

The ``agg`` key is optional. If you do not specify it, then default ``sum`` aggregation will be used. The value of
``agg`` is case insensitive.

.. note::
   If you do not specify the required options, the CREATE command will fail. If you specify wrong entity IDs,
   the failures will happen at SELECT time.

Push Down of Filters
====================

When querying foreign tables, you can add ``WHERE`` clause filtering the result.
For performance optimization, it makes sense to push such filters down to the GoodData.CN, so not all data has to be collected.

We are able to push only some filters down to GoodData.CN:

- Simple attribute(label) filters

  - Example: ``WHERE region IN ('East', 'West')``

- Simple date filters

  - Only DAY granularity is supported
  - (NOT) IN operator is ``not`` supported
  - Example: ``WHERE my_date BETWEEN '2021-01-01 AND 2021-02-01``

If you use an ``OR`` between conditions, it is not pushed down.
Push down is possible in case of custom tables and ``compute`` table, not in case of foreign tables imported
from ``insights``.

Known Limitations
=================

It is not possible to reference a column in ``WHERE`` clause, which is not used in ``SELECT`` section.
Example:

.. code-block:: sql

   SELECT label1, metric FROM insight WHERE label2 = 'a';
   SELECT label1, metric FROM compute WHERE label2 = 'a';

While it is obvious in case of an ``insight`` (it does not contain the column at all), in case of ``compute`` we would
like to support it, but we are not allowed due to lack of functionality in Multicorn -
the filter is always applied on final result set and if it does not contain the column, it does not work.
