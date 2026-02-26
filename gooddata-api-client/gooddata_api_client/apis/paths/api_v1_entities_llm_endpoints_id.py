from gooddata_api_client.paths.api_v1_entities_llm_endpoints_id.get import ApiForget
from gooddata_api_client.paths.api_v1_entities_llm_endpoints_id.put import ApiForput
from gooddata_api_client.paths.api_v1_entities_llm_endpoints_id.delete import ApiFordelete
from gooddata_api_client.paths.api_v1_entities_llm_endpoints_id.patch import ApiForpatch


class ApiV1EntitiesLlmEndpointsId(
    ApiForget,
    ApiForput,
    ApiFordelete,
    ApiForpatch,
):
    pass
