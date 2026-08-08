from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from llm_quality_harness.evaluator import Evaluator
from llm_quality_harness.models import EvaluationCase, SuiteResult, SuiteSummary
from llm_quality_harness.providers import DatasetReplayProvider, ResponseProvider


def load_dataset(path: Path) -> tuple[str, str, list[EvaluationCase]]:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict) or not isinstance(payload.get("cases"), list):
        raise ValueError("dataset must be an object containing a cases array")
    cases = [EvaluationCase.model_validate(case) for case in payload["cases"]]
    if not cases:
        raise ValueError("dataset must contain at least one evaluation case")
    case_ids = [case.id for case in cases]
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("evaluation case IDs must be unique")
    return str(payload.get("suite_id", path.stem)), str(payload.get("version", "1")), cases


def run_suite(
    cases: list[EvaluationCase],
    evaluator: Evaluator,
    *,
    suite_id: str,
    dataset_version: str,
    policy_version: str,
    provider: ResponseProvider | None = None,
) -> SuiteResult:
    if not cases:
        raise ValueError("suite requires at least one case")
    active_provider = provider or DatasetReplayProvider()
    evaluated = []
    for case in cases:
        candidate = case.model_copy(update={"response": active_provider.respond(case)})
        evaluated.append(evaluator.evaluate(candidate))

    metric_names = list(evaluator.weights)
    metric_means = {
        name: round(sum(case.metrics[name].score for case in evaluated) / len(evaluated), 4)
        for name in metric_names
    }
    latencies = sorted(case.latency_ms for case in evaluated)
    p95_index = max(0, math.ceil(0.95 * len(latencies)) - 1)
    safety_cases = [case for case in evaluated if "safety" in case.tags]
    safety_pass_rate = (
        sum(case.status == "passed" for case in safety_cases) / len(safety_cases)
        if safety_cases
        else 1.0
    )
    summary = SuiteSummary(
        total_cases=len(evaluated),
        passed_cases=sum(case.status == "passed" for case in evaluated),
        failed_cases=sum(case.status == "failed" for case in evaluated),
        mean_score=round(sum(case.score for case in evaluated) / len(evaluated), 4),
        metric_means=metric_means,
        latency_p95_ms=round(latencies[p95_index], 3),
        average_cost_usd=round(
            sum(case.usage.cost_usd for case in evaluated) / len(evaluated), 6
        ),
        safety_case_pass_rate=round(safety_pass_rate, 4),
        schema_pass_rate=round(
            sum(case.schema_compliant for case in evaluated) / len(evaluated), 4
        ),
    )
    return SuiteResult(
        suite_id=suite_id,
        dataset_version=dataset_version,
        evaluator_version=evaluator.version,
        policy_version=policy_version,
        summary=summary,
        cases=evaluated,
    )


def run_dataset(path: Path, evaluator: Evaluator, policy_version: str) -> SuiteResult:
    suite_id, version, cases = load_dataset(path)
    return run_suite(
        cases,
        evaluator,
        suite_id=suite_id,
        dataset_version=version,
        policy_version=policy_version,
    )


def write_result(result: SuiteResult, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(result.model_dump_json(indent=2), encoding="utf-8")


def read_result(path: Path) -> SuiteResult:
    return SuiteResult.model_validate_json(path.read_text(encoding="utf-8"))


def dataset_manifest(path: Path) -> dict[str, Any]:
    suite_id, version, cases = load_dataset(path)
    return {
        "suite_id": suite_id,
        "version": version,
        "case_count": len(cases),
        "tags": sorted({tag for case in cases for tag in case.tags}),
    }

