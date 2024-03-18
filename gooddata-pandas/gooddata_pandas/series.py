# (C) 2021 GoodData Corporation
from __future__ import annotations

from typing import Optional, Union

import pandas
from gooddata_sdk import Attribute, Filter, GoodDataSdk, ObjId, SimpleMetric

from gooddata_pandas.data_access import compute_and_extract
from gooddata_pandas.utils import IndexDef, LabelItemDef, make_pandas_index


class SeriesFactory:
    """This class serves as a factory to create Series objects by providing the necessary parameters.

    Attributes:
      sdk (GoodDataSdk): An instance of the GoodData software development kit.
      workspace_id (str): The unique identifier of the workspace.

    """

    def __init__(self, sdk: GoodDataSdk, workspace_id: str) -> None:
        self._sdk = sdk
        self._workspace_id = workspace_id

    def indexed(
        self,
        index_by: IndexDef,
        data_by: Union[SimpleMetric, str, ObjId, Attribute],
        filter_by: Optional[Union[Filter, list[Filter]]] = None,
    ) -> pandas.Series:
        """Creates pandas Series from data points calculated from a single `data_by`.

        Creates pandas Series from data points calculated from a single `data_by`, that will be computed on granularity
        of the index labels. The elements of the index labels will be used to construct simple or hierarchical index.

        Args:
            index_by (IndexDef): label to index by; specify either:

            - string with id: ``some_label_id``,
            - object identifier: ``ObjId(id='some_label_id', type='label')``,
            - string representation of object identifier: ``label/some_label_id``
            - or an Attribute object used in the compute model: ``Attribute(local_id=..., label='some_label_id')``
            - dict containing mapping of index name to label to use for indexing (in one of the ways listed above)

            data_by (Union[SimpleMetric, str, ObjId, Attribute]): label, fact or metric to that will provide data
              (metric values or label elements); specify either:

            - object identifier: ``ObjId(id='some_id', type='<type>')`` - where type is either ``label``, ``fact``
              or ``metric``
            - string representation of object identifier: ``<type>/some_id`` - where type is either ``label``, ``fact``
              or ``metric``
            - Attribute object used in the compute model: ``Attribute(local_id=..., label='some_label_id')``
            - SimpleMetric object used in the compute model: ``SimpleMetric(local_id=..., item=..., aggregation=...)``

            filter_by (Optional[Union[Filter, list[Filter]]]): optionally specify filter to apply during computation on
            the server, reference to filtering column can be one of:

            - string reference to index key
            - object identifier in string form
            - object identifier: ``ObjId(id='some_label_id', type='<type>')``
            - Attribute or Metric depending on type of filter

        Returns:
            pandas.Series: pandas series instance
        """

        data, index = compute_and_extract(
            self._sdk,
            self._workspace_id,
            index_by=index_by,
            columns={"_series": data_by},
            filter_by=filter_by,
        )

        _idx = make_pandas_index(index)

        return pandas.Series(data=data["_series"], index=_idx)

    def not_indexed(
        self,
        data_by: Union[SimpleMetric, str, ObjId, Attribute],
        granularity: Optional[Union[list[LabelItemDef], IndexDef]] = None,
        filter_by: Optional[Union[Filter, list[Filter]]] = None,
    ) -> pandas.Series:
        """
        Creates a pandas.Series from data points calculated from a single `data_by` without constructing an index.

        Args:
            data_by (Union[SimpleMetric, str, ObjId, Attribute]): The label, fact, or metric to obtain data from.
                Specify either:
                    - ObjId: ObjId(id='some_id', type='<type>')
                    - string representation of an identifier: '<type>/some_id'
                    - Attribute: Attribute(local_id=..., label='some_label_id')
                    - SimpleMetric: SimpleMetric(local_id=..., item=..., aggregation=...)
            granularity (Optional[Union[list[LabelItemDef], IndexDef]], optional): The label to slice the metric by.
                Specify either:
                    - string with id: 'some_label_id'
                    - ObjId: ObjId(id='some_label_id', type='label')
                    - string representation of an identifier: 'label/some_label_id'
                    - Attribute: Attribute(local_id=..., label='some_label_id')
                    - list containing multiple labels to slice the metric by
                    - dict containing mapping of index name to label
                Defaults to None.
            filter_by (Optional[Union[Filter, list[Filter]]], optional): The filter(s) to apply. Reference to filtering
                column can be one of:
                    - object identifier in string form
                    - ObjId: ObjId(id='some_label_id', type='<type>')
                    - Attribute or Metric depending on the type of filter
                Defaults to None.

        Returns:
            pandas.Series: The resulting pandas Series instance.
        """

        if isinstance(granularity, list):
            _index: Optional[IndexDef] = {str(idx): label for idx, label in enumerate(granularity)}
        else:
            _index = granularity

        data, _ = compute_and_extract(
            self._sdk,
            self._workspace_id,
            index_by=_index,
            columns={"_series": data_by},
            filter_by=filter_by,
        )

        return pandas.Series(data=data["_series"])
