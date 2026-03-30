# (C) 2021 GoodData Corporation

from gooddata_pandas._arrow_types import TypesMapper
from gooddata_pandas._version import __version__

try:
    from gooddata_pandas.arrow_convertor import convert_arrow_table_to_dataframe
except ImportError:

    def convert_arrow_table_to_dataframe(*args, **kwargs):
        raise ImportError("pyarrow is required for Arrow support. Install it with: pip install gooddata-pandas[arrow]")


from gooddata_pandas.dataframe import DataFrameFactory
from gooddata_pandas.good_pandas import GoodPandas
from gooddata_pandas.result_convertor import LabelOverrides
from gooddata_pandas.series import SeriesFactory
