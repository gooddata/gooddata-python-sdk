# (C) 2024 GoodData Corporation
# env.py
import os

# Define environment variables
HOST = os.getenv("GOODDATA_HOST", "https://checklist.staging.stg11.panther.intgdc.com")
TOKEN = os.getenv("GOODDATA_TOKEN", "<your token>")
DATASOURCE_ID = os.getenv("DATASOURCE_ID", "your datasource")
WORKSPACE_ID = "your workspace"
