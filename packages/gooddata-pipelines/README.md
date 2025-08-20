# GoodData Pipelines

A high-level library for automating the lifecycle of GoodData Cloud (GDC).

You can use the package to manage following resources in GDC:

1. Provisioning (create, update, delete)
   - User profiles
   - User Groups
   - User/Group permissions
   - User Data Filters
   - Child workspaces (incl. Workspace Data Filter settings)
1. _[PLANNED]:_ Backup and restore of workspaces
1. _[PLANNED]:_ Custom fields management
   - extend the Logical Data Model of a child workspace

In case you are not interested in incorporating a library in your own program but would like to use a ready-made script, consider having a look at [GoodData Productivity Tools](https://github.com/gooddata/gooddata-productivity-tools).

## Provisioning

The entities can be managed either in _full load_ or _incremental_ way.

Full load means that the input data should represent the full and complete desired state of GDC after the script has finished. For example, you would include specification of all child workspaces you want to exist in GDC in the input data for workspace provisioning. Any workspaces present in GDC and not defined in the source data (i.e., your input) will be deleted.

On the other hand, the incremental load treats the source data as instructions for a specific change, e.g., a creation or a deletion of a specific workspace. You can specify which workspaces you would want to delete or create, while the rest of the workspaces already present in GDC will remain as they are, ignored by the provisioning script.

The provisioning module exposes _Provisioner_ classes reflecting the different entities. The typical usage would involve importing the Provisioner class and the data input data model for the class and planned provisioning method:

```python
import os
from csv import DictReader
from pathlib import Path

# Import the Entity Provisioner class and corresponding model from gooddata_pipelines library
from gooddata_pipelines import UserFullLoad, UserProvisioner
from gooddata_pipelines.logger.logger import LogObserver

# Optionally, subscribe a standard Python logger to the LogObserver
import logging
logger = logging.getLogger(__name__)
LogObserver().subscribe(logger)

# Create the Provisioner instance - you can also create the instance from a GDC yaml profile
provisioner = UserProvisioner(
    host=os.environ["GDC_HOSTNAME"], token=os.environ["GDC_AUTH_TOKEN"]
)

# Load your data from your data source
source_data_path: Path = Path("path/to/some.csv")
source_data_reader = DictReader(source_data_path.read_text().splitlines())
source_data = [row for row in source_data_reader]

# Validate your input data with
full_load_data: list[UserFullLoad] = UserFullLoad.from_list_of_dicts(
    source_data
)
provisioner.full_load(full_load_data)
```

Ready-made scripts covering the basic use cases can be found here in the [GoodData Productivity Tools](https://github.com/gooddata/gooddata-productivity-tools) repository
