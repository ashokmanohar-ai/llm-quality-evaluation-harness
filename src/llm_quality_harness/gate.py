from __future__ import annotations

from typing import Any

from llm_quality_harness.models import GateFinding, GateReport, SuiteResult


def evaluate_gate(result: SuiteResult, config: dict[str, Any]) -> GateReport:
    findings: list[GateFinding] = []

    def minimum(name: str, actual: float, threshold: float, severity: str = "high") -> None:
        passed = actual >= threshold
        findings.append(
            GateFinding(
                gate=name,
                passed=passed,
                actual=round(actual, 6),
                threshold=threshold,
                severity=severity,
                message=f"{name}: {actual:.4f} {'meets' if passed else 'is below'} {threshold:.4f}",
            )
        )

    def maximum(name: str, actual: float, threshold: float) -> None:
        passed = actual <= threshold
        findings.append(
            GateFinding(
                gate=name,
                passed=passed,
                actual=round(actual, 6),
                threshold=threshold,
                severity="high",
                message=f"{name}: {actual:.4f} {'meets' if passed else 'exceeds'} {threshold:.4f}",
            )
        )

    minimum(
        "suite_score",
        result.summary.mean_score,
        float(config.get("minimum_suite_score", 0.0)),
    )
    minimum(
        "minimum_case_score",
        min(case.score for case in result.cases),
        float(config.get("minimum_case_score", 0.0)),
    )
    for name, threshold in config.get("minimum_metrics", {}).items():
        minimum(f"metric_{name}", result.summary.metric_means.get(name, 0.0), float(threshold))
    maximum(
        "latency_p95_ms",
        result.summary.latency_p95_ms,
        float(config.get("maximum_latency_p95_ms", float("inf"))),
    )
    maximum(
        "average_cost_usd",
        result.summary.average_cost_usd,
        float(config.get("maximum_average_cost_usd", float("inf"))),
    )
    if config.get("require_all_safety_cases", True):
        minimum("safety_case_pass_rate", result.summary.safety_case_pass_rate, 1.0, "blocker")
    if config.get("require_schema_compliance", True):
        minimum("schema_pass_rate", result.summary.schema_pass_rate, 1.0, "blocker")
    return GateReport(
        decision="pass" if all(finding.passed for finding in findings) else "fail",
        findings=findings,
    )

