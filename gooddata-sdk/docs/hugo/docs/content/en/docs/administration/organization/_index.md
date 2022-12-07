---
title: "Organization"
linkTitle: "Organization"
weight: 10
no_list: true
---

Manage an organization.

See [Manage Organizations](https://www.gooddata.com/developers/cloud-native/doc/cloud/manage-deployment/set-up-organizations/manage-organizations/) to learn how organizations work in GoodData.

## Methods

* [update_name](./update_name/)
* [update_oidc_parameters](./update_oidc_parameters/)

## Example

Update organization's name and OIDC provider:

```python
from gooddata_sdk import GoodDataSdk

# GoodData host in the form of uri
host = "http://localhost:3000"
# GoodData user token
token = "some_user_token"
sdk = GoodDataSdk.create(host, token)

# Update organization name
sdk.catalog_organization.update_name(name="new_organization_name")

# Update OIDC provider
sdk.catalog_organization.update_oidc_parameters(oauth_client_id="oauth_client_id",
                                                oauth_issuer_location="oauth_issuer_location",
                                                oauth_client_secret="oauth_client_secret")
```
