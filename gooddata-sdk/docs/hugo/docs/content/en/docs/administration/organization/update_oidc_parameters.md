---
title: "update_oidc_parameters"
linkTitle: "update_oidc_parameters"
weight: 20
no_list: true
superheading: "catalog_organization."
---

<!-- TODO -->

``update_oidc_parameters(oauth_issuer_location: Optional[str] = None, oauth_client_id: Optional[str] = None, oauth_client_secret: Optional[str] = None)``

Update OIDC parameters of organization.

## Example

```python
# Update OIDC provider
sdk.catalog_organization.update_oidc_parameters(oauth_client_id="oauth_client_id",
                                                oauth_issuer_location="oauth_issuer_location",
                                                oauth_client_secret="oauth_client_secret")
```
