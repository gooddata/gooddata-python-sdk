# (C) 2022 GoodData Corporation
from __future__ import annotations

from pathlib import Path

from gooddata_api_client.exceptions import NotFoundException
from gooddata_sdk import (
    CatalogCspDirective,
    CatalogJwk,
    CatalogOrganization,
    CatalogOrganizationSetting,
    CatalogRsaSpecification,
    GoodDataSdk,
)
from tests_support.vcrpy_utils import get_vcr

gd_vcr = get_vcr()

_default_jwk_id = "demoJwk"
_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures" / "organization"


def _default_organization_check(organization: CatalogOrganization):
    assert organization.id == "default"
    assert organization.attributes.name == "Default Organization"
    assert organization.attributes.hostname == "localhost"


def _default_jwk(jwk_id=_default_jwk_id, alg=None, kid=None):
    rsa_specification = CatalogRsaSpecification(
        alg=alg if alg else "RS256",
        kid=kid if kid else "Gkncy6f9BSp7wdav8w4SNZE1yt0",
        use="sig",
        kty="RSA",
        e="AQAB",
        n="sXiw5dOOl6DwAFKYQP623hUOs7T0f2mJEvMN1P-AkVbwagxanJzyRpJJX2zyXtIYnsTrlsjrSRzBTvWBZCXGW4XpmcSIKoRky_hBJGgK6shK"
        "3375oThcAq01JZWEWXU2roYyBQz7VxvUSIAPmQVXn9TCQ7YT_TQOg39Dzot2PZPZtabKM2IQEtV6vVmciqz3QkMnclvGnUAca6KZCPBotdNX"
        "9dWedAOBHmipCzzYIHutnMXsTZtPCEvrlgYyS1yD7u1WaxPgl84D6uglqDBF6WF1Vr2fgeeWfyujiJ_U26BCq6DmGQCN7BPAhJJso6bvP27G"
        "58wZGR3HM_bjJ716Zw",
        x5c=[
            "MIIDbjCCAlagAwIBAgIUQ/BwWYGeDkDQjbUycWZqI/FeUDcwDQYJKoZIhvcNAQELBQAwZDELMAkGA1UEBhMCVVMxEzARBgNVBAgMCkNhbG"
            "lmb3JuaWExFjAUBgNVBAcMDVNhbiBGcmFuY2lzY28xETAPBgNVBAoMCEdvb2REYXRhMRUwEwYDVQQDDAxnb29kZGF0YS5jb20wHhcNMjMw"
            "ODE2MTM1NDMyWhcNMjMwOTE1MTM1NDMyWjBkMQswCQYDVQQGEwJVUzETMBEGA1UECAwKQ2FsaWZvcm5pYTEWMBQGA1UEBwwNU2FuIEZyYW"
            "5jaXNjbzERMA8GA1UECgwIR29vZERhdGExFTATBgNVBAMMDGdvb2RkYXRhLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEB"
            "ALF4sOXTjpeg8ABSmED+tt4VDrO09H9piRLzDdT/gJFW8GoMWpyc8kaSSV9s8l7SGJ7E65bI60kcwU71gWQlxluF6ZnEiCqEZMv4QSRoCu"
            "rISt9++aE4XAKtNSWVhFl1Nq6GMgUM+1cb1EiAD5kFV5/UwkO2E/00DoN/Q86Ldj2T2bWmyjNiEBLVer1ZnIqs90JDJ3Jbxp1AHGuimQjw"
            "aLXTV/XVnnQDgR5oqQs82CB7rZzF7E2bTwhL65YGMktcg+7tVmsT4JfOA+roJagwRelhdVa9n4Hnln8ro4if1NugQqug5hkAjewTwISSbK"
            "Om7z9uxufMGRkdxzP24ye9emcCAwEAAaMYMBYwFAYDVR0RBA0wC4IJbG9jYWxob3N0MA0GCSqGSIb3DQEBCwUAA4IBAQA2j3W4+qAkp0K6"
            "WP0gogMhqToJCx4/ojRdJ0hJeoIluIAiTzL3uDmG+85xbQ758qD6Ya1Mty6aPdNekFxYlUmulhYY+2Sdby6ChQIUgS9wj1sNFuo4e3U3JV"
            "pBfdtJq3diNTcEO/iNWds9MRtNzmrkRIDxAyZvB79Ghuq8i+J9OQ1Na0MEDqKD+KrW0eLT661sT0HgBJCyZaDFQHaiFs3GXEP2QMseMXZu"
            "uhLrg8im7DsO+skQtIWH02x6xxKgj/o5bRmoU4ArOzYRWehrrj+pEeAEIVStLzSnhl4v4ovrQ7P5YbeHLFvmw6rb0wp0HYmuZIvA+wJa0u"
            "azJjfzjv3a"
        ],
        x5t="tGg2yZgC0sVyvaK49GenyQB7cuA",
    )
    return CatalogJwk.init(jwk_id=jwk_id, rsa_spec=rsa_specification)


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


@gd_vcr.use_cassette(str(_fixtures_dir / "create_jwk.yaml"))
def test_create_jwk(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    new_jwk = _default_jwk()
    try:
        sdk.catalog_organization.create_or_update_jwk(new_jwk)
        created_jwk = sdk.catalog_organization.get_jwk("demoJwk")
        assert new_jwk.id == created_jwk.id
        assert new_jwk.attributes == created_jwk.attributes
    finally:
        sdk.catalog_organization.delete_jwk("demoJwk")
        assert len(sdk.catalog_organization.list_jwks()) == 0


@gd_vcr.use_cassette(str(_fixtures_dir / "update_jwk.yaml"))
def test_update_jwk(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    new_jwk = _default_jwk()
    update_jwk = _default_jwk(alg="RS384")
    try:
        sdk.catalog_organization.create_or_update_jwk(new_jwk)
        sdk.catalog_organization.create_or_update_jwk(update_jwk)
        updated_jwk = sdk.catalog_organization.get_jwk("demoJwk")
        assert update_jwk.attributes.content.alg == updated_jwk.attributes.content.alg
    finally:
        sdk.catalog_organization.delete_jwk("demoJwk")
        assert len(sdk.catalog_organization.list_jwks()) == 0


@gd_vcr.use_cassette(str(_fixtures_dir / "delete_jwk.yaml"))
def test_delete_jwk(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    jwk = _default_jwk()
    try:
        sdk.catalog_organization.create_or_update_jwk(jwk)
        sdk.catalog_organization.delete_jwk(jwk.id)
        sdk.catalog_organization.get_jwk(jwk.id)
    except NotFoundException:
        assert len(sdk.catalog_organization.list_jwks()) == 0
    finally:
        assert len(sdk.catalog_organization.list_jwks()) == 0


@gd_vcr.use_cassette(str(_fixtures_dir / "list_jwk.yaml"))
def test_list_jwk(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    jwk1 = _default_jwk(jwk_id="demoJwk1", kid="kid1")
    jwk2 = _default_jwk(jwk_id="demoJwk2", kid="kid2")
    try:
        sdk.catalog_organization.create_or_update_jwk(jwk1)
        sdk.catalog_organization.create_or_update_jwk(jwk2)
        assert len(sdk.catalog_organization.list_jwks()) == 2
    finally:
        sdk.catalog_organization.delete_jwk(jwk1.id)
        sdk.catalog_organization.delete_jwk(jwk2.id)
        assert len(sdk.catalog_organization.list_jwks()) == 0


@gd_vcr.use_cassette(str(_fixtures_dir / "create_organization_setting.yaml"))
def test_create_organization_setting(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    setting_id = "test_setting"
    setting_type = "LOCALE"
    content = {"value": "fr-FR"}

    new_setting = CatalogOrganizationSetting.init(setting_id, setting_type, content)
    try:
        sdk.catalog_organization.create_organization_setting(new_setting)
        setting = sdk.catalog_organization.get_organization_setting(setting_id)
        assert setting.id == setting_id
        assert setting.attributes.type == setting_type
        assert setting.attributes.content == content
    finally:
        sdk.catalog_organization.delete_organization_setting(setting_id)
        assert len(sdk.catalog_organization.list_organization_settings()) == 0


@gd_vcr.use_cassette(str(_fixtures_dir / "list_organization_settings.yaml"))
def test_list_organization_settings(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    setting_id_1 = "test_setting_1"
    setting_id_2 = "test_setting_2"
    new_setting_1 = CatalogOrganizationSetting.init(setting_id_1, "LOCALE", {"value": "fr-FR"})
    new_setting_2 = CatalogOrganizationSetting.init(setting_id_2, "FORMAT_LOCALE", {"value": "en-GB"})

    try:
        sdk.catalog_organization.create_organization_setting(new_setting_1)
        sdk.catalog_organization.create_organization_setting(new_setting_2)
        organization_settings = sdk.catalog_organization.list_organization_settings()
        assert len(organization_settings) == 2
        assert new_setting_1 in organization_settings
        assert new_setting_2 in organization_settings
    finally:
        sdk.catalog_organization.delete_organization_setting(setting_id_1)
        sdk.catalog_organization.delete_organization_setting(setting_id_2)
        assert len(sdk.catalog_organization.list_organization_settings()) == 0


@gd_vcr.use_cassette(str(_fixtures_dir / "delete_organization_setting.yaml"))
def test_delete_organization_setting(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    setting_id = "test_setting"
    new_setting = CatalogOrganizationSetting.init(setting_id, "LOCALE", {"value": "fr-FR"})

    try:
        sdk.catalog_organization.create_organization_setting(new_setting)
        sdk.catalog_organization.delete_organization_setting(setting_id)
        sdk.catalog_organization.get_organization_setting(setting_id)
    except NotFoundException:
        assert len(sdk.catalog_organization.list_organization_settings()) == 0
    finally:
        assert len(sdk.catalog_organization.list_organization_settings()) == 0


@gd_vcr.use_cassette(str(_fixtures_dir / "update_organization_setting.yaml"))
def test_update_organization_setting(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    setting_id = "test_setting"
    new_setting = CatalogOrganizationSetting.init(setting_id, "LOCALE", {"value": "fr-FR"})
    update_setting = CatalogOrganizationSetting.init(setting_id, "LOCALE", {"value": "en-GB"})

    try:
        sdk.catalog_organization.create_organization_setting(new_setting)
        sdk.catalog_organization.update_organization_setting(update_setting)
        setting = sdk.catalog_organization.get_organization_setting(setting_id)
        assert setting.id == setting_id
        assert setting.attributes.type == "LOCALE"
        assert setting.attributes.content == {"value": "en-GB"}
    finally:
        sdk.catalog_organization.delete_organization_setting(setting_id)
        assert len(sdk.catalog_organization.list_organization_settings()) == 0


@gd_vcr.use_cassette(str(_fixtures_dir / "create_csp_directive.yaml"))
def test_create_csp_directive(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    directive_id = "font-src"
    sources = ["https://test.com"]

    new_csp_directive = CatalogCspDirective.init(directive_id, sources)
    try:
        sdk.catalog_organization.create_csp_directive(new_csp_directive)
        csp_directive = sdk.catalog_organization.get_csp_directive(directive_id)
        assert csp_directive.id == directive_id
        assert csp_directive.attributes.sources == sources
    finally:
        sdk.catalog_organization.delete_csp_directive(directive_id)
        assert len(sdk.catalog_organization.list_csp_directives()) == 0


@gd_vcr.use_cassette(str(_fixtures_dir / "list_csp_directives.yaml"))
def test_list_csp_directives(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    directive_id_1 = "font-src"
    directive_id_2 = "script-src"
    new_csp_directive_1 = CatalogCspDirective.init(directive_id_1, ["https://test.com"])
    new_csp_directive_2 = CatalogCspDirective.init(directive_id_2, ["https://test2.com"])

    try:
        sdk.catalog_organization.create_csp_directive(new_csp_directive_1)
        sdk.catalog_organization.create_csp_directive(new_csp_directive_2)
        csp_directives = sdk.catalog_organization.list_csp_directives()
        assert len(csp_directives) == 2
        assert new_csp_directive_1 in csp_directives
        assert new_csp_directive_2 in csp_directives
    finally:
        sdk.catalog_organization.delete_csp_directive(directive_id_1)
        sdk.catalog_organization.delete_csp_directive(directive_id_2)
        assert len(sdk.catalog_organization.list_csp_directives()) == 0


@gd_vcr.use_cassette(str(_fixtures_dir / "delete_csp_directive.yaml"))
def test_delete_csp_directive(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    directive_id = "font-src"
    new_csp_directive = CatalogCspDirective.init(directive_id, ["https://test.com"])

    try:
        sdk.catalog_organization.create_csp_directive(new_csp_directive)
        sdk.catalog_organization.delete_csp_directive(directive_id)
        sdk.catalog_organization.get_csp_directive(directive_id)
    except NotFoundException:
        assert len(sdk.catalog_organization.list_csp_directives()) == 0
    finally:
        assert len(sdk.catalog_organization.list_csp_directives()) == 0


@gd_vcr.use_cassette(str(_fixtures_dir / "update_csp_directive.yaml"))
def test_update_csp_directive(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    directive_id = "font-src"
    new_csp_directive = CatalogCspDirective.init(directive_id, ["https://test.com"])
    update_csp_directive = CatalogCspDirective.init(directive_id, ["https://test2.com"])

    try:
        sdk.catalog_organization.create_csp_directive(new_csp_directive)
        sdk.catalog_organization.update_csp_directive(update_csp_directive)
        csp_directive = sdk.catalog_organization.get_csp_directive(directive_id)
        assert csp_directive.id == directive_id
        assert csp_directive.attributes.sources == ["https://test2.com"]
    finally:
        sdk.catalog_organization.delete_csp_directive(directive_id)
        assert len(sdk.catalog_organization.list_csp_directives()) == 0


@gd_vcr.use_cassette(str(_fixtures_dir / "update_allowed_origins.yaml"))
def test_update_allowed_origins(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    allowed_origins = ["https://test.com"]

    try:
        sdk.catalog_organization.update_allowed_origins(allowed_origins)
        organization = sdk.catalog_organization.get_organization()
        assert organization.attributes.allowed_origins == allowed_origins
    finally:
        sdk.catalog_organization.update_allowed_origins([])
        organization = sdk.catalog_organization.get_organization()
        assert organization.attributes.allowed_origins == []
