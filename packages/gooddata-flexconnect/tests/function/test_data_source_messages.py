# (C) 2025 GoodData Corporation
import orjson
import pyarrow
import pytest
from gooddata_flexconnect.function.data_source_messages import (
    _DATA_SOURCE_MESSAGES_KEY,
    DataSourceMessage,
    add_data_source_messages_metadata,
    with_data_source_messages,
)


@pytest.fixture(scope="module")
def sample_schema():
    return pyarrow.schema(
        [
            pyarrow.field("name", pyarrow.string()),
            pyarrow.field("height", pyarrow.int32()),
        ]
    )


@pytest.fixture(scope="module")
def sample_data_source_message():
    return DataSourceMessage(correlation_id="123", source="test_source", type="test")


def test_with_data_source_messages_empty_original(sample_schema, sample_data_source_message):
    augmented_schema = with_data_source_messages([sample_data_source_message], sample_schema)

    # with_data_source_messages creates a copy, the original schema must stay intact
    assert sample_schema.metadata is None

    assert augmented_schema.names == sample_schema.names
    assert augmented_schema.metadata is not None
    assert orjson.loads(augmented_schema.metadata[_DATA_SOURCE_MESSAGES_KEY]) == [sample_data_source_message.to_dict()]


def test_with_data_source_messages_non_empty_original(sample_schema, sample_data_source_message):
    sample_schema_with_some_metadata = sample_schema.with_metadata({b"foo": b"bar"})

    augmented_schema = with_data_source_messages([sample_data_source_message], sample_schema_with_some_metadata)

    # with_data_source_messages creates a copy, the original schema must stay intact
    assert sample_schema_with_some_metadata.metadata == {b"foo": b"bar"}

    # ensure the original metadata is still there
    assert augmented_schema.names == sample_schema.names
    assert augmented_schema.metadata is not None
    assert augmented_schema.metadata[b"foo"] == b"bar"
    assert orjson.loads(augmented_schema.metadata[_DATA_SOURCE_MESSAGES_KEY]) == [sample_data_source_message.to_dict()]


def test_add_data_source_messages_metadata_empty_original(sample_data_source_message):
    metadata = add_data_source_messages_metadata(data_source_messages=[sample_data_source_message])
    assert orjson.loads(metadata[_DATA_SOURCE_MESSAGES_KEY]) == [sample_data_source_message.to_dict()]


def test_add_data_source_messages_metadata_non_empty_original(sample_data_source_message):
    metadata = add_data_source_messages_metadata(
        data_source_messages=[sample_data_source_message], original_metadata={b"foo": b"bar"}
    )
    assert orjson.loads(metadata[_DATA_SOURCE_MESSAGES_KEY]) == [sample_data_source_message.to_dict()]
    assert metadata[b"foo"] == b"bar"
