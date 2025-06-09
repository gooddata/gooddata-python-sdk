# TODO

A list of outstanding tasks, features, or technical debt to be addressed in this project.

## Pre-release

- [ ] License file

## Features

- [ ] Workspace backup
- [ ] Workspace restore
- [ ] Handle input from csv files [?]

## Refactoring / Debt

- [ ] Cleanup custom exception
- [ ] Use objects to make `workspace_data_parses.py` more transparent
- [ ] Use objects in API integration. Consider using existing Python SDK objects where possible, otherwise create pydantic models to use instead of `dict[str, Any]` stand-ins for json values
- [ ] Improve test coverage. Write missing unit tests for legacy code (e.g., user data filters)

## Documentation

- [ ] Improve package README
- [ ] Workspace provisioning
- [ ] User provisioning
- [ ] User group provisioning
- [ ] Permission provisioning
- [ ] User data filter provisioning
