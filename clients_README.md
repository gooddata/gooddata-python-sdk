# Generated API Clients

The generated clients provide Python classes that you can use to call GoodData.CN REST APIs. The clients contain
models for API requests and responses and controllers to actually call the APIs.

However caveat emptor; the generated code can be at times fairly convoluted, harder to to use or outright buggy.
At times this leads to use of 'tricks' in order to succeed.

We recommend that where possible, you use the gooddata_sdk package for a more convenient experience.

### Known issues

The complexity of some of the GD.CN API schemas combined with the bugs in the generated code mean you may need to
disable return type checking and/or type checking when creating model objects.

Use the `_check_return_type=False` keyword parameter when calling generated API client methods to disable return
type checking. For example:

```python
import gooddata_metadata_client.apis as metadata_apis

api = metadata_apis.WorkspaceObjectControllerApi()
metrics = api.get_all_entities_metrics('workspace_id', size=500, _check_return_type=False)
```

Use the `_check_type=False` keyword parameter when creating objects from generated models. For example:

```python
import gooddata_afm_client.models as afm_models

afm_models.RelativeDateFilterBody(dataset=..., granularity=..., _from=..., to=..., _check_type=False)
```
