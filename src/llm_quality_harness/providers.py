from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from llm_quality_harness.models import EvaluationCase


class ResponseProvider(Protocol):
    """Contract implemented by model, endpoint, replay, or experiment adapters."""

    name: str

    def respond(self, case: EvaluationCase) -> str: ...


class DatasetReplayProvider:
    """Zero-key deterministic provider used by the reference dataset and CI."""

    name = "dataset-replay"

    def respond(self, case: EvaluationCase) -> str:
        return case.response


class CallableProvider:
    """Small adapter for integrating an SDK or internal inference gateway."""

    def __init__(self, name: str, function: Callable[[EvaluationCase], str]) -> None:
        self.name = name
        self.function = function

    def respond(self, case: EvaluationCase) -> str:
        return self.function(case)

