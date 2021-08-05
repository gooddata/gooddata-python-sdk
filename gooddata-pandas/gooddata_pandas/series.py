# (C) 2021 GoodData Corporation
from typing import Union

import pandas
from gooddata_pandas.data_access import compute_and_extract
from gooddata_pandas.utils import IndexDef, LabelItemDef
from gooddata_sdk import GoodDataSdk, Attribute, SimpleMeasure, Filter, ObjId


class GoodDataSeriesFactory:
    def __init__(self, sdk: GoodDataSdk, workspace_id: str):
        self._sdk = sdk
        self._workspace_id = workspace_id

    def indexed(self, index_by: IndexDef, data_by: Union[SimpleMeasure, str, ObjId, Attribute],
                filter_by: Union[Filter, list[Filter]] = None) -> pandas.Series:
        """
        Creates pandas Series from data points calculated from a single `data_by` that will be computed on granularity
        of the index  labels. The elements of the index labels will be used to construct simple or hierarchical index.

        :param index_by: label to index by; specify either:
         - string with id: 'some_label_id',
         - object identifier: ObjId(id='some_label_id', type='label'),
         - string representation of object identifier: 'label/some_label_id'
         - or an Attribute object used in the compute model: Attribute(local_id=..., label='some_label_id')
         - dict containing mapping of index name to label to use for indexing - specified in one of the ways list above
        :param data_by: label, fact or metric to that will provide data (measure values or label elements); specify either:
         - object identifier: ObjId(id='some_id', type='<type>') - where type is either 'label', 'fact' or 'metric'
         - string representation of object identifier: '<type>/some_id' - where type is either 'label', 'fact' or 'metric'
         - Attribute object used in the compute model: Attribute(local_id=..., label='some_label_id')
         - SimpleMeasure object used in the compute model: SimpleMeasure(local_id=..., item=..., aggregation=...)
        :param filter_by: optionally specify filter to apply during computation on the server
        :return:
        """
        data, index = compute_and_extract(self._sdk, self._workspace_id, index_by=index_by,
                                          columns={'_series': data_by}, filter_by=filter_by)

        _idx = None
        if len(index) == 1:
            _idx = pandas.Index(list(index.values())[0])
        elif len(index) > 1:
            _idx = pandas.MultiIndex.from_arrays(list(index.values()), names=list(index.keys()))

        return pandas.Series(data=data['_series'], index=_idx)

    def not_indexed(self, data_by: Union[SimpleMeasure, str, ObjId, Attribute],
                    granularity: Union[list[LabelItemDef], IndexDef] = None,
                    filter_by: Union[Filter, list[Filter]] = None) -> pandas.Series:
        """
        Creates pandas Series from data points calculated from a single `data_by` that will be computed on granularity
        of the specified labels. No index will be constructed.

        Note that data_by may also be a label in which case the Series will contain label elements.

        :param data_by: label, fact or metric to get data from; specify either:
         - object identifier: ObjId(id='some_id', type='<type>') - where type is either 'label', 'fact' or 'metric'
         - string representation of object identifier: '<type>/some_id' - where type is either 'label', 'fact' or 'metric'
         - Attribute object used in the compute model: Attribute(local_id=..., label='some_label_id')
         - SimpleMeasure object used in the compute model: SimpleMeasure(local_id=..., item=..., aggregation=...)
        :param granularity: optionally specify label to slice the metric by; specify either:
         - string with id: 'some_label_id',
         - object identifier: ObjId(id='some_label_id', type='label'),
         - string representation of object identifier: 'label/some_label_id'
         - or an Attribute object used in the compute model: Attribute(local_id=..., label='some_label_id')
         - list containing multiple labels to slice the metric by - specified in one of the ways list above
         - dict containing mapping of index name to label to use for indexing - specified in one of the ways list above;
            this option is available so that you can easily switch from indexed factory method to this one if needed
        :param filter_by: optionally specify filter to apply during computation on the server
        :return:
        """

        if isinstance(granularity, list):
            _index = dict([(idx, label) for idx, label in enumerate(granularity)])
        else:
            _index = granularity

        data, _ = compute_and_extract(self._sdk, self._workspace_id, index_by=granularity,
                                      columns={'_series': data_by}, filter_by=filter_by)

        return pandas.Series(data=data['_series'])
