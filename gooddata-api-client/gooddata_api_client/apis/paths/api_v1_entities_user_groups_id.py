from gooddata_api_client.paths.api_v1_entities_user_groups_id.get import ApiForget
from gooddata_api_client.paths.api_v1_entities_user_groups_id.put import ApiForput
from gooddata_api_client.paths.api_v1_entities_user_groups_id.delete import ApiFordelete
from gooddata_api_client.paths.api_v1_entities_user_groups_id.patch import ApiForpatch


class ApiV1EntitiesUserGroupsId(
    ApiForget,
    ApiForput,
    ApiFordelete,
    ApiForpatch,
):
    pass
