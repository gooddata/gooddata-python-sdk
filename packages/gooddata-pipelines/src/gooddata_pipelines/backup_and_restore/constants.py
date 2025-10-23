# (C) 2025 GoodData Corporation
import datetime

import attrs
from gooddata_sdk._version import __version__ as sdk_version


@attrs.frozen
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


@attrs.frozen
class ApiDefaults:
    PAGE_SIZE = 100
    BATCH_SIZE = 100
    CALLS_PER_SECOND = 1.0


@attrs.frozen
class BackupSettings:
    API = ApiDefaults()
    MAX_RETRIES = 3
    RETRY_DELAY = 5  # seconds
    TIMESTAMP_SDK_FOLDER = (
        str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
        + "-"
        + sdk_version.replace(".", "_")
    )
