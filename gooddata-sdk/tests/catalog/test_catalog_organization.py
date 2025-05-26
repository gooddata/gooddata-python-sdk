# (C) 2022 GoodData Corporation
from __future__ import annotations

from pathlib import Path

from gooddata_api_client.exceptions import NotFoundException
from gooddata_sdk import (
    CatalogCspDirective,
    CatalogDeclarativeNotificationChannel,
    CatalogJwk,
    CatalogLlmEndpoint,
    CatalogOrganization,
    CatalogOrganizationSetting,
    CatalogRsaSpecification,
    CatalogWebhook,
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


@gd_vcr.use_cassette(str(_fixtures_dir / "layout_notification_channels.yaml"))
def test_layout_notification_channels(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    ncs = sdk.catalog_organization.get_declarative_notification_channels()
    assert len(ncs) == 0

    try:
        notification_channels_e = [
            CatalogDeclarativeNotificationChannel(
                id="webhook",
                name="Webhook",
                destination=CatalogWebhook(url="https://webhook.site", token="123"),
                custom_dashboard_url="https://dashboard.site",
                allowed_recipients="CREATOR",
            ),
        ]
        sdk.catalog_organization.put_declarative_notification_channels(notification_channels_e)
        notification_channels_o = sdk.catalog_organization.get_declarative_notification_channels()
        assert notification_channels_e[0].id == notification_channels_o[0].id
        assert notification_channels_e[0].name == notification_channels_o[0].name
        assert notification_channels_e[0].destination == notification_channels_o[0].destination
        assert notification_channels_e[0].custom_dashboard_url == notification_channels_o[0].custom_dashboard_url
        assert notification_channels_e[0].allowed_recipients == notification_channels_o[0].allowed_recipients
    finally:
        sdk.catalog_organization.put_declarative_notification_channels([])
        ncs = sdk.catalog_organization.get_declarative_notification_channels()
        assert len(ncs) == 0


@gd_vcr.use_cassette(str(_fixtures_dir / "get_llm_endpoint.yaml"))
def test_get_llm_endpoint(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    try:
        # Create test endpoint first
        test_id = "endpoint1"
        test_title = "Test Endpoint"
        test_token = "secret-token"

        sdk.catalog_organization.create_llm_endpoint(id=test_id, title=test_title, token=test_token)

        # Get and verify the endpoint
        retrieved_endpoint = sdk.catalog_organization.get_llm_endpoint(test_id)
        assert isinstance(retrieved_endpoint, CatalogLlmEndpoint)
        assert retrieved_endpoint.id == test_id
        assert retrieved_endpoint.attributes.title == test_title
        assert not retrieved_endpoint.attributes.token  # Token not returned for security

    finally:
        # Clean up
        sdk.catalog_organization.delete_llm_endpoint(test_id)


@gd_vcr.use_cassette(str(_fixtures_dir / "list_llm_endpoints.yaml"))
def test_list_llm_endpoints(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    try:
        # Create test endpoints first
        test_id1 = "endpoint1"
        test_title1 = "Test Endpoint 1"
        test_token1 = "secret-token-1"

        test_id2 = "endpoint2"
        test_title2 = "Test Endpoint 2"
        test_token2 = "secret-token-2"

        sdk.catalog_organization.create_llm_endpoint(id=test_id1, title=test_title1, token=test_token1)

        sdk.catalog_organization.create_llm_endpoint(id=test_id2, title=test_title2, token=test_token2)

        # Get and verify the endpoints list
        endpoints = sdk.catalog_organization.list_llm_endpoints()
        assert isinstance(endpoints, list)
        assert len(endpoints) == 2
        assert all(isinstance(endpoint, CatalogLlmEndpoint) for endpoint in endpoints)
        assert {endpoint.id for endpoint in endpoints} == {test_id1, test_id2}
        assert {endpoint.attributes.title for endpoint in endpoints} == {test_title1, test_title2}

        # Test with optional parameters
        filtered_endpoints = sdk.catalog_organization.list_llm_endpoints(filter="title=='Test Endpoint 1'", size=1)
        assert isinstance(filtered_endpoints, list)
        assert len(filtered_endpoints) == 1
        assert filtered_endpoints[0].id == test_id1
        assert filtered_endpoints[0].attributes.title == test_title1

    finally:
        # Clean up
        sdk.catalog_organization.delete_llm_endpoint(test_id1)
        sdk.catalog_organization.delete_llm_endpoint(test_id2)


@gd_vcr.use_cassette(str(_fixtures_dir / "create_llm_endpoint.yaml"))
def test_create_llm_endpoint(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    try:
        # Test minimal required parameters
        minimal_id = "endpoint1"
        minimal_title = "Test Endpoint"
        minimal_token = "secret-token"

        llm_endpoint_1 = sdk.catalog_organization.create_llm_endpoint(
            id=minimal_id, title=minimal_title, token=minimal_token
        )

        assert isinstance(llm_endpoint_1, CatalogLlmEndpoint)
        assert llm_endpoint_1.id == minimal_id
        assert llm_endpoint_1.attributes.title == minimal_title
        # Token is not returned in the API response for security reasons
        assert not llm_endpoint_1.attributes.token

        # Test with all optional parameters
        full_id = "endpoint2"
        full_title = "Test Endpoint 2"
        full_token = "secret-token-2"
        full_description = "Test Description"
        full_provider = "OPENAI"
        full_base_url = "https://api.example.com"
        full_llm_org = "org1"
        full_llm_model = "gpt-4"

        llm_endpoint_2 = sdk.catalog_organization.create_llm_endpoint(
            id=full_id,
            title=full_title,
            token=full_token,
            description=full_description,
            provider=full_provider,
            base_url=full_base_url,
            llm_organization=full_llm_org,
            llm_model=full_llm_model,
        )
        assert isinstance(llm_endpoint_2, CatalogLlmEndpoint)
        assert llm_endpoint_2.id == full_id
        assert llm_endpoint_2.attributes.title == full_title
        # Token is not returned in the API response for security reasons
        assert not llm_endpoint_2.attributes.token
        # Description is not returned in the API response. TODO: Check if this is correct.
        # assert llm_endpoint_2.attributes.description == full_description
        assert llm_endpoint_2.attributes.provider == full_provider
        assert llm_endpoint_2.attributes.base_url == full_base_url
        assert llm_endpoint_2.attributes.llm_organization == full_llm_org
        assert llm_endpoint_2.attributes.llm_model == full_llm_model
    finally:
        # Cleanup
        sdk.catalog_organization.delete_llm_endpoint(minimal_id)
        sdk.catalog_organization.delete_llm_endpoint(full_id)


@gd_vcr.use_cassette(str(_fixtures_dir / "update_llm_endpoint.yaml"))
def test_update_llm_endpoint(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    initial_id = "endpoint1"
    initial_title = "Initial Title"
    initial_token = "initial-token"

    try:
        # Create initial endpoint
        sdk.catalog_organization.create_llm_endpoint(id=initial_id, title=initial_title, token=initial_token)

        # Test with minimal update
        minimal_title = "Updated Title"

        llm_endpoint_1 = sdk.catalog_organization.update_llm_endpoint(id=initial_id, title=minimal_title)

        assert isinstance(llm_endpoint_1, CatalogLlmEndpoint)
        assert llm_endpoint_1.id == initial_id
        assert llm_endpoint_1.attributes.title == minimal_title
        # Token is not returned in the API response for security reasons
        assert not llm_endpoint_1.attributes.token

        # Test with all optional parameters
        full_title = "Updated Title 2"
        full_token = "new-token"
        full_description = "Updated Description"
        full_provider = "OPENAI"
        full_base_url = "https://api.updated.com"
        full_llm_org = "org2"
        full_llm_model = "gpt-3.5"

        llm_endpoint_2 = sdk.catalog_organization.update_llm_endpoint(
            id=initial_id,
            title=full_title,
            token=full_token,
            description=full_description,
            provider=full_provider,
            base_url=full_base_url,
            llm_organization=full_llm_org,
            llm_model=full_llm_model,
        )

        assert isinstance(llm_endpoint_2, CatalogLlmEndpoint)
        assert llm_endpoint_2.id == initial_id
        assert llm_endpoint_2.attributes.title == full_title
        # Token is not returned in the API response for security reasons
        assert not llm_endpoint_2.attributes.token
        # Description is not returned in the API response. TODO: Check if this is correct.
        # assert llm_endpoint_2.attributes.description == full_description
        assert llm_endpoint_2.attributes.provider == full_provider
        assert llm_endpoint_2.attributes.base_url == full_base_url
        assert llm_endpoint_2.attributes.llm_organization == full_llm_org
        assert llm_endpoint_2.attributes.llm_model == full_llm_model

        # Test that attributes are preserved when not provided
        new_title = "New Title"
        llm_endpoint_3 = sdk.catalog_organization.update_llm_endpoint(id=initial_id, title=new_title)

        assert isinstance(llm_endpoint_3, CatalogLlmEndpoint)
        assert llm_endpoint_3.id == initial_id
        assert llm_endpoint_3.attributes.title == new_title
        # Token is not returned in the API response for security reasons
        assert not llm_endpoint_3.attributes.token
        # Verify other fields are preserved
        # Description is not returned in the API response. TODO: Check if this is correct.
        # assert llm_endpoint_3.attributes.description == full_description
        assert llm_endpoint_3.attributes.provider == full_provider
        assert llm_endpoint_3.attributes.base_url == full_base_url
        assert llm_endpoint_3.attributes.llm_organization == full_llm_org
        assert llm_endpoint_3.attributes.llm_model == full_llm_model
    finally:
        # Cleanup
        sdk.catalog_organization.delete_llm_endpoint(initial_id)


@gd_vcr.use_cassette(str(_fixtures_dir / "delete_llm_endpoint.yaml"))
def test_delete_llm_endpoint(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    try:
        # Create endpoint to delete
        sdk.catalog_organization.create_llm_endpoint(id="endpoint1", title="Test Endpoint", token="secret-token")

        # Delete endpoint
        sdk.catalog_organization.delete_llm_endpoint("endpoint1")

        # Verify deletion
        try:
            sdk.catalog_organization.get_llm_endpoint("endpoint1")
            assert False, "Endpoint should not exist"
        except NotFoundException:
            pass
    finally:
        # Ensure cleanup
        try:
            sdk.catalog_organization.delete_llm_endpoint("endpoint1")
        except NotFoundException:
            pass


#
# The following tests are commented out as they require the organization to have the FEDERATED_IDENTITY_MANAGEMENT
# entitlement enabled which cannot be done via SDK and must be done by GoodData support.
#
# @gd_vcr.use_cassette(str(_fixtures_dir / "create_identity_provider.yaml"))
# def test_create_identity_provider(test_config):
#     sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
#
#     identity_provider_id = "test_identity_provider"
#     custom_claim_mapping = {"email": "email"}
#     identifiers = ["goodtesting.com"]
#     oauth_client_id = "test_client_id"
#     oauth_client_secret = "test_client_secret"
#     oauth_issuer_location = "https://issuer.goodtesting.com"
#
#     new_identity_provider = CatalogIdentityProvider.init(
#         identity_provider_id=identity_provider_id,
#         custom_claim_mapping=custom_claim_mapping,
#         identifiers=identifiers,
#         oauth_client_id=oauth_client_id,
#         oauth_client_secret=oauth_client_secret,
#         oauth_issuer_location=oauth_issuer_location,
#     )
#
#     try:
#         sdk.catalog_organization.create_identity_provider(new_identity_provider)
#         identity_provider = sdk.catalog_organization.get_identity_provider(identity_provider_id)
#         assert identity_provider.id == identity_provider_id
#         assert identity_provider.attributes.custom_claim_mapping == custom_claim_mapping
#         assert identity_provider.attributes.identifiers == identifiers
#         assert identity_provider.attributes.oauth_client_id == oauth_client_id
#         assert identity_provider.attributes.oauth_client_secret is None  # oauth_client_secret is not returned
#         assert identity_provider.attributes.oauth_issuer_location == oauth_issuer_location
#     finally:
#         sdk.catalog_organization.delete_identity_provider(identity_provider_id)
#         assert len(sdk.catalog_organization.list_identity_providers()) == 0
#
#
# @gd_vcr.use_cassette(str(_fixtures_dir / "list_identity_providers.yaml"))
# def test_list_identity_providers(test_config):
#     sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
#
#     identity_provider_id = "test_identity_provider"
#     custom_claim_mapping = {"email": "email"}
#     identifiers = ["goodtesting.com"]
#     oauth_client_id = "test_client_id"
#     oauth_client_secret = "test_client_secret"
#     oauth_issuer_location = "https://issuer.goodtesting.com"
#
#     new_identity_provider_1 = CatalogIdentityProvider.init(
#         identity_provider_id=identity_provider_id + "_1",
#         custom_claim_mapping=custom_claim_mapping,
#         identifiers=identifiers,
#         oauth_client_id=oauth_client_id + "_1",
#         oauth_client_secret=oauth_client_secret + "_1",
#         oauth_issuer_location=oauth_issuer_location,
#     )
#     new_identity_provider_2 = CatalogIdentityProvider.init(
#         identity_provider_id=identity_provider_id + "_2",
#         custom_claim_mapping=custom_claim_mapping,
#         identifiers=identifiers,
#         oauth_client_id=oauth_client_id + "_2",
#         oauth_client_secret=oauth_client_secret + "_2",
#         oauth_issuer_location=oauth_issuer_location,
#     )
#
#     try:
#         sdk.catalog_organization.create_identity_provider(new_identity_provider_1)
#         sdk.catalog_organization.create_identity_provider(new_identity_provider_2)
#         identity_providers = sdk.catalog_organization.list_identity_providers()
#         # oauth_client_secret is not returned
#         new_identity_provider_1.attributes.oauth_client_secret = None
#         new_identity_provider_2.attributes.oauth_client_secret = None
#         assert len(identity_providers) == 2
#         assert new_identity_provider_1 in identity_providers
#         assert new_identity_provider_2 in identity_providers
#     finally:
#         sdk.catalog_organization.delete_identity_provider(new_identity_provider_1.id)
#         sdk.catalog_organization.delete_identity_provider(new_identity_provider_2.id)
#         assert len(sdk.catalog_organization.list_identity_providers()) == 0
#
#
# @gd_vcr.use_cassette(str(_fixtures_dir / "delete_identity_provider.yaml"))
# def test_delete_identity_provider(test_config):
#     sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
#
#     identity_provider_id = "test_identity_provider"
#     custom_claim_mapping = {"email": "email"}
#     identifiers = ["goodtesting.com"]
#     oauth_client_id = "test_client_id"
#     oauth_client_secret = "test_client_secret"
#     oauth_issuer_location = "https://issuer.goodtesting.com"
#
#     new_identity_provider = CatalogIdentityProvider.init(
#         identity_provider_id=identity_provider_id,
#         custom_claim_mapping=custom_claim_mapping,
#         identifiers=identifiers,
#         oauth_client_id=oauth_client_id,
#         oauth_client_secret=oauth_client_secret,
#         oauth_issuer_location=oauth_issuer_location,
#     )
#
#     try:
#         sdk.catalog_organization.create_identity_provider(new_identity_provider)
#         sdk.catalog_organization.delete_identity_provider(identity_provider_id)
#         sdk.catalog_organization.get_identity_provider(identity_provider_id)
#     except NotFoundException:
#         assert len(sdk.catalog_organization.list_identity_providers()) == 0
#     finally:
#         assert len(sdk.catalog_organization.list_identity_providers()) == 0
#
#
# @gd_vcr.use_cassette(str(_fixtures_dir / "update_identity_provider.yaml"))
# def test_update_identity_provider(test_config):
#     sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
#
#     identity_provider_id = "test_identity_provider"
#     custom_claim_mapping = {"email": "email"}
#     identifiers = ["goodtesting.com"]
#     oauth_client_id = "test_client_id"
#     oauth_client_secret = "test_client_secret"
#     oauth_issuer_location = "https://issuer.goodtesting.com"
#
#     new_identity_provider = CatalogIdentityProvider.init(
#         identity_provider_id=identity_provider_id,
#         custom_claim_mapping=custom_claim_mapping,
#         identifiers=identifiers,
#         oauth_client_id=oauth_client_id,
#         oauth_client_secret=oauth_client_secret,
#         oauth_issuer_location=oauth_issuer_location,
#     )
#     update_identity_provider = CatalogIdentityProvider.init(
#         identity_provider_id=identity_provider_id,
#         custom_claim_mapping=custom_claim_mapping,
#         identifiers=identifiers + ["anotheridentifier.com"],
#         oauth_client_id=oauth_client_id,
#         oauth_client_secret=oauth_client_secret,
#         oauth_issuer_location=oauth_issuer_location,
#     )
#
#     try:
#         sdk.catalog_organization.create_identity_provider(new_identity_provider)
#         sdk.catalog_organization.update_identity_provider(update_identity_provider)
#         identity_provider = sdk.catalog_organization.get_identity_provider(identity_provider_id)
#         assert identity_provider.id == identity_provider_id
#         assert identity_provider.attributes.custom_claim_mapping == custom_claim_mapping
#         assert identity_provider.attributes.identifiers == identifiers + ["anotheridentifier.com"]
#         assert identity_provider.attributes.oauth_client_id == oauth_client_id
#         assert identity_provider.attributes.oauth_client_secret is None  # oauth_client_secret is not returned
#         assert identity_provider.attributes.oauth_issuer_location == oauth_issuer_location
#     finally:
#         sdk.catalog_organization.delete_identity_provider(identity_provider_id)
#         assert len(sdk.catalog_organization.list_identity_providers()) == 0
#
#
# @gd_vcr.use_cassette(str(_fixtures_dir / "patch_identity_provider.yaml"))
# def test_patch_identity_provider(test_config):
#     sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
#
#     identity_provider_id = "test_identity_provider"
#     custom_claim_mapping = {"email": "email"}
#     identifiers = ["goodtesting.com"]
#     oauth_client_id = "test_client_id"
#     oauth_client_secret = "test_client_secret"
#     oauth_issuer_location = "https://issuer.goodtesting.com"
#
#     new_identity_provider = CatalogIdentityProvider.init(
#         identity_provider_id=identity_provider_id,
#         custom_claim_mapping=custom_claim_mapping,
#         identifiers=identifiers,
#         oauth_client_id=oauth_client_id,
#         oauth_client_secret=oauth_client_secret,
#         oauth_issuer_location=oauth_issuer_location,
#     )
#
#     try:
#         sdk.catalog_organization.create_identity_provider(new_identity_provider)
#         sdk.catalog_organization.patch_identity_provider_attributes(
#             identity_provider_id, {"identifiers": identifiers + ["anotheridentifier.com"]}
#         )
#         patched_identity_provider = sdk.catalog_organization.get_identity_provider(identity_provider_id)
#         assert patched_identity_provider.id == identity_provider_id
#         assert patched_identity_provider.attributes.custom_claim_mapping == custom_claim_mapping
#         assert patched_identity_provider.attributes.identifiers == identifiers + ["anotheridentifier.com"]
#         assert patched_identity_provider.attributes.oauth_client_id == oauth_client_id
#         assert patched_identity_provider.attributes.oauth_client_secret is None  # oauth_client_secret is not returned
#         assert patched_identity_provider.attributes.oauth_issuer_location == oauth_issuer_location
#     finally:
#         sdk.catalog_organization.delete_identity_provider(identity_provider_id)
#         assert len(sdk.catalog_organization.list_identity_providers()) == 0
#
#
# @gd_vcr.use_cassette(str(_fixtures_dir / "layout_identity_providers.yaml"))
# def test_layout_identity_providers(test_config):
#     sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
#
#     idps = sdk.catalog_organization.get_declarative_identity_providers()
#     assert len(idps) == 0
#
#     try:
#         identity_provider_id = "test_identity_provider"
#         custom_claim_mapping = {"email": "email"}
#         identifiers = ["goodtesting.com"]
#         oauth_client_id = "test_client_id"
#         oauth_client_secret = "test_client_secret"
#         oauth_issuer_location = "https://issuer.goodtesting.com"
#
#         identity_providers_e = [
#             CatalogDeclarativeIdentityProvider(
#                 id=identity_provider_id,
#                 custom_claim_mapping=custom_claim_mapping,
#                 identifiers=identifiers,
#                 oauth_client_id=oauth_client_id,
#                 oauth_client_secret=oauth_client_secret,
#                 oauth_issuer_location=oauth_issuer_location,
#             ),
#         ]
#         sdk.catalog_organization.put_declarative_identity_providers(identity_providers_e)
#         identity_providers_o = sdk.catalog_organization.get_declarative_identity_providers()
#         assert identity_providers_o[0].id == identity_providers_e[0].id
#         assert identity_providers_o[0].custom_claim_mapping == identity_providers_e[0].custom_claim_mapping
#         assert identity_providers_o[0].identifiers == identity_providers_e[0].identifiers
#         assert identity_providers_o[0].oauth_client_id == identity_providers_e[0].oauth_client_id
#         assert identity_providers_o[0].oauth_client_secret is None
#         assert identity_providers_o[0].oauth_issuer_location == identity_providers_e[0].oauth_issuer_location
#     finally:
#         sdk.catalog_organization.put_declarative_identity_providers([])
#         idps = sdk.catalog_organization.get_declarative_identity_providers()
#         assert len(idps) == 0
