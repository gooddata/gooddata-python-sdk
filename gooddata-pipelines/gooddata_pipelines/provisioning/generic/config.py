# (C) 2025 GoodData Corporation

from enum import Enum
from typing import Type, TypeAlias

import attrs

from gooddata_pipelines.provisioning.entities.users.models.permissions import (
    PermissionFullLoad,
    PermissionIncrementalLoad,
)
from gooddata_pipelines.provisioning.entities.users.models.user_groups import (
    UserGroupFullLoad,
    UserGroupIncrementalLoad,
)
from gooddata_pipelines.provisioning.entities.users.models.users import (
    UserFullLoad,
    UserIncrementalLoad,
)
from gooddata_pipelines.provisioning.entities.users.permissions import (
    PermissionProvisioner,
)
from gooddata_pipelines.provisioning.entities.users.user_groups import (
    UserGroupProvisioner,
)
from gooddata_pipelines.provisioning.entities.users.users import UserProvisioner
from gooddata_pipelines.provisioning.entities.workspaces.models import (
    WorkspaceFullLoad,
    WorkspaceIncrementalLoad,
)
from gooddata_pipelines.provisioning.entities.workspaces.workspace import (
    WorkspaceProvisioner,
)

ValidationModel: TypeAlias = (
    PermissionFullLoad
    | PermissionIncrementalLoad
    | UserFullLoad
    | UserIncrementalLoad
    | UserGroupFullLoad
    | UserGroupIncrementalLoad
    | WorkspaceFullLoad
    | WorkspaceIncrementalLoad
)

Provisioner: TypeAlias = (
    PermissionProvisioner
    | UserProvisioner
    | UserGroupProvisioner
    | WorkspaceProvisioner
)


class LoadType(str, Enum):
    FULL = "full"
    INCREMENTAL = "incremental"


class WorkflowType(str, Enum):
    WORKSPACE_FULL_LOAD = "workspace_full_load"
    WORKSPACE_INCREMENTAL_LOAD = "workspace_incremental_load"
    USER_FULL_LOAD = "user_full_load"
    USER_INCREMENTAL_LOAD = "user_incremental_load"
    USER_GROUP_FULL_LOAD = "user_group_full_load"
    USER_GROUP_INCREMENTAL_LOAD = "user_group_incremental_load"
    PERMISSION_FULL_LOAD = "permission_full_load"
    PERMISSION_INCREMENTAL_LOAD = "permission_incremental_load"


@attrs.define
class ProvisioningConfig:
    validation_model: Type[ValidationModel]
    provisioner_class: Type[Provisioner]
    load_type: LoadType


PROVISIONING_CONFIG = {
    WorkflowType.WORKSPACE_FULL_LOAD: ProvisioningConfig(
        validation_model=WorkspaceFullLoad,
        provisioner_class=WorkspaceProvisioner,
        load_type=LoadType.FULL,
    ),
    WorkflowType.WORKSPACE_INCREMENTAL_LOAD: ProvisioningConfig(
        validation_model=WorkspaceIncrementalLoad,
        provisioner_class=WorkspaceProvisioner,
        load_type=LoadType.INCREMENTAL,
    ),
    WorkflowType.USER_FULL_LOAD: ProvisioningConfig(
        validation_model=UserFullLoad,
        provisioner_class=UserProvisioner,
        load_type=LoadType.FULL,
    ),
    WorkflowType.USER_INCREMENTAL_LOAD: ProvisioningConfig(
        validation_model=UserIncrementalLoad,
        provisioner_class=UserProvisioner,
        load_type=LoadType.INCREMENTAL,
    ),
    WorkflowType.USER_GROUP_FULL_LOAD: ProvisioningConfig(
        validation_model=UserGroupFullLoad,
        provisioner_class=UserGroupProvisioner,
        load_type=LoadType.FULL,
    ),
    WorkflowType.USER_GROUP_INCREMENTAL_LOAD: ProvisioningConfig(
        validation_model=UserGroupIncrementalLoad,
        provisioner_class=UserGroupProvisioner,
        load_type=LoadType.INCREMENTAL,
    ),
    WorkflowType.PERMISSION_FULL_LOAD: ProvisioningConfig(
        validation_model=PermissionFullLoad,
        provisioner_class=PermissionProvisioner,
        load_type=LoadType.FULL,
    ),
    WorkflowType.PERMISSION_INCREMENTAL_LOAD: ProvisioningConfig(
        validation_model=PermissionIncrementalLoad,
        provisioner_class=PermissionProvisioner,
        load_type=LoadType.INCREMENTAL,
    ),
}
