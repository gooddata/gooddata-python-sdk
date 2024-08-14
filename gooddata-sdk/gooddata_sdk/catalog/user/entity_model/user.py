# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Optional

import attr
from gooddata_api_client.model.json_api_user_in import JsonApiUserIn
from gooddata_api_client.model.json_api_user_in_document import JsonApiUserInDocument

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.user.entity_model.user_group import CatalogUserGroup


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserDocument(Base):
    data: CatalogUser

    @staticmethod
    def client_class() -> type[JsonApiUserInDocument]:
        return JsonApiUserInDocument

    @classmethod
    def init(
        cls,
        user_id: str,
        firstname: Optional[str] = None,
        lastname: Optional[str] = None,
        email: Optional[str] = None,
        authentication_id: Optional[str] = None,
        user_group_ids: Optional[list[str]] = None,
    ) -> CatalogUserDocument:
        user = CatalogUser.init(
            user_id=user_id,
            firstname=firstname,
            lastname=lastname,
            email=email,
            authentication_id=authentication_id,
            user_group_ids=user_group_ids,
        )

        return cls(data=user)

    def update_user(
        self,
        firstname: Optional[str] = None,
        lastname: Optional[str] = None,
        email: Optional[str] = None,
        authentication_id: Optional[str] = None,
        user_group_ids: Optional[list[str]] = None,
    ) -> None:
        attributes = CatalogUserAttributes(
            firstname=firstname, lastname=lastname, email=email, authentication_id=authentication_id
        )
        relationships = CatalogUserRelationships.create_user_relationships(user_group_ids=user_group_ids)
        self.data.attributes = attributes
        self.data.relationships = relationships


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUser(Base):
    id: str
    attributes: Optional[CatalogUserAttributes] = None
    relationships: Optional[CatalogUserRelationships] = None

    @staticmethod
    def client_class() -> type[JsonApiUserIn]:
        return JsonApiUserIn

    @classmethod
    def init(
        cls,
        user_id: str,
        firstname: Optional[str] = None,
        lastname: Optional[str] = None,
        email: Optional[str] = None,
        authentication_id: Optional[str] = None,
        user_group_ids: Optional[list[str]] = None,
    ) -> CatalogUser:
        attributes = CatalogUserAttributes(
            firstname=firstname, lastname=lastname, email=email, authentication_id=authentication_id
        )
        relationships = CatalogUserRelationships.create_user_relationships(user_group_ids=user_group_ids)
        return cls(id=user_id, attributes=attributes, relationships=relationships)

    @property
    def user_groups(self) -> list[CatalogUserGroup]:
        """Get method for the user_groups stored in relationships with the user.

        Returns:
            list[CatalogUserGroup]:
                List of User Groups
        """
        if self.relationships and self.relationships.user_groups:
            return self.relationships.user_groups.data
        return []

    def add_user_group(self, user_group: CatalogUserGroup) -> None:
        """Adds a User Group to the relationships variable.

        Args:
            user_group (CatalogUserGroup):
                User Group to be added.
        Returns:
            None
        """
        if not self.relationships:
            self.relationships = CatalogUserRelationships(user_groups=CatalogUserGroupsData(data=[user_group]))
        else:
            self.relationships.add_user_groups([user_group])

    def add_user_groups(self, user_groups: list[CatalogUserGroup]) -> None:
        """Adds multiple User Groups to the relationship with the user.

        Args:
            user_groups (list[CatalogUserGroup]):
                User Groups to be added.
        Returns:
            None
        """
        if not self.relationships:
            self.relationships = CatalogUserRelationships(user_groups=CatalogUserGroupsData(data=user_groups))
        else:
            self.relationships.add_user_groups(user_groups)

    def remove_user_groups(self) -> None:
        """Clears the User Group from the relationship with the user.

        Returns:
            None
        """
        if self.relationships:
            self.relationships.user_groups = None

    def replace_user_groups(self, user_groups: list[CatalogUserGroup]) -> None:
        """Replaces the User Groups in the relationships variable.

        Args:
            user_groups (list[CatalogUserGroup]):
                New User Groups to be put into relationship with the user.
        Returns:
            None
        """
        if not self.relationships:
            self.relationships = CatalogUserRelationships(user_groups=CatalogUserGroupsData(data=user_groups))
        else:
            self.relationships.replace_user_groups(user_groups)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserAttributes(Base):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    authentication_id: Optional[str] = None


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserRelationships(Base):
    user_groups: Optional[CatalogUserGroupsData] = None

    def add_user_groups(self, user_groups: list[CatalogUserGroup]) -> None:
        """Appends the User Groups to the existing list.

        Args:
            user_groups (list[CatalogUserGroup]):
                User Groups to be added.
        Returns:
            None
        """
        if not self.user_groups:
            self.user_groups = CatalogUserGroupsData(data=user_groups)
        else:
            self.user_groups.data.extend(user_groups)

    def replace_user_groups(self, user_groups: list[CatalogUserGroup]) -> None:
        """Replace the User Groups in the relationship with the user.

        Args:
            user_groups (list[CatalogUserGroup]):
                User Groups to replace the old one.
        Returns:
            None
        """
        if not self.user_groups:
            self.user_groups = CatalogUserGroupsData(data=user_groups)
        else:
            self.user_groups.data = user_groups

    @classmethod
    def create_user_relationships(cls, user_group_ids: Optional[list[str]]) -> CatalogUserRelationships:
        user_groups = None
        if user_group_ids is not None:
            user_groups = CatalogUserGroupsData(
                data=[CatalogUserGroup(id=user_group_id) for user_group_id in user_group_ids]
            )
        return cls(user_groups=user_groups)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserGroupsData(Base):
    data: list[CatalogUserGroup] = attr.field(factory=list)
