# coding: utf-8

"""
    OpenAPI definition

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v0
    Contact: support@gooddata.com
    Generated by: https://openapi-generator.tech
"""

from gooddata_api_client.paths.api_v1_entities_users_user_id_api_tokens.post import CreateEntityApiTokens
from gooddata_api_client.paths.api_v1_entities_users_user_id_user_settings.post import CreateEntityUserSettings
from gooddata_api_client.paths.api_v1_entities_users_user_id_api_tokens_id.delete import DeleteEntityApiTokens
from gooddata_api_client.paths.api_v1_entities_users_user_id_user_settings_id.delete import DeleteEntityUserSettings
from gooddata_api_client.paths.api_v1_entities_users_user_id_api_tokens.get import GetAllEntitiesApiTokens
from gooddata_api_client.paths.api_v1_entities_users_user_id_user_settings.get import GetAllEntitiesUserSettings
from gooddata_api_client.paths.api_v1_entities_users_user_id_api_tokens_id.get import GetEntityApiTokens
from gooddata_api_client.paths.api_v1_entities_users_user_id_user_settings_id.get import GetEntityUserSettings
from gooddata_api_client.paths.api_v1_entities_users_user_id_api_tokens_id.put import UpdateEntityApiTokens
from gooddata_api_client.paths.api_v1_entities_users_user_id_user_settings_id.put import UpdateEntityUserSettings


class UserModelControllerApi(
    CreateEntityApiTokens,
    CreateEntityUserSettings,
    DeleteEntityApiTokens,
    DeleteEntityUserSettings,
    GetAllEntitiesApiTokens,
    GetAllEntitiesUserSettings,
    GetEntityApiTokens,
    GetEntityUserSettings,
    UpdateEntityApiTokens,
    UpdateEntityUserSettings,
):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    pass
