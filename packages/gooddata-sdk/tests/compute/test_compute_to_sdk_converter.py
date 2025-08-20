# (C) 2024 GoodData Corporation
import json

from gooddata_sdk import (
    AbsoluteDateFilter,
    ArithmeticMetric,
    Attribute,
    ComputeToSdkConverter,
    MetricValueFilter,
    NegativeAttributeFilter,
    PopDateMetric,
    PopDatesetMetric,
    PositiveAttributeFilter,
    RankingFilter,
    RelativeDateFilter,
    SimpleMetric,
)


def test_attribute_conversion():
    attribute_dict = json.loads(
        """
        {
          "label": {
            "identifier": { "id": "attribute1", "type": "label" }
          },
          "localIdentifier": "a_attribute1",
          "showAllValues": true
        }
        """
    )

    result = ComputeToSdkConverter.convert_attribute(attribute_dict)

    assert isinstance(result, Attribute)
    assert result.local_id == "a_attribute1"
    assert result.label.id == "attribute1"
    assert result.show_all_values is True


def test_positive_attribute_filter_conversion():
    filter_dict = json.loads(
        """
        {
          "positiveAttributeFilter": {
            "label": {
              "identifier": { "id": "attribute1", "type": "label" }
            },
            "in": {
              "values": [ "val1", "val2" ]
            }
          }
        }
        """
    )

    result = ComputeToSdkConverter.convert_filter(filter_dict)

    assert isinstance(result, PositiveAttributeFilter)
    assert result.label.id == "attribute1"
    assert result.values == ["val1", "val2"]


def test_negative_attribute_filter_conversion():
    filter_dict = json.loads(
        """
        {
          "negativeAttributeFilter": {
            "label": {
              "identifier": { "id": "attribute1", "type": "label" }
            },
            "notIn": {
              "values": [ "val1", "val2" ]
            }
          }
        }
        """
    )

    result = ComputeToSdkConverter.convert_filter(filter_dict)

    assert isinstance(result, NegativeAttributeFilter)
    assert result.label.id == "attribute1"
    assert result.values == ["val1", "val2"]


def test_relative_date_filter_conversion():
    filter_dict = json.loads(
        """
        {
          "relativeDateFilter": {
            "dataset": {
              "identifier": { "id": "date", "type": "dataset" }
            },
            "granularity": "QUARTER",
            "from": -3,
            "to": 0
          }
        }
        """
    )

    result = ComputeToSdkConverter.convert_filter(filter_dict)

    assert isinstance(result, RelativeDateFilter)
    assert result.dataset.id == "date"
    assert result.granularity == "QUARTER"
    assert result.from_shift == -3
    assert result.to_shift == 0


def test_absolute_date_filter_conversion():
    filter_dict = json.loads(
        """
        {
          "absoluteDateFilter": {
            "dataset": {
              "identifier": { "id": "date", "type": "dataset" }
            },
            "from": "2024-07-12 10:00",
            "to": "2024-08-12 20:59"
          }
        }
        """
    )

    result = ComputeToSdkConverter.convert_filter(filter_dict)

    assert isinstance(result, AbsoluteDateFilter)
    assert result.dataset.id == "date"
    assert result.from_date == "2024-07-12 10:00"
    assert result.to_date == "2024-08-12 20:59"


def test_comparison_measure_value_filter_conversion():
    filter_dict = json.loads(
        """
        {
          "comparisonMeasureValueFilter": {
            "measure": { "localIdentifier": "measureLocalId" },
            "operator": "GREATER_THAN",
            "value": 100,
            "treatNullValuesAs": 0
          }
        }
        """
    )

    result = ComputeToSdkConverter.convert_filter(filter_dict)

    assert isinstance(result, MetricValueFilter)
    assert result.metric == "measureLocalId"
    assert result.operator == "GREATER_THAN"
    assert result.values == (100,)
    assert result.treat_nulls_as == 0


def test_range_measure_value_filter_conversion():
    filter_dict = json.loads(
        """
        {
          "rangeMeasureValueFilter": {
            "measure": { "localIdentifier": "measureLocalId" },
            "operator": "BETWEEN",
            "from": 100,
            "to": 200,
            "treatNullValuesAs": 42
          }
        }
        """
    )

    result = ComputeToSdkConverter.convert_filter(filter_dict)

    assert isinstance(result, MetricValueFilter)
    assert result.metric == "measureLocalId"
    assert result.operator == "BETWEEN"
    assert result.values == (100, 200)
    assert result.treat_nulls_as == 42


def test_ranking_filter_conversion():
    filter_dict = json.loads(
        """
        {
          "rankingFilter": {
            "measures": [{
                "localIdentifier": "measure1.localId"
            }],
            "operator": "TOP",
            "value": 5
          }
        }
        """
    )

    result = ComputeToSdkConverter.convert_filter(filter_dict)

    assert isinstance(result, RankingFilter)
    assert result.metrics[0] == "measure1.localId"
    assert result.operator == "TOP"
    assert result.value == 5


def test_ranking_filter_with_dimensionality_conversion():
    filter_dict = json.loads(
        """
        {
          "rankingFilter": {
            "measures": [{
                "localIdentifier": "measure1.localId"
            }],
           "dimensionality": [{
                "localIdentifier": "attribute1.localId"
            }],
            "operator": "TOP",
            "value": 5
          }
        }
        """
    )

    result = ComputeToSdkConverter.convert_filter(filter_dict)

    assert isinstance(result, RankingFilter)
    assert result.metrics[0] == "measure1.localId"
    assert result.dimensionality[0] == "attribute1.localId"
    assert result.operator == "TOP"
    assert result.value == 5


def test_simple_metric_conversion():
    metric_dict = json.loads(
        """
        {
          "localIdentifier": "m_fact1_max",
          "definition": {
            "measure": {
              "item": {
                "identifier": { "id": "fact1", "type": "fact" }
              },
              "filters": [
                {
                  "positiveAttributeFilter": {
                    "label": {
                      "identifier": { "id": "attribute1", "type": "label" }
                    },
                    "in": {
                      "values": [ "value2", "value1" ]
                    }
                  }
                }
              ],
              "aggregation": "MAX"
            }
          }
        }
        """
    )

    result = ComputeToSdkConverter.convert_metric(metric_dict)

    assert isinstance(result, SimpleMetric)
    assert result.local_id == "m_fact1_max"
    assert result.item.id == "fact1"
    assert result.aggregation == "MAX"
    assert isinstance(result.filters[0], PositiveAttributeFilter)


def test_arithmetic_metric_conversion():
    metric_dict = json.loads(
        """
        {
          "localIdentifier": "m_arithmetic",
          "definition": {
            "arithmeticMeasure": {
              "measureIdentifiers": [
                { "localIdentifier": "m_fact1_max" },
                { "localIdentifier": "m_fact2_runsum" }
              ],
              "operator": "MULTIPLICATION"
            }
          }
        }
        """
    )

    result = ComputeToSdkConverter.convert_metric(metric_dict)

    assert isinstance(result, ArithmeticMetric)
    assert result.local_id == "m_arithmetic"
    assert result.operator == "MULTIPLICATION"
    assert result.operand_local_ids == ["m_fact1_max", "m_fact2_runsum"]


def test_over_period_metric_conversion():
    metric_dict = json.loads(
        """
        {
          "localIdentifier": "m_over_period",
          "definition": {
            "overPeriodMeasure": {
              "measureIdentifier": {
                "localIdentifier": "m_price_sum"
              },
              "dateAttributes": [
                {
                  "attribute": {
                    "identifier": { "id": "date.year", "type": "attribute" }
                  },
                  "periodsAgo": 1
                }
              ]
            }
          }
        }
        """
    )

    result = ComputeToSdkConverter.convert_metric(metric_dict)

    assert isinstance(result, PopDateMetric)
    assert result.local_id == "m_over_period"
    assert result.metric_local_id == "m_price_sum"
    assert result.date_attributes[0].attribute.id == "date.year"


def test_previous_period_metric_conversion():
    metric_dict = json.loads(
        """
        {
          "localIdentifier": "m_previous_period",
          "definition": {
            "previousPeriodMeasure": {
              "measureIdentifier": {
                "localIdentifier": "m_price_sum"
              },
              "dateDatasets": [
                {
                  "dataset": {
                    "identifier": { "id": "date", "type": "dataset" }
                  },
                  "periodsAgo": 1
                }
              ]
            }
          }
        }
        """
    )

    result = ComputeToSdkConverter.convert_metric(metric_dict)

    assert isinstance(result, PopDatesetMetric)
    assert result.local_id == "m_previous_period"
    assert result.metric_local_id == "m_price_sum"
    assert result.date_datasets[0].dataset.id == "date"
