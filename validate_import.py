import sys
sys.path.insert(0, '/home/runner/_work/gdc-nas/gdc-nas/sdk/packages/gooddata-sdk/src')
sys.path.insert(0, '/home/runner/_work/gdc-nas/gdc-nas/sdk/packages/gooddata-api-client/src')
import gooddata_sdk
print('Import OK')
from gooddata_sdk import CatalogWorkspaceParameter, CatalogNumberParameterDefinition, CatalogWorkspaceParameterConstraints
print('Parameter exports OK')
