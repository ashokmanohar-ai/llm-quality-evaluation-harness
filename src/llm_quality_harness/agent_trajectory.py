from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class AgentStep:
    name: str
    tool: str | None = None
    success: bool = True
    latency_ms: int = 0
    retry_count: int = 0
    expected_tool: str | None = None


@dataclass(frozen=True)
class TrajectoryScore:
    task_completion: float
    tool_selection: float
    trajectory_efficiency: float
    recovery_success: float
    weighted_score: float


def _ratio(passed: int, total: int) -> float:
    return 1.0 if total == 0 else passed / total


def score_trajectory(
    steps: Iterable[AgentStep],
    *,
    task_completed: bool,
    max_expected_steps: int | None = None,
) -> TrajectoryScore:
    """Score an agent trajectory using deterministic, explainable checks.

    This intentionally avoids an LLM judge. Semantic trajectory judges can be layered on
    later, but deterministic tool, retry and completion evidence should remain separately
    inspectable for release decisions.
    """
    materialized = list(steps)
    tool_steps = [step for step in materialized if step.tool is not None]
    expected_tool_steps = [step for step in tool_steps if step.expected_tool is not None]

    correct_tools = sum(step.tool == step.expected_tool for step in expected_tool_steps)
    tool_selection = _ratio(correct_tools, len(expected_tool_steps))

    failed_steps = [step for step in materialized if not step.success]
    recovered_failures = sum(
        any(later.success for later in materialized[index + 1 :])
        for index, step in enumerate(materialized)
        if not step.success
    )
    recovery_success = _ratio(recovered_failures, len(failed_steps))

    expected = max_expected_steps or max(1, len(materialized))
    excess = max(0, len(materialized) - expected)
    retries = sum(step.retry_count for step in materialized)
    penalty = min(1.0, (excess + retries) / max(1, expected))
    trajectory_efficiency = 1.0 - penalty

    task_completion = 1.0 if task_completed else 0.0
    weighted_score = (
        task_completion * 0.40
        + tool_selection * 0.25
        + trajectory_efficiency * 0.20
        + recovery_success * 0.15
    )

    return TrajectoryScore(
        task_completion=round(task_completion, 4),
        tool_selection=round(tool_selection, 4),
        trajectory_efficiency=round(trajectory_efficiency, 4),
        recovery_success=round(recovery_success, 4),
        weighted_score=round(weighted_score, 4),
    )
