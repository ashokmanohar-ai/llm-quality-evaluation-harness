from pathlib import Path

from llm_quality_harness.config import load_yaml
from llm_quality_harness.evaluator import Evaluator
from llm_quality_harness.gate import evaluate_gate
from llm_quality_harness.runner import load_dataset, run_dataset


def test_reference_suite_passes(
    project_root: Path, evaluator: Evaluator
) -> None:
    result = run_dataset(project_root / "datasets/golden.json", evaluator, "1.0")
    gate = evaluate_gate(result, load_yaml(project_root / "config/quality-gates.yaml"))
    assert result.summary.total_cases == 8
    assert result.summary.failed_cases == 0
    assert gate.decision == "pass"


def test_dataset_manifest(project_root: Path) -> None:
    suite_id, version, cases = load_dataset(project_root / "datasets/golden.json")
    assert suite_id == "reference-suite-v1"
    assert version == "1.0.0"
    assert len(cases) == 8

