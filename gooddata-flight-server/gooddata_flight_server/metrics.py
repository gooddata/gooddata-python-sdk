#  (C) 2024 GoodData Corporation

from prometheus_client import Counter, Summary


# TODO: metric prefix should be configurable
class ServerMetrics:
    TRIM_SUMMARY = Summary(
        "gdfs_malloc_trim",
        "Summary of malloc trim call durations.",
    )

    TRIM_ERROR_COUNT = Counter(
        "gdfs_malloc_trim_error",
        "Number of times malloc_trim has failed. Repeated failures means big trouble incoming.",
    )
