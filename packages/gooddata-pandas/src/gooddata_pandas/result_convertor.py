# (C) 2022 GoodData Corporation
from typing import Any, Callable, Optional, Union, cast

import pandas
from attrs import define, field, frozen
from gooddata_sdk import BareExecutionResponse, ExecutionResult, ResultCacheMetadata, ResultSizeDimensions

_DEFAULT_PAGE_SIZE = 100
_DataHeaders = list[list[Any]]
_DataArray = list[Union[int, None]]
LabelOverrides = dict[str, dict[str, dict[str, str]]]


@frozen
class _DataWithHeaders:
    """Extracted data; either array of values for one-dimensional result or array of arrays of values.

    Attributes:
        data (List[_DataArray]):
            Extracted data; either array of values for one-dimensional result or array of arrays of values.
        data_headers (Tuple[_DataHeaders, Optional[_DataHeaders]]):
            Per-dimension headers for the data.
        grand_totals (Tuple[Optional[List[_DataArray]], Optional[List[_DataArray]]]):
            Per-dimension grand total data.
        grand_total_headers (Tuple[Optional[_DataHeaders], Optional[_DataHeaders]]):
            Per-dimension grand total headers.
    """

    data: list[_DataArray]
    data_headers: tuple[_DataHeaders, Optional[_DataHeaders]]
    grand_totals: tuple[Optional[list[_DataArray]], Optional[list[_DataArray]]]
    grand_total_headers: tuple[Optional[list[dict[str, _DataHeaders]]], Optional[list[dict[str, _DataHeaders]]]]


@define
class _AccumulatedData:
    """
    Utility class to offload code from the function that extracts all data and headers for a
    particular paged result. The method drives the paging and calls out to this class to accumulate
    the essential data and headers from the page.

    Attributes:
        data (List[_DataArray]): Holds the accumulated data arrays from the pages.
        data_headers (List[Optional[_DataHeaders]]): Holds the headers for data arrays.
        grand_totals (List[Optional[List[_DataArray]]]): Holds the grand total data arrays.
        grand_totals_headers (List[Optional[_DataHeaders]]): Holds the headers for grand total data arrays.
    """

    data: list[_DataArray] = field(init=False, factory=list)
    data_headers: list[Optional[_DataHeaders]] = field(init=False, factory=lambda: [None, None])
    grand_totals: list[Optional[list[_DataArray]]] = field(init=False, factory=lambda: [None, None])
    grand_totals_headers: list[Optional[list[dict[str, _DataHeaders]]]] = field(
        init=False, factory=lambda: [None, None]
    )
    total_of_grant_totals_processed: bool = field(init=False, default=False)

    def accumulate_data(self, from_result: ExecutionResult) -> None:
        """
        Accumulate data from the ExecutionResult.

        If the result is one-dimensional, the data is a single array, so this adds the elements of that array
        into 'data'. If it's two-dimensional, the data is an array of arrays, so this adds as many arrays as
        there are table rows.

        Args:
            from_result (ExecutionResult): The result whose data will be extended into the current instance's data.
        """
        self.data.extend(from_result.data)

    def extend_existing_row_data(self, from_result: ExecutionResult) -> None:
        """
        Extend the existing row data with the data from the ExecutionResult.

        Args:
            from_result (ExecutionResult): The result whose data will be extended into the current instance's data.
        """
        offset = from_result.paging_offset[0]

        for i in range(len(from_result.data)):
            self.data[offset + i].extend(from_result.data[i])

    def accumulate_headers(self, from_result: ExecutionResult, from_dim: int) -> None:
        """
        Accumulate headers for a particular dimension of a result into the provided `data_headers` array at the index
        matching the dimension index.

        This will mutate the `data_headers`.

        Args:
            from_result (ExecutionResult): The result whose headers will be accumulated.
            from_dim (int): The dimension index.
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
        Accumulate grand totals from the results.

        Processes all grand totals on all dimensions and needs to know in which direction the paging is happening
        in order to append new grand total data.

        Args:
            from_result (ExecutionResult): The result whose grand totals will be accumulated.
            paging_dim (int): The paging dimension.
            response (BareExecutionResponse): The BareExecutionResponse instance.
        """
        grand_totals = from_result.grand_totals
        if not len(grand_totals):
            return

        # get dimension indexes mapping from response like {"dim1": 0, "dim0": 1}
        dim_idx_dict = {dim["localIdentifier"]: idx for idx, dim in enumerate(response.dimensions)}

        for grand_total in grand_totals:
            # 2-dim results have always 1-dim grand totals (3-dim results have 2-dim gt but DataFrame stores 2D only)
            dims = grand_total["totalDimensions"]

            # if dims are empty then data contain total of column and row grandtotals so extend existing data array
            if len(dims) == 0:
                if not self.total_of_grant_totals_processed:
                    grand_totals_item = cast(list[_DataArray], self.grand_totals[0])
                    for total_idx, total_data in enumerate(grand_total["data"]):
                        grand_totals_item[total_idx].extend(total_data)
                    self.total_of_grant_totals_processed = True
                continue

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
                self.grand_totals_headers[opposite_dim] = grand_total["dimensionHeaders"][0]["headerGroups"]
            elif paging_dim != opposite_dim:
                # grand totals are already initialized and the code is paging in the direction that reveals
                # additional grand total values; append them accordingly; no need to consider total headers:
                # that is because only the grand total data is subject to paging
                grand_totals_item = cast(list[_DataArray], self.grand_totals[opposite_dim])
                if opposite_dim == 0:
                    # have column totals and paging 'to the right'; totals for the new columns are revealed so
                    # extend existing data arrays
                    for total_idx, total_data in enumerate(grand_total["data"]):
                        grand_totals_item[total_idx].extend(total_data)
                else:
                    # have row totals and paging down, keep adding extra rows
                    grand_totals_item.extend(grand_total["data"])

    def result(self) -> _DataWithHeaders:
        """
        Returns the data with headers.

        Returns:
            _DataWithHeaders: The data, data headers, grand totals and grand total headers.
        """
        return _DataWithHeaders(
            data=self.data,
            data_headers=(cast(_DataHeaders, self.data_headers[0]), self.data_headers[1]),
            grand_totals=(self.grand_totals[0], self.grand_totals[1]),
            grand_total_headers=(self.grand_totals_headers[0], self.grand_totals_headers[1]),
        )


@define
class DataFrameMetadata:
    """
    DataFrameMetadata class stores metadata about a DataFrame.

    Attributes:
      row_totals_indexes: A nested list of integers. Each inner list represents
                          the row indices containing totals per index header column.
                          Example:
                          Category  | Country | Budget
                          Car       | Arizona |    100
                                    | Texas   |     50
                                    | SUM     |    150
                          Train     | Arizona |    200    =>    [[7],[3,6]]
                                    | Texas   |    100
                                    | AVG     |    150
                          SUM       |         |    450

      execution_response: An instance of BareExecutionResponse representing the
                          execution response.
    """

    row_totals_indexes: list[list[int]]
    execution_response: BareExecutionResponse
    primary_labels_from_index: dict[int, dict[str, str]]
    primary_labels_from_columns: dict[int, dict[str, str]]

    @classmethod
    def from_data(
        cls,
        headers: tuple[_DataHeaders, Optional[_DataHeaders]],
        execution_response: BareExecutionResponse,
        primary_labels_from_index: dict[int, dict[str, str]],
        primary_labels_from_columns: dict[int, dict[str, str]],
    ) -> "DataFrameMetadata":
        """This method constructs a DataFrameMetadata object from data headers and an execution response.

        Args: headers (Tuple[_DataHeaders, Optional[_DataHeaders]]):
            A tuple containing data headers. execution_response (BareExecutionResponse): An ExecutionResponse object.

        Returns: DataFrameMetadata: An initialized DataFrameMetadata object."""
        row_totals_indexes = [
            [idx for idx, hdr in enumerate(dim) if hdr is not None and "totalHeader" in hdr] for dim in headers[0]
        ]
        return cls(
            row_totals_indexes=row_totals_indexes,
            execution_response=execution_response,
            primary_labels_from_index=primary_labels_from_index,
            primary_labels_from_columns=primary_labels_from_columns,
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

    Args:
        execution_response (BareExecutionResponse): Execution response to work with.
        result_cache_metadata (ResultCacheMetadata): Metadata for the result cache.
        result_size_dimensions_limits (ResultSizeDimensions): Limits for result size dimensions.
        result_size_bytes_limit (Optional[int], optional): Limit for result size in bytes. Defaults to None.
        page_size (int, optional): Page size to use when reading data. Defaults to _DEFAULT_PAGE_SIZE.

    Returns:
        _DataWithHeaders: All the data and headers from the execution result.
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
    primary_attribute_labels_mapping: dict[int, dict[str, str]],
    label_overrides: Optional[LabelOverrides] = None,
    use_local_ids_in_headers: bool = False,
    use_primary_labels_in_attributes: bool = False,
) -> Callable[[Any, Optional[int]], Optional[str]]:
    """
    Prepares a header mapper function which translates header structures into appropriate labels used
    in a dataframe.

    Args:
        response (BareExecutionResponse): Response structure to gather dimension header details.
        dim (int): Dimension id.
        primary_attribute_labels_mapping (Dict[int, Dict[str, str]]): Dict to be filled by mapping of primary labels to
            custom labels per level identified by integer.
        label_overrides (Optional[LabelOverrides]): Label overrides. Defaults to None.
        use_local_ids_in_headers (bool): Use local identifiers of header attributes and metrics. Optional.
            Defaults to False.
        use_primary_labels_in_attributes (bool): Use primary labels in attributes. Optional. Defaults to False.

    Returns:
        Callable[[Any, Optional[int]], Optional[str]]: Mapper function.
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
                label_value = header["attributeHeader"]["labelValue"]
                primary_label_value = header["attributeHeader"]["primaryLabelValue"]
                label = primary_label_value if use_primary_labels_in_attributes else label_value
                if header_idx is not None:
                    if header_idx in primary_attribute_labels_mapping:
                        primary_attribute_labels_mapping[header_idx][primary_label_value] = label_value
                    else:
                        primary_attribute_labels_mapping[header_idx] = {primary_label_value: label_value}
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
    headers: tuple[_DataHeaders, Optional[_DataHeaders]],
    response: BareExecutionResponse,
    label_overrides: LabelOverrides,
    use_local_ids_in_headers: bool = False,
    use_primary_labels_in_attributes: bool = False,
) -> tuple[Optional[pandas.Index], dict[int, dict[str, str]]]:
    """Converts headers to a pandas MultiIndex.

    This function converts the headers present in the response to a pandas MultiIndex (can be used in pandas dataframes)

    Args:
        dim_idx (int): Index of the current dimension.
        headers (Tuple[_DataHeaders, Optional[_DataHeaders]]):
            Tuple of data headers and optional secondary data headers.
        response (BareExecutionResponse): The execution response object with all data.
        label_overrides (LabelOverrides): A dictionary containing label overrides for the headers.
        use_local_ids_in_headers (bool, optional): If True, uses local Ids in headers, otherwise not. Defaults to False.
        use_primary_labels_in_attributes (bool, optional): If True, uses primary labels in attributes, otherwise not.
            Defaults to False.

    Returns:
        Tuple[Optional[pandas.Index], Dict[int, Dict[str, str]]: A pandas MultiIndex object created from the headers
        with primary attribute labels mapping as Dict, or None with empty Dict if the headers are empty.
    """
    # dict of primary labels and it's custom labels for attributes per level as key
    primary_attribute_labels_mapping: dict[int, dict[str, str]] = {}

    if len(response.dimensions) <= dim_idx or not len(response.dimensions[dim_idx]["headers"]):
        return None, primary_attribute_labels_mapping

    mapper = _create_header_mapper(
        response=response,
        dim=dim_idx,
        label_overrides=label_overrides,
        use_local_ids_in_headers=use_local_ids_in_headers,
        use_primary_labels_in_attributes=use_primary_labels_in_attributes,
        primary_attribute_labels_mapping=primary_attribute_labels_mapping,
    )

    return pandas.MultiIndex.from_arrays(
        [
            tuple(mapper(header, header_idx) for header in header_group)
            for header_idx, header_group in enumerate(cast(_DataHeaders, headers[dim_idx]))
        ],
        names=[mapper(dim_header, None) for dim_header in (response.dimensions[dim_idx]["headers"])],
    ), primary_attribute_labels_mapping


def _merge_grand_totals_into_data(extract: _DataWithHeaders) -> Union[_DataArray, list[_DataArray]]:
    """
    Merges grand totals into the extracted data. This function will mutate the extracted data,
    extending the rows and columns with grand totals. Going with mutation here so as not to copy arrays around.

    Args:
        extract (_DataWithHeaders): Extracted data with headers and grand totals.

    Returns:
        Union[_DataArray, List[_DataArray]]: Mutated data with rows and columns extended with grand totals.
    """
    data: list[_DataArray] = extract.data

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


def _merge_grand_total_headers_into_headers(extract: _DataWithHeaders) -> tuple[_DataHeaders, Optional[_DataHeaders]]:
    """Merges grand total headers into data headers. This function will mutate the extracted data.

    Args:
        extract (_DataWithHeaders): The data along with its headers that need to be merged.

    Returns:
        Tuple[_DataHeaders, Optional[_DataHeaders]]:
            A tuple containing the modified data headers and the grand total headers if present.
    """
    headers: tuple[_DataHeaders, Optional[_DataHeaders]] = extract.data_headers

    for dim_idx, grand_total_headers in enumerate(extract.grand_total_headers):
        if grand_total_headers is None:
            continue
        header = cast(list[list[Any]], headers[dim_idx])
        for level, grand_total_header in enumerate(grand_total_headers):
            header[level].extend(grand_total_header["headers"])

    return headers


def convert_execution_response_to_dataframe(
    execution_response: BareExecutionResponse,
    result_cache_metadata: ResultCacheMetadata,
    label_overrides: LabelOverrides,
    result_size_dimensions_limits: ResultSizeDimensions,
    result_size_bytes_limit: Optional[int] = None,
    use_local_ids_in_headers: bool = False,
    use_primary_labels_in_attributes: bool = False,
    page_size: int = _DEFAULT_PAGE_SIZE,
) -> tuple[pandas.DataFrame, DataFrameMetadata]:
    """
    Converts execution result to a pandas dataframe, maintaining the dimensionality of the result.

    Args:
        execution_response (BareExecutionResponse): Execution response through which the result can be read
            and converted to a dataframe.
        result_cache_metadata (ResultCacheMetadata): Metadata about the result cache.
        label_overrides (LabelOverrides): Label overrides for the dataframe.
        result_size_dimensions_limits (ResultSizeDimensions): Dimension limits for the dataframe.
        result_size_bytes_limit (Optional[int], default=None): Size limit in bytes for the dataframe.
        use_local_ids_in_headers (bool, default=False): Use local ids in headers if True, else use default settings.
        use_primary_labels_in_attributes (bool, default=False): Use primary labels in attributes if True, else use
            default settings.
        page_size (int, default=_DEFAULT_PAGE_SIZE): Size of the page.

    Returns:
        Tuple[pandas.DataFrame, DataFrameMetadata]: A tuple containing the created dataframe and its metadata.
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

    index, primary_labels_from_index = _headers_to_index(
        dim_idx=0,
        headers=full_headers,
        response=execution_response,
        label_overrides=label_overrides,
        use_local_ids_in_headers=use_local_ids_in_headers,
        use_primary_labels_in_attributes=use_primary_labels_in_attributes,
    )

    columns, primary_labels_from_columns = _headers_to_index(
        dim_idx=1,
        headers=full_headers,
        response=execution_response,
        label_overrides=label_overrides,
        use_local_ids_in_headers=use_local_ids_in_headers,
        use_primary_labels_in_attributes=use_primary_labels_in_attributes,
    )

    df = pandas.DataFrame(
        data=full_data,
        index=index,
        columns=columns,
    )

    return df, DataFrameMetadata.from_data(
        headers=full_headers,
        execution_response=execution_response,
        primary_labels_from_index=primary_labels_from_index,
        primary_labels_from_columns=primary_labels_from_columns,
    )
