---
title: "add_metadata_locale"
linkTitle: "add_metadata_locale"
weight: 55
superheading: "catalog_workspace."
---

``add_metadata_locale(workspace_id: str, target_language: str, translator_func: Callable, set_locale: bool = True) -> None``

Add and optionally set the metadata localization for a workspace in a target language.

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
The ID of the workspace.
{{< /parameter >}}
{{< parameter p_name="target_language" p_type="string" >}}
The target language for the metadata localization.
{{< /parameter >}}
{{< parameter p_name="translator_func" p_type="Callable" >}}
A function to translate the source text.
{{< /parameter >}}
{{< parameter p_name="set_locale" p_type="bool" >}}
Flag to indicate if the locale settings should be updated in the workspace.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```python
# Add and set the metadata localization for a workspace using a translation function.
sdk.catalog_workspace.add_metadata_locale(
    workspace_id="123",
    target_language="de-DE",
    translator_func=my_translation_function,
    set_locale=True
)
