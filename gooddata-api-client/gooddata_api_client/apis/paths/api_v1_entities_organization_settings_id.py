from gooddata_api_client.paths.api_v1_entities_organization_settings_id.get import ApiForget
from gooddata_api_client.paths.api_v1_entities_organization_settings_id.put import ApiForput
from gooddata_api_client.paths.api_v1_entities_organization_settings_id.delete import ApiFordelete
from gooddata_api_client.paths.api_v1_entities_organization_settings_id.patch import ApiForpatch


class ApiV1EntitiesOrganizationSettingsId(
    ApiForget,
    ApiForput,
    ApiFordelete,
    ApiForpatch,
):
    pass
