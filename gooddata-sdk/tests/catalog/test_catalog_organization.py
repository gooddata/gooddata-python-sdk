# (C) 2022 GoodData Corporation
from __future__ import annotations

from pathlib import Path

from tests_support.vcrpy_utils import get_vcr

from gooddata_sdk import CatalogOrganization, GoodDataSdk

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures" / "organization"


def _default_organization_check(organization: CatalogOrganization):
    assert organization.id == "default"
    assert organization.attributes.name == "Default Organization"
    assert organization.attributes.hostname == "localhost"


@gd_vcr.use_cassette(str(_fixtures_dir / "organization.yaml"))
def test_get_organization(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    organization = sdk.catalog_organization.get_organization()
    _default_organization_check(organization)


@gd_vcr.use_cassette(str(_fixtures_dir / "update_oidc_settings.yaml"))
def test_update_oidc_settings(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    organization = sdk.catalog_organization.get_organization()
    _default_organization_check(organization)

    oauth_issuer_location = "test.com"
    oauth_client_id = "123456"
    oauth_client_secret = "password"

    try:
        sdk.catalog_organization.update_oidc_parameters(
            oauth_issuer_location=oauth_issuer_location,
            oauth_client_id=oauth_client_id,
            oauth_client_secret=oauth_client_secret,
        )

        updated_organization = sdk.catalog_organization.get_organization()
        _default_organization_check(updated_organization)
        assert updated_organization.attributes.oauth_issuer_location == oauth_issuer_location
        assert updated_organization.attributes.oauth_client_id == oauth_client_id

    finally:
        sdk.catalog_organization.update_oidc_parameters(
            oauth_issuer_location=None, oauth_client_id=None, oauth_client_secret=None
        )

        revert_organization = sdk.catalog_organization.get_organization()
        _default_organization_check(revert_organization)


@gd_vcr.use_cassette(str(_fixtures_dir / "update_name.yaml"))
def test_update_name(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    organization = sdk.catalog_organization.get_organization()
    _default_organization_check(organization)
    default_name = organization.attributes.name
    new_name = "test_organization"

    try:
        sdk.catalog_organization.update_name(new_name)
        updated_organization = sdk.catalog_organization.get_organization()
        assert updated_organization.id == organization.id
        assert updated_organization.attributes.name == new_name
        assert updated_organization.attributes.hostname == organization.attributes.hostname
    finally:
        sdk.catalog_organization.update_name(default_name)
        organization = sdk.catalog_organization.get_organization()
        _default_organization_check(organization)
