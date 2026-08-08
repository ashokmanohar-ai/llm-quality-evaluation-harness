from __future__ import annotations

import re
from collections.abc import Iterable

TOKEN_PATTERN = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)?", re.IGNORECASE)
CITATION_PATTERN = re.compile(r"\[([A-Za-z0-9_.:-]+)\]")


def tokenize(text: str, stopwords: set[str] | None = None) -> list[str]:
    words = [match.group(0).lower() for match in TOKEN_PATTERN.finditer(text)]
    if stopwords:
        return [word for word in words if word not in stopwords]
    return words


def token_set(text: str, stopwords: set[str] | None = None) -> set[str]:
    return set(tokenize(text, stopwords))


def precision_recall_f1(
    candidate: Iterable[str], reference: Iterable[str]
) -> tuple[float, float, float]:
    candidate_set = set(candidate)
    reference_set = set(reference)
    if not candidate_set and not reference_set:
        return 1.0, 1.0, 1.0
    if not candidate_set or not reference_set:
        return 0.0, 0.0, 0.0
    overlap = len(candidate_set & reference_set)
    precision = overlap / len(candidate_set)
    recall = overlap / len(reference_set)
    f1 = 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)
    return precision, recall, f1


def expected_fact_coverage(response: str, facts: list[str], stopwords: set[str]) -> float:
    if not facts:
        return 1.0
    response_tokens = token_set(response, stopwords)
    covered = 0
    for fact in facts:
        fact_tokens = token_set(fact, stopwords)
        if fact_tokens and fact_tokens.issubset(response_tokens):
            covered += 1
    return covered / len(facts)


def extract_citations(text: str) -> list[str]:
    return CITATION_PATTERN.findall(text)
