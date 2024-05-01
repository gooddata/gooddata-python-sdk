---
title: "Introduction"
linkTitle: "Introduction"
weight: 10
sectionIndex: false
cascade:
- type: "docs"
  toc_root: true
  _target:
    path: "/*/**"
---

GoodData Python SDK provides a clean and convenient way to interact with the [GoodData API](https://www.gooddata.com/docs/cloud/api-and-sdk/api/) in Python applications.

Python is a popular language for working with large amounts of data and data analytics; It is for this reason that we are actively developing this SDK to let Python developers integrate the GoodData analytical engine into their own applications as seamlessly as possible, or to automate their administrative workflow.

![Relationship to GoodData](./figures/Python_doc_flat.png)



## What is Python SDK Good For



Python SDK lets you script things that may otherwise be very tedious to do using the GoodData user interface alone, such as:

#### Automate the provisioning

You can perform administration tasks such as managing users, permissions and create new workspaces, their hierarchies and data sources. With Python SDK you can write scripts that will let you easily create new users and workspaces, as well as manage existing ones.

```python
sdk.catalog_data_source.create_or_update_data_source(
    CatalogDataSourcePostgres(
        id=data_source_id,
        name=data_source_name,
        db_specific_attributes=PostgresAttributes(
            host=os.environ["POSTGRES_HOST"],
            db_name=os.environ["POSTGRES_DBNAME"]
        ),
        schema=os.environ["POSTGRES_SCHEMA"],
        credentials=BasicCredentials(
            username=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
        ),
    )
)
```

#### Integrate into CI/CD pipelines

Integrate GoodData analytics into your continuous delivery practices by, for example, automatically transplanting content from your staging workspaces to your production workspaces at an appropriate time in your production and delivery cycle.

```python
# Reads visualizations from workspace
visualizations = sdk.visualizations.get_visualizations("123")

# Iterate through visualizations and check if they are valid
for visualization in visualizations:
    try:
        sdk.visualizations.for_visualization("123", visualization)
    except Exception:
        print(f"Visualization {visualization.title} is broken.")

```

#### Create data pipelines

Export your data,
levarage services like machine learning to transform your data
and import the data back into GoodData to visualize the results and gain visualizations.
In the Example below, we demonstrate GoodPandas, which can leverage machine learning practices.
```python
pandas = GoodPandas(os.getenv('HOST'), os.getenv('TOKEN'))
df = pandas.data_frames(workspace_id="123")

campaign_spend = df.for_visualization("campaign_spend")

# Now you have a dataframe with data from your visualization
# You can do linear regression, clustering, predictions, analysis, etc.
```


![Relationship to GoodData](./figures/Python_doc_isometric.png)

### What is Python SDK Not Good For

Python SDK is not designed to facilitate the embedding of GoodData analytics into the front-end of your web applications. For customizable embedding of visualizations and dashboard, see our [React SDK](https://sdk.gooddata.com/gooddata-ui/docs/about_gooddataui.html).

## What Can I Do With Python SDK

With Python SDK you have full control over:

* Workspaces
  * Workspace hierarchies
  * Workspace data filters
* Data sources
* Logical data models
* Workspace content
  * Facts
  * Attributes
  * Labels
  * Metrics
  * Visualizations

You can also perform certain administration tasks:

* Manage users and user groups
* Manage workspace permissions and hierarchyPermissions

## Where to Learn More

Get started with Python SDK right now by following the [Quick Start](./getting-started/#quick-start) guide.

New to GoodData? Follow the [Getting Started](https://www.gooddata.com/docs/cloud/getting-started/) series of articles that include Python SDK code examples.

### Troubleshooting

In case of any issues with Python SDK, feel free to reach out to us on our [community slack](https://www.gooddata.com/slack/) or create a [GitHub issue](https://github.com/gooddata/gooddata-python-sdk/issues).
