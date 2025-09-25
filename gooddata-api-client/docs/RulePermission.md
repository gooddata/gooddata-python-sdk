# RulePermission

List of rules

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**permissions** | [**List[GrantedPermission]**](GrantedPermission.md) | Permissions granted by the rule | [optional] 
**type** | **str** | Type of the rule | 

## Example

```python
from gooddata_api_client.models.rule_permission import RulePermission

# TODO update the JSON string below
json = "{}"
# create an instance of RulePermission from a JSON string
rule_permission_instance = RulePermission.from_json(json)
# print the JSON string representation of the object
print(RulePermission.to_json())

# convert the object into a dict
rule_permission_dict = rule_permission_instance.to_dict()
# create an instance of RulePermission from a dict
rule_permission_from_dict = RulePermission.from_dict(rule_permission_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


