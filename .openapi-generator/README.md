### OpenAPI generator configuration and customizations
This directory contains configuration to generate OpenAPI clients together with
custom templates for part of generated code. Layout:
- configs - configuration files
- custom_templates - custom_templates directory used for all generated clients

Clients are created using [OpenAPI generator](https://github.com/OpenAPITools/openapi-generator). Python language
was marked as STABLE recently by [PR](https://github.com/OpenAPITools/openapi-generator/pull/11270).


#### How to generate or re-generate client
OpenAPI client generation is orchestrated by script `scripts/generate_client.sh`. Script either creates a new client
if no such exists or update existing client code.

Use prepared `make` targets from repository root:
- `make afm-client`
- `make metadata-client`
- `make scan-client`

Predefined targets use http://localhost:3000 URL to fetch OpenAPI schema.

When you need to point generator to different schema source, use `generate_client.sh` script directly.
Below is the example for `gooddata-scan-client` and schema on URL `https://my-gd-cn`, execute it from
the repository root:
```bash
./scripts/generate_client.sh gooddata-scan-client -u 'https://my-gd-cn'
```

#### How to generate default templates
It is possible to generate default openapi generator templates. Execute the following from the repository root
```bash
docker run --rm \
-v "$(pwd):/local" \
-u $(id -u ${USER}):$(id -g ${USER}) \
openapitools/openapi-generator-cli:v5.3.1 author template \
-g python --library urllib3 \
-o /local/.openapi-generator/templates
```
Templates can be used as the base for customizations. See
[templating](https://github.com/OpenAPITools/openapi-generator/blob/master/docs/templating.md) documentation for the details.

If new file needs to be added refer to [customization](https://github.com/OpenAPITools/openapi-generator/blob/master/docs/customization.md)
documentation.

#### Generator configuration
List of options available for python generator is [here](https://github.com/OpenAPITools/openapi-generator/blob/master/docs/generators/python.md).
There are also options common to all generators. Execute docker cli with `help` to list them.
```bash
docker run --rm \
-u $(id -u ${USER}):$(id -g ${USER}) \
openapitools/openapi-generator-cli help generate
```

Code used to generate python client code is [here](https://github.com/OpenAPITools/openapi-generator/blob/master/modules/openapi-generator/src/main/java/org/openapitools/codegen/languages/PythonClientCodegen.java)

#### How to upgrade generator version
- Find out the last used generator version and the last used OpenAPI version
- Dump default templates and compare them with custom templates
- Update custom templates based on a new updates from generated templates
- Generate new clients using new version of generator and the last used version of OpenAPI
