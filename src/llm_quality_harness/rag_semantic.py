from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping

from .semantic_integrations import normalize_semantic_score


@dataclass(frozen=True)
class RAGSemanticScores:
    faithfulness: float
    context_precision: float
    context_recall: float
    answer_relevance: float

    @property
    def weighted_score(self) -> float:
        return round(
            self.faithfulness * 0.35
            + self.context_precision * 0.20
            + self.context_recall * 0.20
            + self.answer_relevance * 0.25,
            4,
        )


class SemanticRAGEvaluator:
    """Provider-neutral adapter around semantic RAG evaluators such as Ragas.

    The callable contract keeps the harness offline-testable. A production adapter can
    delegate to Ragas, Azure AI evaluation, an internal judge service, or another
    approved evaluator without changing the release-gate model.
    """

    def __init__(self, evaluator: Callable[[Mapping[str, object]], Mapping[str, float]]) -> None:
        self._evaluator = evaluator

    def evaluate(self, case: Mapping[str, object]) -> RAGSemanticScores:
        raw = self._evaluator(case)
        required = (
            'faithfulness',
            'context_precision',
            'context_recall',
            'answer_relevance',
        )
        missing = [name for name in required if name not in raw]
        if missing:
            raise ValueError(f'missing semantic RAG metrics: {", ".join(missing)}')
        return RAGSemanticScores(
            faithfulness=normalize_semantic_score(raw['faithfulness']),
            context_precision=normalize_semantic_score(raw['context_precision']),
            context_recall=normalize_semantic_score(raw['context_recall']),
            answer_relevance=normalize_semantic_score(raw['answer_relevance']),
        )


def build_ragas_evaluator() -> SemanticRAGEvaluator:
    """Return a lazy Ragas adapter when the package is available.

    The implementation intentionally imports Ragas only at call time. This preserves the
    zero-key, offline MVP while documenting the production integration seam.
    """
    from .semantic_integrations import require_integration

    require_integration('ragas')

    def _not_configured(_: Mapping[str, object]) -> Mapping[str, float]:
        raise RuntimeError(
            'Ragas is installed but no model/embedding evaluator has been configured. '
            'Wire an approved Ragas evaluation function into SemanticRAGEvaluator.'
        )

    return SemanticRAGEvaluator(_not_configured)
