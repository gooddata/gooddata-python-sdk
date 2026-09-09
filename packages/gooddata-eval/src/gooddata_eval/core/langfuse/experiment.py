# (C) 2026 GoodData Corporation
"""Langfuse experiment root-span construction and score-target resolution."""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from gooddata_eval.core.langfuse.otlp import (
    ATTR_ENVIRONMENT,
    ATTR_EXPERIMENT_DATASET_ID,
    ATTR_EXPERIMENT_DESCRIPTION,
    ATTR_EXPERIMENT_ID,
    ATTR_EXPERIMENT_ITEM_EXPECTED_OUTPUT,
    ATTR_EXPERIMENT_ITEM_ID,
    ATTR_EXPERIMENT_ITEM_METADATA_PREFIX,
    ATTR_EXPERIMENT_ITEM_ROOT_OBSERVATION_ID,
    ATTR_EXPERIMENT_METADATA_PREFIX,
    ATTR_EXPERIMENT_NAME,
    ATTR_OBSERVATION_INPUT,
    ATTR_OBSERVATION_METADATA_PREFIX,
    ATTR_OBSERVATION_OUTPUT,
    ATTR_OBSERVATION_TYPE,
    ATTR_SESSION_ID,
    ATTR_TRACE_METADATA_PREFIX,
    ATTR_TRACE_NAME,
    ATTR_TRACE_TAGS,
    ATTR_VERSION,
    Span,
    flatten_metadata,
    new_span_id,
    new_trace_id,
    otlp_attribute,
)

# Fixed namespace for deriving experiment ids from run names — arbitrary but stable across processes.
_EXPERIMENT_NAMESPACE = uuid.UUID("6f6e2f5a-2f0e-4f0c-9c1b-8f6f2a3b9d10")


def experiment_id_for(run_name: str) -> str:
    return str(uuid.uuid5(_EXPERIMENT_NAMESPACE, run_name))


@dataclass(frozen=True)
class ExperimentRun:
    name: str
    dataset_id: str
    metadata: dict[str, Any] | None = None
    description: str | None = None


@dataclass(frozen=True)
class ExperimentItem:
    item_id: str
    input: Any = None
    output: Any = None
    expected_output: Any = None
    metadata: dict[str, Any] | None = None


def build_experiment_root_span(
    run: ExperimentRun | None,
    item: ExperimentItem,
    *,
    start: datetime,
    end: datetime,
    trace_name: str,
    session_id: str | None = None,
    version: str | None = None,
    tags: tuple[str, ...] = (),
    observation_metadata: dict[str, Any] | None = None,
    trace_metadata: dict[str, Any] | None = None,
    environment: str | None = None,
) -> Span:
    """Build the single root span gd-eval emits per (dataset item, run).

    With `run=None` this is a plain observation span carrying no `langfuse.experiment.*`
    attributes at all — used when there is no experiment to attach the item to.
    """
    if end < start:
        end = start
    span_id = new_span_id()

    attributes: list[dict[str, Any]] = [otlp_attribute(ATTR_OBSERVATION_TYPE, "span")]
    if item.input is not None:
        attributes.append(otlp_attribute(ATTR_OBSERVATION_INPUT, json.dumps(item.input, default=str)))
    if item.output is not None:
        attributes.append(otlp_attribute(ATTR_OBSERVATION_OUTPUT, json.dumps(item.output, default=str)))
    attributes.extend(flatten_metadata(ATTR_OBSERVATION_METADATA_PREFIX, observation_metadata))

    attributes.append(otlp_attribute(ATTR_TRACE_NAME, trace_name))
    if session_id is not None:
        attributes.append(otlp_attribute(ATTR_SESSION_ID, session_id))
    if version is not None:
        attributes.append(otlp_attribute(ATTR_VERSION, version))
    if environment is not None:
        attributes.append(otlp_attribute(ATTR_ENVIRONMENT, environment))
    if tags:
        attributes.append(otlp_attribute(ATTR_TRACE_TAGS, list(tags)))
    attributes.extend(flatten_metadata(ATTR_TRACE_METADATA_PREFIX, trace_metadata))

    if run is not None:
        attributes.append(otlp_attribute(ATTR_EXPERIMENT_ID, experiment_id_for(run.name)))
        attributes.append(otlp_attribute(ATTR_EXPERIMENT_NAME, run.name))
        attributes.append(otlp_attribute(ATTR_EXPERIMENT_DATASET_ID, run.dataset_id))
        if run.description is not None:
            attributes.append(otlp_attribute(ATTR_EXPERIMENT_DESCRIPTION, run.description))
        attributes.extend(flatten_metadata(ATTR_EXPERIMENT_METADATA_PREFIX, run.metadata))

        attributes.append(otlp_attribute(ATTR_EXPERIMENT_ITEM_ID, item.item_id))
        attributes.append(otlp_attribute(ATTR_EXPERIMENT_ITEM_ROOT_OBSERVATION_ID, span_id))
        if item.expected_output is not None:
            attributes.append(
                otlp_attribute(ATTR_EXPERIMENT_ITEM_EXPECTED_OUTPUT, json.dumps(item.expected_output, default=str))
            )
        attributes.extend(flatten_metadata(ATTR_EXPERIMENT_ITEM_METADATA_PREFIX, item.metadata))

    return Span(trace_id=new_trace_id(), span_id=span_id, name=trace_name, start=start, end=end, attributes=attributes)


class ScoreTarget(str):
    """Where a score for one evaluated item is written: the gen-ai trace, gd-eval's own
    experiment root observation, or both.

    The `str` value is the gen-ai trace id when present, else the experiment trace id, else
    empty — so a `ScoreTarget` can be used directly wherever a plain trace id string was used.
    """

    gen_ai_trace_id: str | None
    experiment_trace_id: str | None
    experiment_span_id: str | None

    def __new__(
        cls,
        gen_ai_trace_id: str | None = None,
        experiment_trace_id: str | None = None,
        experiment_span_id: str | None = None,
    ) -> ScoreTarget:
        value = gen_ai_trace_id or experiment_trace_id or ""
        instance = super().__new__(cls, value)
        instance.gen_ai_trace_id = gen_ai_trace_id
        instance.experiment_trace_id = experiment_trace_id
        instance.experiment_span_id = experiment_span_id
        return instance

    def destinations(self) -> list[tuple[str, str | None]]:
        """Score write destinations as `(trace_id, observation_id)` pairs, gen-ai first."""
        targets: list[tuple[str, str | None]] = []
        if self.gen_ai_trace_id:
            targets.append((self.gen_ai_trace_id, None))
        if self.experiment_trace_id:
            targets.append((self.experiment_trace_id, self.experiment_span_id))
        return targets
