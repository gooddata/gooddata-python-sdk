from gooddata_api_client.paths.api_v1_entities_data_sources_id.get import ApiForget
from gooddata_api_client.paths.api_v1_entities_data_sources_id.put import ApiForput
from gooddata_api_client.paths.api_v1_entities_data_sources_id.delete import ApiFordelete
from gooddata_api_client.paths.api_v1_entities_data_sources_id.patch import ApiForpatch


class ApiV1EntitiesDataSourcesId(
    ApiForget,
    ApiForput,
    ApiFordelete,
    ApiForpatch,
):
    pass
