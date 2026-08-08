from __future__ import annotations

import math
import statistics

from llm_quality_harness.models import ComparisonResult, SuiteResult


def compare_suites(
    baseline: SuiteResult, candidate: SuiteResult, *, regression_threshold: float = 0.03
) -> ComparisonResult:
    baseline_cases = {case.case_id: case for case in baseline.cases}
    candidate_cases = {case.case_id: case for case in candidate.cases}
    shared = sorted(baseline_cases.keys() & candidate_cases.keys())
    if not shared:
        raise ValueError("baseline and candidate have no shared case IDs")
    deltas = [candidate_cases[key].score - baseline_cases[key].score for key in shared]
    mean_delta = statistics.fmean(deltas)
    margin = (
        1.96 * statistics.stdev(deltas) / math.sqrt(len(deltas))
        if len(deltas) > 1
        else 0.0
    )
    metric_names = baseline.summary.metric_means.keys() & candidate.summary.metric_means.keys()
    metric_deltas = {
        name: round(candidate.summary.metric_means[name] - baseline.summary.metric_means[name], 4)
        for name in sorted(metric_names)
    }
    regressed = [
        key
        for key in shared
        if candidate_cases[key].score - baseline_cases[key].score < -regression_threshold
    ]
    return ComparisonResult(
        baseline_suite_id=baseline.suite_id,
        candidate_suite_id=candidate.suite_id,
        mean_delta=round(mean_delta, 4),
        confidence_interval_95=(round(mean_delta - margin, 4), round(mean_delta + margin, 4)),
        metric_deltas=metric_deltas,
        regressed_case_ids=regressed,
        compared_cases=len(shared),
    )
