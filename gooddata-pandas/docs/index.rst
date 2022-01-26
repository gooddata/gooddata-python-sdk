.. _index_root:

GoodData Pandas Documentation
*****************************

GoodData Pandas contains a thin layer that utilizes GoodData Python SDK and allows you to conveniently create pandas series and
data frames from the computations done against semantic model in your GoodData.CN workspace.

Getting Started
---------------

Requirements
============

-  GoodData.CN installation; either running on your cloud
   infrastructure or the free Community Edition running on your workstation
-  Python 3.7 or newer

Installation
============

Run the following command to install the ``gooddata-pandas`` package on your system:

.. code-block:: shell

    pip install gooddata-pandas

Examples
--------

Here are a couple of introductory examples how to create indexed and not-indexed series and data frames:

Series
======

.. code-block:: python

    from gooddata_pandas import GoodPandas

    # GoodData.CN host in the form of uri eg. "http://localhost:3000"
    host = "http://localhost:3000"
    # GoodData.CN user token
    token = "some_user_token"
    # initialize the adapter to work on top of GD.CN host and use the provided authentication token
    gp = GoodPandas(host, token)

    workspace_id = "demo"
    series = gp.series(workspace_id)

    # create indexed series
    indexed_series = series.indexed(index_by="label/label_id", data_by="fact/measure_id")

    # create non-indexed series containing just the values of measure sliced by elements of the label
    non_indexed = series.not_indexed(data_by="fact/measure_id", granularity="label/label_id")

Data Frames
===========

.. code-block:: python

    from gooddata_pandas import GoodPandas

    # GoodData.CN host in the form of uri eg. "http://localhost:3000"
    host = "http://localhost:3000"
    # GoodData.CN user token
    token = "some_user_token"
    # initialize the adapter to work on top of GD.CN host and use the provided authentication token
    gp = GoodPandas(host, token)

    workspace_id = "demo"
    frames = gp.data_frames(workspace_id)

    # create indexed data frame
    indexed_df = frames.indexed(
        index_by="label/label_id",
        columns=dict(
            first_label='label/first_label_id',
            second_label='label/second_label_id',
            first_metric='metric/first_metric_id',
            second_metric='fact/fact_id'
        )
    )

    # create data frame with hierarchical index
    indexed_df = frames.indexed(
        index_by=dict(first_label='label/first_label_id', second_label='label/second_label_id'),
        columns=dict(first_metric='metric/first_metric_id', second_metric='fact/fact_id')
    )

    # create non-indexed data frame
    non_indexed_df = frames.not_indexed(
        columns=dict(
            first_label='label/first_label_id',
            second_label='label/second_label_id',
            first_metric='metric/first_metric_id',
            second_metric='fact/fact_id'
        )
    )

    # creates data frame based on the contents of the insight. if the insight contains labels and measures, the data
    # frame will contain index or hierarchical index.
    insight_df = frames.for_insight('insight_id')

    # creates data frame based on the content of the items dict. if the dict contains both labels and measures, the
    # frame will contain index or hierarchical index.
    df = frames.for_items(
        items=dict(
            first_label='label/first_label_id',
            second_label='label/second_label_id',
            first_metric='metric/first_metric_id',
            second_metric='fact/fact_id'
        )
    )

.. _index_api:

API Documentation
-----------------
Check out the :doc:`api` section for further information.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api


Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
