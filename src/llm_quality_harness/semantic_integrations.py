from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from typing import Any


@dataclass(frozen=True)
class IntegrationStatus:
    name: str
    installed: bool
    detail: str


def integration_status() -> list[IntegrationStatus]:
    """Report optional semantic-evaluation integrations without making them hard deps."""
    integrations = {
        'ragas': 'RAG semantic evaluation',
        'deepeval': 'LLM and agent evaluation',
        'langgraph': 'Agent workflow orchestration',
        'opentelemetry': 'Tracing and observability',
    }
    result: list[IntegrationStatus] = []
    for package, detail in integrations.items():
        try:
            import_module(package)
            installed = True
        except ModuleNotFoundError:
            installed = False
        result.append(IntegrationStatus(package, installed, detail))
    return result


def require_integration(package: str) -> Any:
    """Load an optional integration and fail with an actionable installation message."""
    try:
        return import_module(package)
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            f'Optional integration {package!r} is not installed. '
            'Install the relevant production evaluation extra before using this adapter.'
        ) from exc


def normalize_semantic_score(value: float) -> float:
    """Normalize external evaluator scores to the harness 0..1 contract."""
    if value < 0 or value > 1:
        raise ValueError('semantic evaluator score must be between 0 and 1')
    return round(float(value), 4)
