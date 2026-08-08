import pytest

from llm_quality_harness.evaluator import Evaluator
from llm_quality_harness.models import EvaluationCase
from llm_quality_harness.runner import run_suite
from llm_quality_harness.statistics import compare_suites


def suite(evaluator: Evaluator, suite_id: str, case_id: str):  # type: ignore[no-untyped-def]
    case = EvaluationCase(
        id=case_id,
        prompt="Define evidence",
        response="Evidence is a measured result",
        reference_answer="Evidence is a measured result",
    )
    return run_suite(
        [case], evaluator, suite_id=suite_id, dataset_version="1", policy_version="1"
    )


def test_single_case_interval(evaluator: Evaluator) -> None:
    comparison = compare_suites(suite(evaluator, "base", "same"), suite(evaluator, "new", "same"))
    assert comparison.confidence_interval_95 == (0.0, 0.0)


def test_comparison_requires_shared_ids(evaluator: Evaluator) -> None:
    with pytest.raises(ValueError, match="no shared"):
        compare_suites(suite(evaluator, "base", "one"), suite(evaluator, "new", "two"))

