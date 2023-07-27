from gooddata_api_client.paths.api_v1_entities_workspaces_id.get import ApiForget
from gooddata_api_client.paths.api_v1_entities_workspaces_id.put import ApiForput
from gooddata_api_client.paths.api_v1_entities_workspaces_id.delete import ApiFordelete
from gooddata_api_client.paths.api_v1_entities_workspaces_id.patch import ApiForpatch


class ApiV1EntitiesWorkspacesId(
    ApiForget,
    ApiForput,
    ApiFordelete,
    ApiForpatch,
):
    pass
