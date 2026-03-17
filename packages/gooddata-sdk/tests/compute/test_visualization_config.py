# (C) 2025 GoodData Corporation
from unittest.mock import MagicMock

import pytest
from gooddata_sdk import AnomalyDetectionConfig, ClusteringConfig, ForecastConfig, VisualizationConfig


class TestForecastConfig:
    def test_from_dict_all_fields(self):
        data = {"forecastPeriod": 12, "confidenceLevel": 0.95, "seasonal": True}
        config = ForecastConfig.from_dict(data)
        assert config.forecast_period == 12
        assert config.confidence_level == 0.95
        assert config.seasonal is True

    def test_from_dict_non_seasonal(self):
        data = {"forecastPeriod": 6, "confidenceLevel": 0.80, "seasonal": False}
        config = ForecastConfig.from_dict(data)
        assert config.forecast_period == 6
        assert config.confidence_level == 0.80
        assert config.seasonal is False

    def test_repr(self):
        config = ForecastConfig(forecast_period=12, confidence_level=0.95, seasonal=True)
        assert "ForecastConfig" in repr(config)
        assert "12" in repr(config)


class TestClusteringConfig:
    def test_from_dict(self):
        data = {"numberOfClusters": 5, "threshold": 0.75}
        config = ClusteringConfig.from_dict(data)
        assert config.number_of_clusters == 5
        assert config.threshold == 0.75

    def test_repr(self):
        config = ClusteringConfig(number_of_clusters=3, threshold=0.5)
        assert "ClusteringConfig" in repr(config)
        assert "3" in repr(config)


class TestAnomalyDetectionConfig:
    def test_from_dict_with_sensitivity(self):
        data = {"sensitivity": "HIGH"}
        config = AnomalyDetectionConfig.from_dict(data)
        assert config.sensitivity == "HIGH"

    def test_from_dict_without_sensitivity(self):
        data = {}
        config = AnomalyDetectionConfig.from_dict(data)
        assert config.sensitivity is None

    def test_repr(self):
        config = AnomalyDetectionConfig(sensitivity="LOW")
        assert "AnomalyDetectionConfig" in repr(config)
        assert "LOW" in repr(config)


class TestVisualizationConfig:
    def test_from_dict_with_forecast(self):
        data = {
            "forecast": {"forecastPeriod": 12, "confidenceLevel": 0.95, "seasonal": True},
        }
        config = VisualizationConfig.from_dict(data)
        assert config.forecast is not None
        assert config.forecast.forecast_period == 12
        assert config.clustering is None
        assert config.anomaly_detection is None

    def test_from_dict_with_clustering(self):
        data = {
            "clustering": {"numberOfClusters": 4, "threshold": 0.6},
        }
        config = VisualizationConfig.from_dict(data)
        assert config.clustering is not None
        assert config.clustering.number_of_clusters == 4
        assert config.forecast is None
        assert config.anomaly_detection is None

    def test_from_dict_with_anomaly_detection(self):
        data = {
            "anomalyDetection": {"sensitivity": "MEDIUM"},
        }
        config = VisualizationConfig.from_dict(data)
        assert config.anomaly_detection is not None
        assert config.anomaly_detection.sensitivity == "MEDIUM"
        assert config.forecast is None
        assert config.clustering is None

    def test_from_dict_empty(self):
        config = VisualizationConfig.from_dict({})
        assert config.forecast is None
        assert config.clustering is None
        assert config.anomaly_detection is None

    def test_from_dict_none_values(self):
        data = {"forecast": None, "clustering": None, "anomalyDetection": None}
        config = VisualizationConfig.from_dict(data)
        assert config.forecast is None
        assert config.clustering is None
        assert config.anomaly_detection is None

    def test_repr(self):
        config = VisualizationConfig()
        assert "VisualizationConfig" in repr(config)


class TestExtractVisualizationConfig:
    def _make_chat_result(self, config_data):
        chat_result = MagicMock()
        vis_object = {"metrics": [], "filters": [], "dimensionality": []}
        if config_data is not None:
            vis_object["config"] = config_data
        chat_result.created_visualizations = {"objects": [vis_object]}
        return chat_result

    def test_extract_forecast_config(self):
        from gooddata_sdk.compute.service import ComputeService

        service = MagicMock(spec=ComputeService)
        service.extract_visualization_config = ComputeService.extract_visualization_config.__get__(service)

        chat_result = self._make_chat_result(
            {"forecast": {"forecastPeriod": 10, "confidenceLevel": 0.9, "seasonal": False}}
        )
        result = ComputeService.extract_visualization_config(service, chat_result)
        assert result is not None
        assert isinstance(result, VisualizationConfig)
        assert result.forecast is not None
        assert result.forecast.forecast_period == 10

    def test_extract_no_config(self):
        from gooddata_sdk.compute.service import ComputeService

        service = MagicMock(spec=ComputeService)
        chat_result = self._make_chat_result(None)
        result = ComputeService.extract_visualization_config(service, chat_result)
        assert result is None

    def test_extract_empty_objects(self):
        from gooddata_sdk.compute.service import ComputeService

        service = MagicMock(spec=ComputeService)
        chat_result = MagicMock()
        chat_result.created_visualizations = {"objects": []}
        result = ComputeService.extract_visualization_config(service, chat_result)
        assert result is None
