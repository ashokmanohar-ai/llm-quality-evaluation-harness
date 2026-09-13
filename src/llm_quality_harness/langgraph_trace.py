from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .agent_trajectory import AgentStep, TrajectoryScore, score_trajectory


@dataclass(frozen=True)
class TraceEvaluation:
    trace_id: str
    step_count: int
    tool_calls: int
    score: TrajectoryScore


def _tool_name(event: Mapping[str, object]) -> str | None:
    tool = event.get('tool') or event.get('tool_name')
    return str(tool) if tool else None


def normalize_langgraph_events(events: Iterable[Mapping[str, object]]) -> list[AgentStep]:
    """Normalize framework trace events into the harness' stable trajectory contract.

    The adapter accepts simple dictionary events so callers can transform LangGraph,
    OpenTelemetry, or gateway-specific traces without coupling the scoring engine to a
    specific tracing backend.
    """
    steps: list[AgentStep] = []
    for index, event in enumerate(events, start=1):
        name = str(event.get('name') or event.get('node') or f'step-{index}')
        success = bool(event.get('success', True))
        latency = int(event.get('latency_ms', 0) or 0)
        retries = int(event.get('retry_count', 0) or 0)
        expected = event.get('expected_tool')
        steps.append(
            AgentStep(
                name=name,
                tool=_tool_name(event),
                success=success,
                latency_ms=latency,
                retry_count=retries,
                expected_tool=str(expected) if expected else None,
            )
        )
    return steps


def evaluate_agent_trace(
    trace_id: str,
    events: Iterable[Mapping[str, object]],
    *,
    task_completed: bool,
    max_expected_steps: int | None = None,
) -> TraceEvaluation:
    normalized = normalize_langgraph_events(events)
    score = score_trajectory(
        normalized,
        task_completed=task_completed,
        max_expected_steps=max_expected_steps,
    )
    return TraceEvaluation(
        trace_id=trace_id,
        step_count=len(normalized),
        tool_calls=sum(step.tool is not None for step in normalized),
        score=score,
    )
