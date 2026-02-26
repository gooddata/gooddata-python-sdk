from gooddata_api_client.paths.api_v1_entities_jwks_id.get import ApiForget
from gooddata_api_client.paths.api_v1_entities_jwks_id.put import ApiForput
from gooddata_api_client.paths.api_v1_entities_jwks_id.delete import ApiFordelete
from gooddata_api_client.paths.api_v1_entities_jwks_id.patch import ApiForpatch


class ApiV1EntitiesJwksId(
    ApiForget,
    ApiForput,
    ApiFordelete,
    ApiForpatch,
):
    pass
