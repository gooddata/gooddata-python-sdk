# P005 - OpenAPI Datetime Format Schema Annotations

## Summary
This synchronization tracks the addition of explicit OpenAPI datetime format schema annotations for `createdAt` and `modifiedAt` timestamp fields across multiple metadata models in gdc-nas.

## GDC-NAS Changes
- **Problem ID**: P005
- **JIRA**: STL-2296
- **Commits**:
  - ff5a90d9c251292fda3ef6a2dff5161de6317fa2 (merge)
  - 66eb00ce47e05d514d292491c47e16d4297b9487 (implementation)

## Affected Entities
The following metadata models had `@field:Schema` annotations added to their `createdAt` and `modifiedAt` fields:

1. AnalyticalDashboard
2. AttributeHierarchy
3. Automation
4. DashboardPlugin
5. ExportDefinition
6. MemoryItem
7. Metric
8. VisualizationObject

## Schema Annotations Added
```kotlin
@field:Schema(
    description = "Time of the entity creation.",
    example = "[ \"2023-07-20 12:30\" ]",
    type = "string",
    pattern = "[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}",
    nullable = true
)
```

## SDK Impact
The Python SDK's gooddata-api-client has been regenerated from the updated OpenAPI spec. All affected entity model files now include:

- Proper datetime type annotations: `(datetime, none_type,)`
- Regex validation patterns: `r'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}'`

### Verified Files
- `gooddata-api-client/gooddata_api_client/model/json_api_metric_out_attributes.py`
- `gooddata-api-client/gooddata_api_client/model/json_api_analytical_dashboard_out_attributes.py`
- `gooddata-api-client/gooddata_api_client/model/json_api_visualization_object_out_attributes.py`
- `gooddata-api-client/gooddata_api_client/model/json_api_automation_out_attributes.py`
- `gooddata-api-client/gooddata_api_client/model/json_api_attribute_hierarchy_out_attributes.py`
- `gooddata-api-client/gooddata_api_client/model/json_api_dashboard_plugin_out_attributes.py`
- `gooddata-api-client/gooddata_api_client/model/json_api_export_definition_out_attributes.py`
- `gooddata-api-client/gooddata_api_client/model/json_api_memory_item_out_attributes.py`

## Verification Status
✅ All affected models have proper datetime format specifications
✅ Regex patterns match the backend schema annotations
✅ Type annotations correctly reflect nullable datetime fields
✅ No additional SDK code changes required

## Jira Ticket
**NOTE**: Jira sandbox was under maintenance during sync process. Ticket should be created manually:
- **Project**: DX (or appropriate project)
- **Type**: Task
- **Summary**: Sync SDK with datetime format schema annotations
- **Description**: See commit message for full details
- **Related Issues**: STL-2296

## Notes
The changes were automatically incorporated through OpenAPI client regeneration. The datetime format specifications ensure consistent parsing and serialization of timestamp fields between the backend API and Python SDK clients.
