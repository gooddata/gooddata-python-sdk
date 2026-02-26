from gooddata_api_client.paths.api_v1_entities_identity_providers_id.get import ApiForget
from gooddata_api_client.paths.api_v1_entities_identity_providers_id.put import ApiForput
from gooddata_api_client.paths.api_v1_entities_identity_providers_id.delete import ApiFordelete
from gooddata_api_client.paths.api_v1_entities_identity_providers_id.patch import ApiForpatch


class ApiV1EntitiesIdentityProvidersId(
    ApiForget,
    ApiForput,
    ApiFordelete,
    ApiForpatch,
):
    pass
