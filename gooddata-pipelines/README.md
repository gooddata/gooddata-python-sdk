# GoodData Pipelines

A high-level library for automating the lifecycle of GoodData Cloud (GDC).

You can use the package to manage following resources in GDC:

1. Provisioning (create, update, delete)
   - User profiles
   - User Groups
   - User/Group permissions
   - User Data Filters
   - Child workspaces (incl. Workspace Data Filter settings)
1. Backup and restore of workspaces
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
import logging

from csv import DictReader
from pathlib import Path

# Import the Entity Provisioner class and corresponding model from the gooddata_pipelines library
from gooddata_pipelines import UserFullLoad, UserProvisioner

# Create the Provisioner instance - you can also create the instance from a GDC yaml profile
provisioner = UserProvisioner(
    host=os.environ["GDC_HOSTNAME"], token=os.environ["GDC_AUTH_TOKEN"]
)

# Optional: set up logging and subscribe to logs emitted by the provisioner
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
provisioner.logger.subscribe(logger)

# Load your data from your data source
source_data_path: Path = Path("path/to/some.csv")
source_data_reader = DictReader(source_data_path.read_text().splitlines())
source_data = [row for row in source_data_reader]

# Validate your input data
full_load_data: list[UserFullLoad] = UserFullLoad.from_list_of_dicts(
    source_data
)

# Run the provisioning
provisioner.full_load(full_load_data)

```

## Bugs & Requests

Please use the [GitHub issue tracker](https://github.com/gooddata/gooddata-python-sdk/issues) to submit bugs
or request features.

## Changelog

See [Github releases](https://github.com/gooddata/gooddata-python-sdk/releases) for released versions
and a list of changes.

## Backup and restore of workspaces
The backup and restore module allows you to create snapshots of GoodData Cloud workspaces and restore them later. This is useful for:

- Creating backups before major changes
- Migrating workspaces between environments
- Disaster recovery scenarios
- Copying workspace configurations

### Backup

The module supports three backup modes:

1. **List of workspaces** - Backup specific workspaces by providing a list of workspace IDs
2. **Workspace hierarchies** - Backup a workspace and all its direct and indirect children
3. **Entire organization** - Backup all workspaces in the organization

Each backup includes:
- Workspace declarative model (logical data model, analytics model, permissions)
- User data filters
- Filter views
- Automations

#### Storage Options

Backups can be stored in:
- **Local storage** - Save backups to a local directory
- **S3 storage** - Upload backups to an AWS S3 bucket

#### Basic Usage

```python
import os
from pathlib import Path

from gooddata_pipelines import BackupManager
from gooddata_pipelines.backup_and_restore.models.storage import (
    BackupRestoreConfig,
    LocalStorageConfig,
    StorageType,
)
from gooddata_pipelines.logger.logger import LogObserver

# Optionally, subscribe a standard Python logger to the LogObserver
import logging
logger = logging.getLogger(__name__)
LogObserver().subscribe(logger)

# Configure backup storage
config = BackupRestoreConfig(
    storage_type=StorageType.LOCAL,
    storage=LocalStorageConfig(),
    batch_size=10,  # Number of workspaces to process in one batch
    api_calls_per_second=10,  # Rate limit for API calls
)

# Create the BackupManager instance
backup_manager = BackupManager.create(
    config=config,
    host=os.environ["GDC_HOSTNAME"],
    token=os.environ["GDC_AUTH_TOKEN"]
)

# Backup-specific workspaces
workspace_ids = ["workspace1", "workspace2", "workspace3"]
backup_manager.backup_workspaces(workspace_ids=workspace_ids)

# Or read workspace IDs from a CSV file
backup_manager.backup_workspaces(path_to_csv="workspaces.csv")

# Backup workspace hierarchies (workspace + all children)
backup_manager.backup_hierarchies(workspace_ids=["parent_workspace"])

# Backup entire organization
backup_manager.backup_entire_organization()
```

#### Using S3 Storage
``` python
from gooddata_pipelines.backup_and_restore.models.storage import (
BackupRestoreConfig,
S3StorageConfig,
StorageType,
)

# Configure S3 storage with explicit credentials
config = BackupRestoreConfig(
storage_type=StorageType.S3,
storage=S3StorageConfig(
bucket="my-backup-bucket",
backup_path="gooddata-backups/",
aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
aws_default_region="us-east-1"
),
)

# Or use AWS profile
config = BackupRestoreConfig(
storage_type=StorageType.S3,
storage=S3StorageConfig(
bucket="my-backup-bucket",
backup_path="gooddata-backups/",
profile="my-aws-profile"
),
)

backup_manager = BackupManager.create(
config=config,
host=os.environ["GDC_HOSTNAME"],
token=os.environ["GDC_AUTH_TOKEN"]
)

backup_manager.backup_workspaces(workspace_ids=["workspace1"])
```

#### Using GoodData Profile
You can also create the BackupManager from a GoodData profile file:
``` python
from pathlib import Path

backup_manager = BackupManager.create_from_profile(
    config=config,
    profile="production",
    profiles_path=Path.home() / ".gooddata" / "profiles.yaml"
)
```

CSV File Format
When providing workspace IDs via a CSV file, the file should have a workspace_id column:
``` csv
workspace_id
workspace1
workspace2
workspace3
```

#### Configuration Options

The BackupRestoreConfig class accepts the following parameters:
- `storage_type` - Type of storage (StorageType.LOCAL or StorageType.S3)
- `storage` - Storage-specific configuration (LocalStorageConfig or S3StorageConfig)
- `batch_size` (optional, default: 10) - Number of workspaces to process in one batch
- `api_calls_per_second` (optional, default: 10) - Rate limit for API calls to avoid throttling
- `api_page_size` (optional, default: 500) - Page size for paginated API calls


#### Error Handling and Retries

The backup process includes automatic retry logic with exponential backoff. If a batch fails, it will retry up to 3 times before failing completely. Individual workspace errors are logged but don't stop the entire backup process.
Restore

Note: Restore functionality is currently in development.
