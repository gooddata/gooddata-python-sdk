from gooddata_api_client.paths.api_v1_entities_themes_id.get import ApiForget
from gooddata_api_client.paths.api_v1_entities_themes_id.put import ApiForput
from gooddata_api_client.paths.api_v1_entities_themes_id.delete import ApiFordelete
from gooddata_api_client.paths.api_v1_entities_themes_id.patch import ApiForpatch


class ApiV1EntitiesThemesId(
    ApiForget,
    ApiForput,
    ApiFordelete,
    ApiForpatch,
):
    pass
