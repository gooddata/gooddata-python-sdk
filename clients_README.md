# Generated API Clients

The generated client provides Python classes that you can use to call GoodData REST APIs. The client contains
models for API requests and responses and controllers to actually call the APIs.

We recommend using the gooddata_sdk package where possible because:
- the generated code can be at times fairly convoluted, harder to use or outright buggy. At times this leads to
  use of 'tricks' in order to succeed.
- even if generator project marked python language support as STABLE, we plan to:
  - use the latest generator version with possible API breaking changes
  - merge clients to one project

Information about OpenAPI generator, its configuration and customization, are available in
[OpenAPI Generator README](.openapi-generator/README.md).
