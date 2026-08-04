---
title: "create_or_update_jwk"
linkTitle: "create_or_update_jwk"
superheading: "catalog_organization."
weight: 100
api_ref: "CatalogOrganizationService.create_or_update_jwk"
---

``create_or_update_jwk( jwk: CatalogJwk ) -> UpsertOutcome``

Create a new jwk or overwrite an existing jwk with the same id.

## Parameters

| name |	type	| description |
| -- | -- | -- |
| jwk	| CatalogJwk	 | Catalog Jwk object to be created or updated. |

## Returns

| type | description |
| -- | -- |
| UpsertOutcome | CREATED if the jwk did not exist yet, UPDATED if it did. |
