# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from from gooddata_scan_client.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from gooddata_scan_client.model.column_warning import ColumnWarning
from gooddata_scan_client.model.data_source_parameter import DataSourceParameter
from gooddata_scan_client.model.data_source_schemata import DataSourceSchemata
from gooddata_scan_client.model.declarative_column import DeclarativeColumn
from gooddata_scan_client.model.declarative_table import DeclarativeTable
from gooddata_scan_client.model.declarative_tables import DeclarativeTables
from gooddata_scan_client.model.scan_request import ScanRequest
from gooddata_scan_client.model.scan_result_pdm import ScanResultPdm
from gooddata_scan_client.model.table_warning import TableWarning
from gooddata_scan_client.model.test_definition_request import TestDefinitionRequest
from gooddata_scan_client.model.test_query_duration import TestQueryDuration
from gooddata_scan_client.model.test_request import TestRequest
from gooddata_scan_client.model.test_response import TestResponse
