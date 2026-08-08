from __future__ import annotations

from pathlib import Path

import pytest

from llm_quality_harness.config import load_evaluation_config
from llm_quality_harness.evaluator import Evaluator
from llm_quality_harness.models import EvaluationCase


@pytest.fixture
def project_root() -> Path:
    return Path(__file__).parents[1]


@pytest.fixture
def evaluator(project_root: Path) -> Evaluator:
    return Evaluator(load_evaluation_config(project_root / "config/evaluation.yaml"))


@pytest.fixture
def answer_case() -> EvaluationCase:
    return EvaluationCase(
        id="case-1",
        prompt="What is quality evidence?",
        response="Quality evidence is a measured result [DOC-1].",
        reference_answer="Quality evidence is a measured result [DOC-1].",
        expected_facts=["measured result"],
        contexts=[{"id": "DOC-1", "text": "Quality evidence is a measured result [DOC-1]."}],
        latency_ms=10,
        tags=["quality"],
    )

