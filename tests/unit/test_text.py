from llm_quality_harness.text import (
    expected_fact_coverage,
    extract_citations,
    precision_recall_f1,
    tokenize,
)


def test_tokenize_removes_stopwords() -> None:
    assert tokenize("The model is safe", {"the", "is"}) == ["model", "safe"]


def test_precision_recall_f1() -> None:
    precision, recall, f1 = precision_recall_f1({"a", "b"}, {"b", "c"})
    assert precision == 0.5
    assert recall == 0.5
    assert f1 == 0.5


def test_empty_token_sets_are_equivalent() -> None:
    assert precision_recall_f1([], []) == (1.0, 1.0, 1.0)


def test_expected_fact_coverage_and_citations() -> None:
    response = "Use human approval and audit logs [POL-1]."
    assert expected_fact_coverage(response, ["human approval", "audit logs"], {"and"}) == 1.0
    assert extract_citations(response) == ["POL-1"]

