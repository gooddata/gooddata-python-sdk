from gooddata_api_client.paths.api_v1_entities_csp_directives_id.get import ApiForget
from gooddata_api_client.paths.api_v1_entities_csp_directives_id.put import ApiForput
from gooddata_api_client.paths.api_v1_entities_csp_directives_id.delete import ApiFordelete
from gooddata_api_client.paths.api_v1_entities_csp_directives_id.patch import ApiForpatch


class ApiV1EntitiesCspDirectivesId(
    ApiForget,
    ApiForput,
    ApiFordelete,
    ApiForpatch,
):
    pass
