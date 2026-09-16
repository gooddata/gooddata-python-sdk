# (C) 2025 GoodData Corporation
"""Direct imports of the generated API classes used by the SDK.

``gooddata_api_client.apis`` eagerly imports all ~130 generated API classes, which in turn
pulls in nearly every generated model. The SDK only ever instantiates the six classes
re-exported here, so importing their leaf modules keeps ``import gooddata_sdk`` cheap.
"""

from gooddata_api_client.api.actions_api import ActionsApi
from gooddata_api_client.api.ai_lake_api import AILakeApi
from gooddata_api_client.api.appearance_api import AppearanceApi
from gooddata_api_client.api.entities_api import EntitiesApi
from gooddata_api_client.api.layout_api import LayoutApi
from gooddata_api_client.api.user_management_api import UserManagementApi

__all__ = [
    "ActionsApi",
    "AILakeApi",
    "AppearanceApi",
    "EntitiesApi",
    "LayoutApi",
    "UserManagementApi",
]
