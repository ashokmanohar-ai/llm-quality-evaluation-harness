from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping

from .semantic_integrations import normalize_semantic_score


@dataclass(frozen=True)
class LLMQualityScores:
    groundedness: float
    hallucination_resistance: float
    task_completion: float
    policy_adherence: float

    @property
    def weighted_score(self) -> float:
        return round(
            self.groundedness * 0.35
            + self.hallucination_resistance * 0.30
            + self.task_completion * 0.20
            + self.policy_adherence * 0.15,
            4,
        )


class DeepEvalAdapter:
    """Stable harness contract for DeepEval-style semantic evaluators."""

    def __init__(self, evaluator: Callable[[Mapping[str, object]], Mapping[str, float]]) -> None:
        self._evaluator = evaluator

    def evaluate(self, case: Mapping[str, object]) -> LLMQualityScores:
        raw = self._evaluator(case)
        required = (
            'groundedness',
            'hallucination_resistance',
            'task_completion',
            'policy_adherence',
        )
        missing = [name for name in required if name not in raw]
        if missing:
            raise ValueError(f'missing semantic LLM metrics: {", ".join(missing)}')
        return LLMQualityScores(
            groundedness=normalize_semantic_score(raw['groundedness']),
            hallucination_resistance=normalize_semantic_score(raw['hallucination_resistance']),
            task_completion=normalize_semantic_score(raw['task_completion']),
            policy_adherence=normalize_semantic_score(raw['policy_adherence']),
        )


def build_deepeval_adapter() -> DeepEvalAdapter:
    from .semantic_integrations import require_integration

    require_integration('deepeval')

    def _not_configured(_: Mapping[str, object]) -> Mapping[str, float]:
        raise RuntimeError(
            'DeepEval is installed but no judge/model configuration has been supplied. '
            'Inject an approved DeepEval callable into DeepEvalAdapter.'
        )

    return DeepEvalAdapter(_not_configured)
