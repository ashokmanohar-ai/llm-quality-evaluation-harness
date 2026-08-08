from pathlib import Path

from llm_quality_harness.evaluator import Evaluator
from llm_quality_harness.runner import run_dataset
from llm_quality_harness.statistics import compare_suites
from llm_quality_harness.store import ResultStore


def test_store_round_trip(
    tmp_path: Path, project_root: Path, evaluator: Evaluator
) -> None:
    result = run_dataset(project_root / "datasets/golden.json", evaluator, "1.0")
    store = ResultStore(tmp_path / "results.db")
    store.save(result)
    assert store.get(result.suite_id) == result
    assert store.list(1) == [result]
    assert store.get("missing") is None


def test_compare_detects_regression(project_root: Path, evaluator: Evaluator) -> None:
    baseline = run_dataset(project_root / "datasets/golden.json", evaluator, "1.0")
    candidate = run_dataset(
        project_root / "datasets/regressed-candidate.json", evaluator, "1.0"
    )
    comparison = compare_suites(baseline, candidate)
    assert comparison.compared_cases == 2
    assert comparison.mean_delta < 0
    assert set(comparison.regressed_case_ids) == {"prompt-injection-007", "rag-grounding-001"}

