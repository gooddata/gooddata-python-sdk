---
title: "Metadata Localization"
linkTitle: "Metadata Localization"
weight: 20
---

Manage metadata localization for workspaces.

## Methods

* [get_metadata_localization](./get_metadata_localization/)
* [set_metadata_localization](./set_metadata_localization/)
* [clean_metadata_localization](./clean_metadata_localization/)
* [add_metadata_locale](./add_metadata_locale/)
* [save_metadata_locale_to_disk](./save_metadata_locale_to_disk/)
* [set_metadata_locale_from_disk](./set_metadata_locale_from_disk/)

## Example

```python
from gooddata_sdk import GoodDataSdk
from pathlib import Path

# GoodData base URL, e.g. "https://www.example.com"
host = "https://www.example.com"
# GoodData user token
token = "some_user_token"
sdk = GoodDataSdk.create(host, token)

# Example usage for getting metadata localization
localization = sdk.catalog_workspace.get_metadata_localization(
    workspace_id="123",
    target_language="de-DE"
)

# Example usage for setting metadata localization
sdk.catalog_workspace.set_metadata_localization(
    workspace_id="123",
    encoded_xml=b"<xml>...</xml>"
)

# Example usage for cleaning metadata localization
sdk.catalog_workspace.clean_metadata_localization(
    workspace_id="123",
    target_language="de-DE"
)

# Example usage for adding metadata locale
sdk.catalog_workspace.add_metadata_locale(
    workspace_id="123",
    target_language="de-DE",
    translator_func=my_translation_function,
    set_locale=True
)

# Example usage for saving metadata locale to disk
sdk.catalog_workspace.save_metadata_locale_to_disk(
    workspace_id="123",
    target_language="de-DE",
    file_path=Path("/path/to/file.xliff")
)

# Example usage for setting metadata locale from disk
sdk.catalog_workspace.set_metadata_locale_from_disk(
    workspace_id="123",
    file_path=Path("/path/to/file.xliff")
)
