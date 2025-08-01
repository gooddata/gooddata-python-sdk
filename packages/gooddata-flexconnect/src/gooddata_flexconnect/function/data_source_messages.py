# (C) 2025 GoodData Corporation
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, Optional

import orjson
import pyarrow

_DATA_SOURCE_MESSAGES_KEY = b"x-gdc-data-source-messages"
"""
Key used in the PyArrow metadata to carry the data source messages.
"""


@dataclass(frozen=True)
class DataSourceMessage:
    """
    A message sent by the data source. This will be included in the execution results' metadata.
    """

    source: str
    """
    Identification of the source of the message, typically the id or other identifier of the data source.
    """

    correlation_id: str
    """
    Unique id of the operation, meant to correlate different messages together.
    """

    type: str
    """
    Type of the message, currently free-form, we might define some enum for these in the future.
    """

    data: Optional[Any] = None
    """
    Optional message-specific data. This can be anything that can be JSON-serialized.
    Try to keep this as small as possible: the backend has a quite strict size limit on the messages.
    """

    def to_dict(self) -> dict[str, Any]:
        """
        Converts this instance to its dictionary representation.
        """
        return {"source": self.source, "correlation_id": self.correlation_id, "type": self.type, "data": self.data}


def add_data_source_messages_metadata(
    data_source_messages: Iterable[DataSourceMessage], original_metadata: Optional[dict] = None
) -> dict[bytes, bytes]:
    """
    Given a list of DataSourceMessages, creates a PyArrow-compatible metadata dictionary.

    This is useful when creating a PyArrow Table directly:

    >>> t = pyarrow.table(
    ...     [1, 2, 3],
    ...     ["test"],
    ...     metadata=add_data_source_messages_metadata(
    ...         [DataSourceMessage(correlation_id="123", source="test_source", type="info")]
    ...     ),
    ... )

    You can also add other metadata as needed:
    >>> t2 = pyarrow.table(
    ...     [1, 2, 3],
    ...     ["test"],
    ...     metadata=add_data_source_messages_metadata(
    ...         [DataSourceMessage(correlation_id="123", source="test_source", type="info")],
    ...         original_metadata={b"some": b"extra metadata"},
    ...     ),
    ... )

    :param data_source_messages: list of DataSourceMessages to include
    :param original_metadata: original medata to add the DataSourceMessages to.
    :return: a new metadata dictionary
    """
    if original_metadata is None:
        original_metadata = {}
    return {**original_metadata, _DATA_SOURCE_MESSAGES_KEY: orjson.dumps(data_source_messages)}


def with_data_source_messages(
    data_source_messages: Iterable[DataSourceMessage], schema: pyarrow.Schema
) -> pyarrow.Schema:
    """
    Given a schema and a list of DataSourceMessages, returns a new schema with the DataSourceMessages included.

    This is useful when creating PyArrow RecordBatchReaders:

    >>> s = with_data_source_messages(
    ...     [DataSourceMessage(correlation_id="123", source="test_source", type="info")],
    ...     pyarrow.schema(...),  # the original schema for your RecordBatchReader
    ... )
    >>> rbr = pyarrow.RecordBatchReader.from_batches(schema=s, batches=...)

    :param schema: the schema to enrich with the DataSourceMessages
    :param data_source_messages: list of DataSourceMessages to include
    """
    return schema.with_metadata(add_data_source_messages_metadata(data_source_messages, schema.metadata))
