# GoodData Pipelines

The `gooddata-pipelines` package provides a number of high level scripts to interact with and manage [GoodData](https://www.gooddata.com/).

At the moment, the package allows you to automate these features:

- Provisioning (creation, updtating and removal of resources) of
  - workspaces
  - users
  - user groups
  - user permissions
  - user data filters
  <!-- TODO: Backups, restores -->

<!-- TODO: link to documentation -->
<!-- See [DOCUMENTATION](https://www.gooddata.com/docs/python-sdk/1.43.0) for more details. -->

## Requirements

- GoodData Cloud or GoodData.CN installation
- Python 3.10 or newer

## Installation

Run the following command to install the `gooddata-pipelines` package on your system:

    pip install gooddata-pipelines

## Example

This example illustrates how to use this package to manage GoodData Cloud workspaces. The provisioning script will ingest data which will be used as a source of truth to configure GoodData. The script will compare the source data with the current state of GoodData instance and will create, update and delete workspaces and user data filter settings to match the source data.

```python

# Import WorkspaceProvisioner and Workspace model.
from gooddata_pipelines import Workspace, WorkspaceProvisioner

# Gather the raw data to be used by the provisioner.
raw_data: list[dict] = [
    {
        "parent_id": "parent_workspace_id",
        "workspace_id": "workspace_id",
        "workspace_name": "Workspace Name",
        "workspace_data_filter_id": "wdf_id",
        "workspace_data_filter_values": ["value1", "value2"],
    }
]

# Convert raw data to Workspace objects.
data = [Workspace(**item) for item in raw_data]

# Create a WorkspaceProvisioner using your GoodData host name and token.
host = "https://your-gooddata-host.com"
token = "your_gooddata_token"
provisioner = WorkspaceProvisioner.create(host=host, token=token)

# Provision the workspaces
provisioner.provision(data)
```

## Bugs & Requests

Please use the [GitHub issue tracker](https://github.com/gooddata/gooddata-python-sdk/issues) to submit bugs
or request features.

## Changelog

See [Github releases](https://github.com/gooddata/gooddata-python-sdk/releases) for released versions
and a list of changes.
