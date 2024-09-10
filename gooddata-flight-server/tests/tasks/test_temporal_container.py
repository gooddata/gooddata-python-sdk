#  (C) 2023 GoodData Corporation
import pytest
from gooddata_flight_server.tasks.temporal_container import TemporalContainer


@pytest.fixture(scope="function")
def tc() -> TemporalContainer[str]:
    t: TemporalContainer[str] = TemporalContainer(
        logger_name="test_container",
        grace_period=1,
        entry_evict_fun=lambda _: None,
        start_collector=False,
    )

    t._add_entry("e1", "val1", 1)
    t._add_entry("e2", "val2", 2)
    t._add_entry("e3", "val3", 3)
    t._add_entry("e4", "val4", 4)

    return t


def test_expiration1(tc):
    """
    Typical expiration flow - items are kept in container and evicted
    as time goes on.
    """
    assert tc._evict_expired_items(1.5) == []
    assert tc._evict_expired_items(2) == ["val1"]
    assert tc._evict_expired_items(3.2) == ["val2"]
    assert tc._evict_expired_items(10) == ["val3", "val4"]


def test_expiration2(tc):
    """
    Item is popped from container - so naturally time-based eviction
    will not trigger for it.
    """
    assert tc.pop_entry("e1") == "val1"
    assert tc._evict_expired_items(2) == []


def test_evict_entry(tc):
    assert tc.evict_entry("e1") is True
    assert tc.evict_entry("missing") is False


def test_get_entry(tc):
    assert tc.get_entry("e1") == "val1"
    assert tc.get_entry("missing") is None


def test_iter1(tc):
    assert list(tc.__iter__()) == ["val1", "val2", "val3", "val4"]


def test_close(tc):
    assert len(tc) == 4
    tc.close()
    assert len(tc) == 0

    with pytest.raises(AssertionError):
        tc._add_entry("key", "value", 123)

    with pytest.raises(AssertionError):
        tc.pop_entry("e1")

    with pytest.raises(AssertionError):
        tc.get_entry("e1")

    with pytest.raises(AssertionError):
        tc.evict_entry("e1")
