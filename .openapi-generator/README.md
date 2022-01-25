### OpenAPI generator configuration and customizations
This directory contains configuration to generate OpenAPI clients together with
custom templates for part of generated code. Layout:
- configs - configuration files
- custom_templates - custom_templates directory used for all generated clients

Clients are created using [OpenAPI generator](https://github.com/OpenAPITools/openapi-generator). Python language
was marked as STABLE recently by [PR](https://github.com/OpenAPITools/openapi-generator/pull/11270).


#### How to generate or re-generate client
OpenAPI client generation is orchestrated by script `scripts/generate_client.sh`. Script either creates a new client
if no such exists or updates existing client code.

Use prepared `make` targets from repository root:
- `make afm-client`
- `make metadata-client`
- `make scan-client`

Predefined targets use `http://gooddata-cn-ce:3000` URL to fetch OpenAPI schema and connect generator container to
the `gooddata-python-sdk_default` network. It is prepared to be executed against running `docker-compose.yaml`
services.

When you need to point generator to different schema source, use `generate_client.sh` script directly.
Below is the example for `gooddata-scan-client` and schema on URL `https://my-gd-cn`, execute it from
the repository root:
```bash
./scripts/generate_client.sh gooddata-scan-client -u 'https://my-gd-cn'
```

When the schema source is available only in docker on the localhost use parameter `-n` to specify docker network
name:
```bash
./scripts/generate_client.sh gooddata-scan-client -u 'https://my-gd-cn' -n 'my-gd-cn-network-name'
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


### Known issues
Metadata OpenApi specification is missing response schema or the following resources:
- /api/config
- /api/options/availableDrivers

This inconsistency will be addressed by future GD.CN version.
It unfortunately causes `NullPointerException` in `openapitools/openapi-generator-cli:v5.3.1` and later.
Do the following to generate the file:
- store OpenApi schema to localhost to repository root
- add missing response schemata
- generate metadata client using
  ```bash
  ./scripts/generate_client.sh gooddata-metadata-client -f "/local/<name_of_openapi_json_file>.json"
  ```

#### Missing schemata
- /api/options
  ```json
  {
    "schema": {
      "type": "object",
      "description": "A hashmap of all available datasource drivers",
      "properties": {
        "options": {
          "type": "object",
          "properties": {
            "description": {
              "type": "string"
            },
            "links": {
              "type": "object",
              "properties": {
                "availableDrivers": {
                  "type": "string"
                }
              }
            }
          }
        }
      }
    }
  }
  ```
- /api/options/availableDrivers
  ```json
  {
    "schema": {
      "type": "object",
      "description": "A hashmap of all available datasource drivers",
      "additionalProperties": {
        "type": "string"
      }
    }
  }

  ```
