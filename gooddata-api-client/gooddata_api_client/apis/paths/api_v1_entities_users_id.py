from gooddata_api_client.paths.api_v1_entities_users_id.get import ApiForget
from gooddata_api_client.paths.api_v1_entities_users_id.put import ApiForput
from gooddata_api_client.paths.api_v1_entities_users_id.delete import ApiFordelete
from gooddata_api_client.paths.api_v1_entities_users_id.patch import ApiForpatch


class ApiV1EntitiesUsersId(
    ApiForget,
    ApiForput,
    ApiFordelete,
    ApiForpatch,
):
    pass
