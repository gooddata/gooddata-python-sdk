# (C) 2025 GoodData Corporation

from typing import Any

from gooddata_pipelines.logger import LoggerLike
from gooddata_pipelines.provisioning.generic.config import (
    PROVISIONING_CONFIG,
    LoadType,
    WorkflowType,
)


def provision(
    data: list[dict[str, Any]],
    workflow_type: WorkflowType,
    host: str,
    token: str,
    logger: LoggerLike | None = None,
) -> None:
    """Generic provisioning function accepting raw data and workflow type.

    The function will validate data based on the selected workflow type and run
    the corresponding provisioning in full or incremental mode.

    Args:
        data: List of dictionaries containing the data to be provisioned.
        workflow_type: The type of workflow to run.
        host: The host of the GoodData platform.
        token: The token for the GoodData platform.
        logger: The logger to use for logging.
    """

    if workflow_type not in PROVISIONING_CONFIG:
        raise ValueError(f"Invalid workflow type: {workflow_type}")

    config = PROVISIONING_CONFIG[workflow_type]

    provisioner = config.provisioner_class.create(host, token)
    validated_data: list = [config.validation_model(**item) for item in data]

    if logger:
        provisioner.logger.subscribe(logger)

    if config.load_type == LoadType.FULL:
        provisioner.full_load(validated_data)
    elif config.load_type == LoadType.INCREMENTAL:
        provisioner.incremental_load(validated_data)
    else:
        raise ValueError(f"Invalid load type: {config.load_type}")
