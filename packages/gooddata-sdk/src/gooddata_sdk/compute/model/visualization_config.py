# (C) 2025 GoodData Corporation
from __future__ import annotations

from typing import Any


class ForecastConfig:
    """Wrapper for ForecastConfig returned by AI chat visualization."""

    def __init__(self, forecast_period: int, confidence_level: float, seasonal: bool) -> None:
        self.forecast_period = forecast_period
        self.confidence_level = confidence_level
        self.seasonal = seasonal

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ForecastConfig:
        return cls(
            forecast_period=data["forecastPeriod"],
            confidence_level=data["confidenceLevel"],
            seasonal=data["seasonal"],
        )

    def __repr__(self) -> str:
        return (
            f"ForecastConfig(forecast_period={self.forecast_period!r}, "
            f"confidence_level={self.confidence_level!r}, seasonal={self.seasonal!r})"
        )


class ClusteringConfig:
    """Wrapper for ClusteringConfig returned by AI chat visualization."""

    def __init__(self, number_of_clusters: int, threshold: float) -> None:
        self.number_of_clusters = number_of_clusters
        self.threshold = threshold

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ClusteringConfig:
        return cls(
            number_of_clusters=data["numberOfClusters"],
            threshold=data["threshold"],
        )

    def __repr__(self) -> str:
        return f"ClusteringConfig(number_of_clusters={self.number_of_clusters!r}, threshold={self.threshold!r})"


class AnomalyDetectionConfig:
    """Wrapper for AnomalyDetectionConfig returned by AI chat visualization."""

    def __init__(self, sensitivity: str | None = None) -> None:
        self.sensitivity = sensitivity

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AnomalyDetectionConfig:
        return cls(sensitivity=data.get("sensitivity"))

    def __repr__(self) -> str:
        return f"AnomalyDetectionConfig(sensitivity={self.sensitivity!r})"


class VisualizationConfig:
    """Wrapper for VisualizationConfig returned by AI chat visualization."""

    def __init__(
        self,
        forecast: ForecastConfig | None = None,
        clustering: ClusteringConfig | None = None,
        anomaly_detection: AnomalyDetectionConfig | None = None,
    ) -> None:
        self.forecast = forecast
        self.clustering = clustering
        self.anomaly_detection = anomaly_detection

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> VisualizationConfig:
        forecast = None
        if "forecast" in data and data["forecast"] is not None:
            forecast = ForecastConfig.from_dict(data["forecast"])

        clustering = None
        if "clustering" in data and data["clustering"] is not None:
            clustering = ClusteringConfig.from_dict(data["clustering"])

        anomaly_detection = None
        if "anomalyDetection" in data and data["anomalyDetection"] is not None:
            anomaly_detection = AnomalyDetectionConfig.from_dict(data["anomalyDetection"])

        return cls(forecast=forecast, clustering=clustering, anomaly_detection=anomaly_detection)

    def __repr__(self) -> str:
        return (
            f"VisualizationConfig(forecast={self.forecast!r}, "
            f"clustering={self.clustering!r}, anomaly_detection={self.anomaly_detection!r})"
        )
