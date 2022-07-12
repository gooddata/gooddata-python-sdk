:orphan:

Catalog Organization Service
****************************

The ``gooddata_sdk.catalog_organization`` service enables you to perform the following actions
on organization:

* Update OIDC parameters
* Update organization name

.. _o entity methods:

Entity methods
^^^^^^^^^^^^^^

The *gooddata_sdk.catalog_organization* supports the following entity API calls:

* ``update_oidc_parameters(oauth_issuer_location: Optional[str] = None, oauth_client_id: Optional[str] = None, oauth_client_secret: Optional[str] = None)``

    Update OIDC parameters of organization.

* ``update_name(name: str)``

    Update name of organization.

**Example Usage**

.. code-block:: python

    from gooddata_sdk import GoodDataSdk

    # GoodData.CN host in the form of uri eg. "http://localhost:3000"
    host = "http://localhost:3000"
    # GoodData.CN user token
    token = "some_user_token"
    sdk = GoodDataSdk.create(host, token)

    # Update organization name
    sdk.catalog_organization.update_name(name="new_organization_name")

    # Update OIDC provider
    sdk.catalog_organization.update_oidc_parameters(oauth_client_id="oauth_client_id",
                                                    oauth_issuer_location="oauth_issuer_location",
                                                    oauth_client_secret="oauth_client_secret")
