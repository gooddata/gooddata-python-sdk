# (C) 2022 GoodData Corporation
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, cast

import pandas
from attrs import define, field, frozen

from gooddata_sdk import BareExecutionResponse, ExecutionResult, ResultCacheMetadata, ResultSizeDimensions

_DEFAULT_PAGE_SIZE = 100
_DataHeaders = List[List[Any]]
_DataArray = List[Union[int, None]]
LabelOverrides = Dict[str, Dict[str, Dict[str, str]]]


@frozen
class _DataWithHeaders:
    data: List[_DataArray]
    """extracted data; either array of values for one-dimensional result or array of arrays of values"""

    data_headers: Tuple[_DataHeaders, Optional[_DataHeaders]]
    """per-dimension headers for the data"""

    grand_totals: Tuple[Optional[List[_DataArray]], Optional[List[_DataArray]]]
    """per-dimension grand total data"""

    grand_total_headers: Tuple[Optional[_DataHeaders], Optional[_DataHeaders]]
    """per-dimension grand total headers"""


@define
class _AccumulatedData:
    """
    Utility class to offload code from the function that extracts all data and headers for a
    particular paged result. The method drives the paging and calls out to this class to accumulate
    the essential data and headers from the page.
    """

    data: List[_DataArray] = field(init=False, factory=list)
    data_headers: List[Optional[_DataHeaders]] = field(init=False, factory=lambda: [None, None])
    grand_totals: List[Optional[List[_DataArray]]] = field(init=False, factory=lambda: [None, None])
    grand_totals_headers: List[Optional[_DataHeaders]] = field(init=False, factory=lambda: [None, None])

    def accumulate_data(self, from_result: ExecutionResult) -> None:
        """
        if one-dimensional result, the data is single array, so this adds the elements of that array into 'data'
        if two-dimensional, the data is array of arrays, so this adds as many arrays as there are table rows
        """
        self.data.extend(from_result.data)

    def extend_existing_row_data(self, from_result: ExecutionResult) -> None:
        offset = from_result.paging_offset[0]

        for i in range(len(from_result.data)):
            self.data[offset + i].extend(from_result.data[i])

    def accumulate_headers(self, from_result: ExecutionResult, from_dim: int) -> None:
        """
        Accumulates headers for particular dimension of a result into the provided `data_headers` array at the index
        matching the dimension index. This will mutate the `data_headers`
        """
        if self.data_headers[from_dim] is None:
            self.data_headers[from_dim] = from_result.get_all_headers(dim=from_dim)
        else:
            for idx, headers in enumerate(from_result.get_all_headers(dim=from_dim)):
                cast(_DataHeaders, self.data_headers[from_dim])[idx].extend(headers)

    def accumulate_grand_totals(
        self, from_result: ExecutionResult, paging_dim: int, response: BareExecutionResponse
    ) -> None:
        """
        accumulates grand totals from the results; processes all grand totals on all dimensions; the method
        needs to know in which direction is the paging happening so that it can append new grand total data.
        """
        grand_totals = from_result.grand_totals
        if not len(grand_totals):
            return

        # get dimension indexes mapping from response like {"dim1": 0, "dim0": 1}
        dim_idx_dict = {dim["localIdentifier"]: idx for idx, dim in enumerate(response.dimensions)}

        for grand_total in grand_totals:
            # 2-dim results have always 1-dim grand totals (3-dim results have 2-dim gt but DataFrame stores 2D only)
            dims = grand_total["totalDimensions"]
            assert len(dims) == 1, "Only 2-dimensional results are supported"
            dim_idx = dim_idx_dict[dims[0]]
            # the dimension id specified on the grand total says from what dimension were
            # the grand totals calculated (1 for column totals or 0 for row totals);
            #
            # the grand totals themselves should, however be placed in the opposite dimension:
            #
            # column totals are extra rows at the end of the data
            # row totals are extra columns at the right 'edge' of the data
            opposite_dim = 1 if dim_idx == 0 else 0

            if self.grand_totals[opposite_dim] is None:
                # grand totals not initialized yet; initialize both data and headers by making
                # a shallow copy from the results
                self.grand_totals[opposite_dim] = grand_total["data"][:]
                # TODO: row total measure headers are currently not supported (only aggregation info w/o measure label)
                #       measure header defs are under ["headerGroups"][>0]
                self.grand_totals_headers[opposite_dim] = grand_total["dimensionHeaders"][0]["headerGroups"][0][
                    "headers"
                ][:]
            elif paging_dim != opposite_dim:
                # grand totals are already initialized and the code is paging in the direction that reveals
                # additional grand total values; append them accordingly; no need to consider total headers:
                # that is because only the grand total data is subject to paging
                grand_totals_item = cast(List[_DataArray], self.grand_totals[opposite_dim])
                if opposite_dim == 0:
                    # have column totals and paging 'to the right'; totals for the new columns are revealed so
                    # extend existing data arrays
                    for total_idx, total_data in enumerate(grand_total["data"]):
                        grand_totals_item[total_idx].extend(total_data)
                else:
                    # have row totals and paging down, keep adding extra rows
                    grand_totals_item.extend(grand_total["data"])

    def result(self) -> _DataWithHeaders:
        return _DataWithHeaders(
            data=self.data,
            data_headers=(cast(_DataHeaders, self.data_headers[0]), self.data_headers[1]),
            grand_totals=(self.grand_totals[0], self.grand_totals[1]),
            grand_total_headers=(self.grand_totals_headers[0], self.grand_totals_headers[1]),
        )


@define
class DataFrameMetadata:
    # row line location where total header is located per index header column
    # example:
    # Category  | Country | Budget
    # Car       | Arizona |    100
    #           | Texas   |     50
    #           | SUM     |    150
    # Train     | Arizona |    200    =>    [[7],[3,6]]
    #           | Texas   |    100
    #           | AVG     |    150
    # SUM       |         |    450
    row_totals_indexes: List[List[int]]

    execution_response: BareExecutionResponse

    @classmethod
    def from_data(
        cls,
        headers: Tuple[_DataHeaders, Optional[_DataHeaders]],
        execution_response: BareExecutionResponse,
    ) -> "DataFrameMetadata":
        row_totals_indexes = [
            [idx for idx, hdr in enumerate(dim) if hdr is not None and "totalHeader" in hdr] for dim in headers[0]
        ]
        return cls(
            row_totals_indexes=row_totals_indexes,
            execution_response=execution_response,
        )


def _read_complete_execution_result(
    execution_response: BareExecutionResponse,
    result_cache_metadata: ResultCacheMetadata,
    result_size_dimensions_limits: ResultSizeDimensions,
    result_size_bytes_limit: Optional[int] = None,
    page_size: int = _DEFAULT_PAGE_SIZE,
) -> _DataWithHeaders:
    """
    Extracts all data and headers for an execution result. This does page around the execution result to extract
    everything from the paged API.

    :param execution_response: execution response to work with;
    :return:
    """
    num_dims = len(execution_response.dimensions)
    offset = [0] * num_dims
    limit = [page_size] * num_dims
    acc = _AccumulatedData()

    result_size_limits_checked = False

    while True:
        # top-level loop pages through the first dimension;
        #
        # if one-dimensional result, it pages over an array of data
        # if two-dimensional result, it pages over table rows
        result = execution_response.read_result(offset=offset, limit=limit)

        if not result_size_limits_checked:
            result.check_dimensions_size_limits(result_size_dimensions_limits)
            result_cache_metadata.check_bytes_size_limit(result_size_bytes_limit)
            result_size_limits_checked = True

        acc.accumulate_data(from_result=result)
        acc.accumulate_headers(from_result=result, from_dim=0)
        acc.accumulate_grand_totals(from_result=result, paging_dim=0, response=execution_response)

        if num_dims > 1:
            # when result is two-dimensional make sure to read the column headers and column totals
            # just once - when scrolling 'to the right' for the first time;
            load_headers_and_totals = False
            if acc.data_headers[1] is None:
                acc.accumulate_headers(from_result=result, from_dim=1)
                load_headers_and_totals = True

            if not result.is_complete(dim=1):
                # have two-dimensional result (typical table) and the page does not contain
                # all the columns.
                #
                # page 'to the right' to get data from all columns, extend existing rows with that data
                offset = [offset[0], result.next_page_start(dim=1)]
                while True:
                    result = execution_response.read_result(offset=offset, limit=limit)
                    acc.extend_existing_row_data(from_result=result)

                    if load_headers_and_totals:
                        acc.accumulate_headers(from_result=result, from_dim=1)
                        acc.accumulate_grand_totals(from_result=result, paging_dim=1, response=execution_response)

                    if result.is_complete(dim=1):
                        break

                    offset = [offset[0], result.next_page_start(dim=1)]

        if result.is_complete(dim=0):
            break

        offset = [result.next_page_start(dim=0), 0] if num_dims > 1 else [result.next_page_start(dim=0)]

    return acc.result()


def _create_header_mapper(
    response: BareExecutionResponse,
    dim: int,
    label_overrides: Optional[LabelOverrides] = None,
    use_local_ids_in_headers: bool = False,
) -> Callable[[Any, Optional[int]], Optional[str]]:
    """
    Prepares header mapper function which is doing header structures translations into appropriate label used
    in a dataframe
    :param response: Response structure to gather dimension header details
    :param dim: dimension id
    :param label_overrides: label overrides
    :param use_local_ids_in_headers: Use local identifiers of header attributes and metrics. Optional.

    :return: Mapper function
    """
    if label_overrides is None:
        label_overrides = {}

    dim_descriptor = response.dimensions[dim]
    attribute_labels = label_overrides.get("labels", {})
    measure_labels = label_overrides.get("metrics", {})

    def _mapper(header: Any, header_idx: Optional[int]) -> Optional[str]:
        label = None
        if header is None:
            pass
        elif "attributeHeader" in header:
            if "labelValue" in header["attributeHeader"]:
                label = header["attributeHeader"]["labelValue"]
                # explicitly handle '(empty value)' if it's None otherwise it's not recognizable in final MultiIndex
                # backend represents ^^^ by "" (datasource value is "") or None (datasource value is NULL) therefore
                # if both representation are used it's necessary to set label to unique header label (space) to avoid
                # Excel formatter apply call failure
                if label is None:
                    label = " "
            elif "labelName" in header["attributeHeader"]:
                attr_local_id = header["attributeHeader"]["localIdentifier"]
                if use_local_ids_in_headers:
                    label = attr_local_id
                else:
                    if attr_local_id in attribute_labels:
                        label = attribute_labels[attr_local_id]["title"]
                    else:
                        label = header["attributeHeader"]["labelName"]
        elif "measureHeader" in header and header_idx is not None:
            measure_idx = header["measureHeader"]["measureIndex"]
            measure_descriptor = dim_descriptor["headers"][header_idx]["measureGroupHeaders"][measure_idx]

            if use_local_ids_in_headers:
                label = measure_descriptor["localIdentifier"]
            else:
                if measure_descriptor["localIdentifier"] in measure_labels:
                    label = measure_labels[measure_descriptor["localIdentifier"]]["title"]
                elif "name" in measure_descriptor:
                    label = measure_descriptor["name"]
                else:
                    label = measure_descriptor["localIdentifier"]
        elif "totalHeader" in header:
            label = header["totalHeader"]["function"]
        return label

    return _mapper


def _headers_to_index(
    dim_idx: int,
    headers: Tuple[_DataHeaders, Optional[_DataHeaders]],
    response: BareExecutionResponse,
    label_overrides: LabelOverrides,
    use_local_ids_in_headers: bool = False,
) -> Optional[pandas.Index]:
    if len(response.dimensions) <= dim_idx or not len(response.dimensions[dim_idx]["headers"]):
        return None

    mapper = _create_header_mapper(
        response=response,
        dim=dim_idx,
        label_overrides=label_overrides,
        use_local_ids_in_headers=use_local_ids_in_headers,
    )

    return pandas.MultiIndex.from_arrays(
        [
            tuple(mapper(header, header_idx) for header in header_group)
            for header_idx, header_group in enumerate(cast(_DataHeaders, headers[dim_idx]))
        ],
        names=[mapper(dim_header, None) for dim_header in (response.dimensions[dim_idx]["headers"])],
    )


def _merge_grand_totals_into_data(extract: _DataWithHeaders) -> Union[_DataArray, List[_DataArray]]:
    """
    Merges grand totals into the extracted data. this function will mutate the extracted data, extending
    the rows and columns with grand totals. Going with mutation here so as not to copy arrays around
    """
    data: List[_DataArray] = extract.data

    if extract.grand_totals[0] is not None:
        # column totals are computed into extra rows, one row per column total
        # add those rows at the end of the data rows
        data.extend(extract.grand_totals[0])

    if extract.grand_totals[1] is not None:
        # row totals are computed into extra columns that should be appended to
        # existing data rows
        for row_idx, cols_to_append in enumerate(extract.grand_totals[1]):
            data[row_idx].extend(cols_to_append)

    return data


def _merge_grand_total_headers_into_headers(extract: _DataWithHeaders) -> Tuple[_DataHeaders, Optional[_DataHeaders]]:
    """
    Merges grand total headers into data headers. This function will mutate the extracted data.
    """
    headers: Tuple[_DataHeaders, Optional[_DataHeaders]] = extract.data_headers

    for dim_idx, grand_total_headers in enumerate(extract.grand_total_headers):
        if grand_total_headers is None:
            continue
        header = cast(List[List[Any]], headers[dim_idx])
        header[0].extend(grand_total_headers)
        padding = [None] * len(grand_total_headers)
        for other_headers in header[1:]:
            other_headers.extend(padding)

    return headers


def convert_execution_response_to_dataframe(
    execution_response: BareExecutionResponse,
    result_cache_metadata: ResultCacheMetadata,
    label_overrides: LabelOverrides,
    result_size_dimensions_limits: ResultSizeDimensions,
    result_size_bytes_limit: Optional[int] = None,
    use_local_ids_in_headers: bool = False,
    page_size: int = _DEFAULT_PAGE_SIZE,
) -> Tuple[pandas.DataFrame, DataFrameMetadata]:
    """
    Converts execution result to a pandas dataframe, maintaining the dimensionality of the result.

    Because the result itself does not contain all the necessary metadata to do the full conversion, this method
    expects that the execution _response_.

    :param label_overrides: label overrides
    :param execution_response: execution response through which the result can be read and converted to a dataframe
    :return: a new dataframe
    """
    extract = _read_complete_execution_result(
        execution_response=execution_response,
        result_cache_metadata=result_cache_metadata,
        result_size_dimensions_limits=result_size_dimensions_limits,
        result_size_bytes_limit=result_size_bytes_limit,
        page_size=page_size,
    )
    full_data = _merge_grand_totals_into_data(extract)
    full_headers = _merge_grand_total_headers_into_headers(extract)

    df = pandas.DataFrame(
        data=full_data,
        index=_headers_to_index(
            dim_idx=0,
            headers=full_headers,
            response=execution_response,
            label_overrides=label_overrides,
            use_local_ids_in_headers=use_local_ids_in_headers,
        ),
        columns=_headers_to_index(
            dim_idx=1,
            headers=full_headers,
            response=execution_response,
            label_overrides=label_overrides,
            use_local_ids_in_headers=use_local_ids_in_headers,
        ),
    )

    return df, DataFrameMetadata.from_data(headers=full_headers, execution_response=execution_response)
