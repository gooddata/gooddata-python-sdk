# (C) 2025 GoodData Corporation

"""Module for exceptions used in GoodData Pipelines provisioning."""

from gooddata_pipelines.provisioning.utils.utils import AttributesMixin


# TODO: Use the generic context exception and phase out the specific ones
#  - we don't need to conform to process-specific schema anymore
class ContextException(Exception, AttributesMixin):
    def __init__(
        self, message: str, *context_objects: object, **kwargs: str
    ) -> None:
        """Exception raised during context processing."""
        super().__init__(message)
        attributes = self.get_attrs(*context_objects, overrides=kwargs)

        for key, value in attributes.items():
            setattr(self, key, value)


class ProvisioningException(Exception, AttributesMixin):
    def __init__(
        self, message: str, *context_objects: object, **kwargs: str
    ) -> None:
        """Exception raised during provisioning."""
        super().__init__(message)
        self.attributes = self.get_attrs(*context_objects, overrides=kwargs)
        self.error_message: str = message


class WorkspaceException(ProvisioningException):
    def __init__(
        self,
        message: str,
        *context_objects: object,
        **kwargs: str,
    ) -> None:
        """Exception raised during workspace provisioning."""
        super().__init__(message, *context_objects, **kwargs)

        self.http_status: str = self.attributes.get(
            "http_status", "500 Internal Server Error"
        )
        self.http_method: str | None = self.attributes.get("http_method", "NA")
        self.workspace_id: str = self.attributes.get("workspace_id", "NA")
        self.workspace_name: str | None = self.attributes.get(
            "workspace_name", "NA"
        )
        self.wdf_id: str | None = self.attributes.get("wdf_id", None)
        self.wdf_values: str | None = self.attributes.get("wdf_values", None)
        self.api_endpoint: str = self.attributes.get(
            "api_endpoint", "workspace_provisioning"
        )


class WorkspaceDataIntegrityException(WorkspaceException):
    def __init__(
        self, message: str, *context_objects: object, **kwargs: str
    ) -> None:
        """Exception raised during workspace validation."""
        super().__init__(message, *context_objects, **kwargs)

        self.workspace_id: str = self.attributes.get("workspace_id", "NA")
        self.workspace_name: str | None = self.attributes.get(
            "workspace_name", None
        )
        self.wdf_id: str | None = self.attributes.get("wdf_id", None)
        self.wdf_values: str | None = self.attributes.get("wdf_values", None)
        self.api_endpoint: str = self.attributes.get(
            "api_endpoint", "workspace_data_validation"
        )


class BaseUserException(ProvisioningException):
    def __init__(
        self, message: str, *context_objects: object, **kwargs: str
    ) -> None:
        """Exception raised during user provisioning."""
        super().__init__(message, *context_objects, **kwargs)

        self.http_status: str = self.attributes.get(
            "http_status", "500 Internal Server Error"
        )
        self.http_method: str | None = self.attributes.get("http_method", None)
        self.workspace_id: str | None = self.attributes.get(
            "workspace_id", None
        )
        self.user_id: str | None = self.attributes.get("user_id", None)
        self.user_group_id: str | None = self.attributes.get(
            "user_group_id", None
        )
        self.api_endpoint: str = self.attributes.get(
            "api_endpoint", "user_provisioning"
        )
