import datetime
from dataclasses import dataclass

from gooddata_sdk._version import __version__ as sdk_version


@dataclass(frozen=True)
class DirNames:
    """
    Folder names used in the SDK backup process:
    - LAYOUTS - GoodData Layouts
    - LDM - Logical Data Model
    - AM - Analytics Model
    - UDF - User Data Filters
    """

    LAYOUTS = "gooddata_layouts"
    LDM = "ldm"
    AM = "analytics_model"
    UDF = "user_data_filters"


@dataclass(frozen=True)
class ConcurrencyDefaults:
    MAX_WORKERS = 2
    DEFAULT_BATCH_SIZE = 100


@dataclass(frozen=True)
class ApiDefaults:
    DEFAULT_PAGE_SIZE = 100


@dataclass(frozen=True)
class BackupSettings(ConcurrencyDefaults, ApiDefaults):
    MAX_RETRIES = 3
    RETRY_DELAY = 5  # seconds
    TIMESTAMP_SDK_FOLDER = (
        str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
        + "-"
        + sdk_version.replace(".", "_")
    )
