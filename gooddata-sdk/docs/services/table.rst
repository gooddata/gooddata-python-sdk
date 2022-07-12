:orphan:

Table Service
*************

The ``gooddata_sdk.table`` service allows you to consume analytics in typical tabular format. The service allows free-form
computations and computations of data for GoodData.CN Insights.

.. _t entity methods:

Entity methods
^^^^^^^^^^^^^^

The *gooddata_sdk.table* supports the following entity API calls:


* ``for_insight(workspace_id: str, insight: Insight)``

    Returns *ExecutionTable*.

    Retrieve data as an ExecutionTable from the given insight.

* ``for_items(workspace_id: str, items: list[Union[Attribute, Metric]], filters: Optional[list[Filter]] = None)``

    Returns *ExecutionTable*.

    Retrieve data as an ExecutionTable from the given list of attributes/metrics, and filters.

**Example usage:**

Get tabular data for an insight defined on your GoodData.CN server:

.. code-block:: python

    from gooddata_sdk import GoodDataSdk

    # GoodData.CN host in the form of uri eg. "http://localhost:3000"
    host = "http://localhost:3000"
    # GoodData.CN user token
    token = "some_user_token"
    sdk = GoodDataSdk.create(host, token)

    workspace_id = "demo"
    insight_id = "some_insight_id_in_demo_workspace"

    # Reads insight from workspace
    insight = sdk.insights.get_insight(workspace_id, insight_id)

    # Triggers computation for the insight. the result will be returned in a tabular form
    table = sdk.tables.for_insight(workspace_id, insight)

    # This is how you can read data row-by-row and do something with it
    for row in table.read_all():
        print(row)

    # An example of data printed for insight top_10_products
    # {'781952e728204dcf923142910cc22ae2': 'Biolid', 'fe513cef1c6244a5ac21c5f49c56b108': 'Outdoor', '77dc71bbac92412bac5f94284a5919df': 34697.71}
    # {'781952e728204dcf923142910cc22ae2': 'ChalkTalk', 'fe513cef1c6244a5ac21c5f49c56b108': 'Home', '77dc71bbac92412bac5f94284a5919df': 17657.35}
    # {'781952e728204dcf923142910cc22ae2': 'Elentrix', 'fe513cef1c6244a5ac21c5f49c56b108': 'Outdoor', '77dc71bbac92412bac5f94284a5919df': 27662.09}
    # {'781952e728204dcf923142910cc22ae2': 'Integres', 'fe513cef1c6244a5ac21c5f49c56b108': 'Outdoor', '77dc71bbac92412bac5f94284a5919df': 47766.74}
    # {'781952e728204dcf923142910cc22ae2': 'Magnemo', 'fe513cef1c6244a5ac21c5f49c56b108': 'Electronics', '77dc71bbac92412bac5f94284a5919df': 44026.52}
    # {'781952e728204dcf923142910cc22ae2': 'Neptide', 'fe513cef1c6244a5ac21c5f49c56b108': 'Outdoor', '77dc71bbac92412bac5f94284a5919df': 99440.44}
    # {'781952e728204dcf923142910cc22ae2': 'Optique', 'fe513cef1c6244a5ac21c5f49c56b108': 'Home', '77dc71bbac92412bac5f94284a5919df': 40307.76}
    # {'781952e728204dcf923142910cc22ae2': 'PortaCode', 'fe513cef1c6244a5ac21c5f49c56b108': 'Electronics', '77dc71bbac92412bac5f94284a5919df': 18841.17}
    # {'781952e728204dcf923142910cc22ae2': 'Slacks', 'fe513cef1c6244a5ac21c5f49c56b108': 'Clothing', '77dc71bbac92412bac5f94284a5919df': 18469.15}
    # {'781952e728204dcf923142910cc22ae2': 'T-Shirt', 'fe513cef1c6244a5ac21c5f49c56b108': 'Clothing', '77dc71bbac92412bac5f94284a5919df': 17937.49}
