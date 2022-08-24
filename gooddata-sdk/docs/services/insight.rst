Insights Service
================

The ``gooddata_sdk.insights`` service gives you access to insights stored in a workspace. It can retrieve all the insights from a workspace or one
insight based on its name. Insight instance is the input for other services like a Table service

Entity methods
**************

The *gooddata_sdk.insights* supports the following entity API calls:

* ``get_insights(workspace_id: str)``

    Returns *list[Insight]*.

    Retrieve a list of Insight objects.

**Example usage:**

Read all insights in a workspace:

.. code-block:: python

    from gooddata_sdk import GoodDataSdk

    # GoodData.CN host in the form of uri eg. "http://localhost:3000"
    host = "http://localhost:3000"
    # GoodData.CN user token
    token = "some_user_token"
    sdk = GoodDataSdk.create(host, token)

    workspace_id = "demo"

    # Reads insights from workspace
    insights = sdk.insights.get_insights(workspace_id)
    # Print all fetched insights
    for insight in insights:
        print(str(insight))
