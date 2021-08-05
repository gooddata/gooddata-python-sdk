
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from .api.data_source_actions_controller_api import DataSourceActionsControllerApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from gooddata_metadata_client.api.data_source_actions_controller_api import DataSourceActionsControllerApi
from gooddata_metadata_client.api.data_source_entities_controller_api import DataSourceEntitiesControllerApi
from gooddata_metadata_client.api.data_source_layout_controller_api import DataSourceLayoutControllerApi
from gooddata_metadata_client.api.declarative_layout_controller_api import DeclarativeLayoutControllerApi
from gooddata_metadata_client.api.options_controller_api import OptionsControllerApi
from gooddata_metadata_client.api.organization_controller_api import OrganizationControllerApi
from gooddata_metadata_client.api.organization_model_controller_api import OrganizationModelControllerApi
from gooddata_metadata_client.api.organization_redirect_controller_api import OrganizationRedirectControllerApi
from gooddata_metadata_client.api.user_model_controller_api import UserModelControllerApi
from gooddata_metadata_client.api.workspace_object_controller_api import WorkspaceObjectControllerApi
