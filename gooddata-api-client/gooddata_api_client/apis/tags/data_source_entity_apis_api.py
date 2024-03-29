# coding: utf-8

"""
    OpenAPI definition

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v0
    Contact: support@gooddata.com
    Generated by: https://openapi-generator.tech
"""

from gooddata_api_client.paths.api_v1_entities_data_sources.post import CreateEntityDataSources
from gooddata_api_client.paths.api_v1_entities_data_sources_id.delete import DeleteEntityDataSources
from gooddata_api_client.paths.api_v1_entities_data_source_identifiers.get import GetAllEntitiesDataSourceIdentifiers
from gooddata_api_client.paths.api_v1_entities_data_sources_data_source_id_data_source_tables.get import GetAllEntitiesDataSourceTables
from gooddata_api_client.paths.api_v1_entities_data_sources.get import GetAllEntitiesDataSources
from gooddata_api_client.paths.api_v1_entities_data_source_identifiers_id.get import GetEntityDataSourceIdentifiers
from gooddata_api_client.paths.api_v1_entities_data_sources_data_source_id_data_source_tables_id.get import GetEntityDataSourceTables
from gooddata_api_client.paths.api_v1_entities_data_sources_id.get import GetEntityDataSources
from gooddata_api_client.paths.api_v1_entities_data_sources_id.patch import PatchEntityDataSources
from gooddata_api_client.paths.api_v1_entities_data_sources_id.put import UpdateEntityDataSources


class DataSourceEntityAPIsApi(
    CreateEntityDataSources,
    DeleteEntityDataSources,
    GetAllEntitiesDataSourceIdentifiers,
    GetAllEntitiesDataSourceTables,
    GetAllEntitiesDataSources,
    GetEntityDataSourceIdentifiers,
    GetEntityDataSourceTables,
    GetEntityDataSources,
    PatchEntityDataSources,
    UpdateEntityDataSources,
):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    pass
