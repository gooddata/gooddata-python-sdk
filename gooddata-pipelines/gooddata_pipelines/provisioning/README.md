<!-- TODO: reused readme from client-specific implementation - revise this, keep relevant parts only! -->
<!-- TODO: possibly salvage this for productivity-tools repository readme -->

# Provisioning tool

Interface to read resources from a source database and replicate the setting in Panther.

## Database clients

The provisioning tool can connect to:

- ADS (`ADSClient`)

All workflows currently fetch data from ADS. Other data sources are not yet implemented.

Planned:

- read CSV files from S3
- PostgreSQL (`PostgresClient`)
- BigQuery (`BigQueryClient`)

## Dependencies

The script was written using Python version 3.12.4. Project dependencies can be installed by running

```bash
pip install -r requirements.txt
```

## Environment variables

Create a .env file containing variables outlined in .env.sample.

Note that the names of columns and tables need to adhere to the rules of the source database. For instance, in case of the ADS, the `WORKSPACE_PROVISIONING_LOG_TABLE_NAME` cannot contain dash `-` or other special characters.

## Usage

The entrypoint for running the scripts locally is the `workflow_provisioning.py` file. You can run this script with arguments defining which entities should be provisioned:

```bash
python workflow_provisioning.py workspaces
```

To see what options are available, run

```bash
python workflow_provisioning.py --help
```

The script supports multiple arguments as input. In that case, the entities are processed in a logical order, i.e. starting with workspace provisioning, user creation/deletion, then user groups and finally permission management.

```bash
python workflow_provisioning.py workspaces users user_permissions
```

### Workspace provisioning

The script can be run from `workflow_workspaces.py` in project root directory. Before running the script, you need to create a `.env` file in the root directory. The structure should reflect the `.env.sample` file.

The environment variables are separated in four sections: database credentials, Panther credentials, query parameters, and logging.

In case of URLs, such as the `PANTHER_DOMAIN` environment variable, please use the entire URL, including the `https://` in the beginning.

Afterwards, you can run the provisioning script simply by running the command below. It will use ADS as the source of primary data.

```bash
python workflow_provisioning.py workspaces
```

### User provisioning

The user provisioning consists of three workflows to manage users, user groups and to assign workspace level permissions to either a user or a group.

The environment variables that are needed for execution are outlined in `.env.sample` file located in `panther-integration` folder.

#### Users

To manage users under the specified organization, run:

```bash
python workflow_provisioning.py users
```

Following format of the input data is expected:

| user_id              | firstname | lastname | email                   | auth_id   | user_groups | is_active |
| -------------------- | --------- | -------- | ----------------------- | --------- | ----------- | --------- |
| jozef.mrkva          | jozef     | mrkva    | jozef.mrkva@test.com    | auth_id_1 |             | True      |
| bartolomej.brokolica |           |          |                         |           |             | False     |
| peter.pertzlen       | peter     | pertzlen | peter.pertzlen@test.com | auth_id_3 | ug_1, ug_2  | True      |
| zoltan.zeler         | zoltan    | zeler    | zoltan.zeler@test.com   | auth_id_4 | ug_1        | True      |
| kristian.kalerab     | kristian  | kalerab  |                         | auth_id_5 |             | True      |
| richard.cvikla       |           |          | richard.cvikla@test.com | auth_id_6 | ug_1, ug_2  | False     |
| adam.avokado         |           |          |                         | auth_id_7 |             | False     |

Here, each `user_id` is the ID of the user to manage.

The `firstname`, `lastname`, `email`, and `auth_id` fields are optional attributes of the user.

The `user_groups` field specifies user group memberships of the user.

Lastly, the `is_active` field contains information about whether the user should or should not exist in the organization. The `is_active` field is case-insensitive and considers `true` as the only value taken as positive. Any other value in this field is considered negative (e.g.: `blabla` would evaluate to `False`).

The workflow only modifies users mentioned in the input data.

#### User groups

To manage user groups under the specified organization, run:

```bash
python workflow_provisioning.py user_groups
```

Following format of the input data is expected:

| user_group_id | user_group_name | parent_user_groups | is_active |
| ------------- | --------------- | ------------------ | --------- |
| ug_1          | Admins          |                    | True      |
| ug_2          | Developers      | ug_1               | True      |
| ug_3          | Testers         | ug_1, ug_2         | True      |
| ug_4          | TemporaryAccess | ug_2               | False     |

Here, each `user_group_id` is the unique identifier for the user group.

The `user_group_name` field is an optional name for the user group, defaulting to the ID if not provided.

The `parent_user_groups` field specifies the parent user groups, defining hierarchical relationships.

The `is_active` field contains information about whether the user group should exist or be deleted from the organization. The `is_active` field is case-insensitive, recognizing `true` as the only affirmative value. Any other value is considered negative (e.g., `no` would evaluate to `False`).

#### Permissions

To grant permissions to either individual user or user groups, run:

```bash
python workflow_provisioning.py user_permissions
```

Following format of the input data is expected:

| user_id | ug_id | ws_id   | ws_permissions | is_active |
| ------- | ----- | ------- | -------------- | --------- |
| user_1  |       | ws_id_1 | ANALYZE        | True      |
| user_1  |       | ws_id_1 | VIEW           | False     |
| user_1  |       | ws_id_2 | MANAGE         | True      |
| user_2  |       | ws_id_1 | ANALYZE        | True      |
| user_2  |       | ws_id_2 | MANAGE         | True      |
|         | ug_1  | ws_id_1 | ANALYZE        | True      |
|         | ug_1  | ws_id_1 | VIEW           | True      |
|         | ug_1  | ws_id_1 | MANAGE         | False     |
|         | ug_2  | ws_id_1 | ANALYZE        | True      |
|         | ug_2  | ws_id_2 | MANAGE         | True      |

Here, each `user_id` is the ID of the user to manage, and `ug_id` is the ID of the user group to manage. Note that these fields are mutually exclusive and you should provide only one of the two values per each row.

The `ws_id` is the workspace ID that the permission is bound to.

Lastly, the `is_active` field contains information about whether the permission should or should not exist in the organization. The `is_active` field is case insensitive and considers `true` as the only value taken as positive. Any other value in this field is considered negative (e.g.: `blabla` would evaluate to `False`).

## Tests

The tests suite can be run with pytest:

```bash
poetry run pytest
```
