### FOSSA scan support
FOSSA scan is triggered manually currently. It will be part of PR check in the future.

#### How to trigger scan manually
Use job https://checklist.intgdc.com/job/space/job/fossa-repository-scanning-tool with the following parameters:
- REPOSITORIES: gooddata-python-sdk
- GITHUB_USER: gooddata
- BRANCH: latest
- DOCKER_IMAGE: harbor.intgdc.com/tools/gdc-fossa-cli:latest
- SCAN_CMD: analyze
