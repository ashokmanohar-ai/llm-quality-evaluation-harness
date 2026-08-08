from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


class ContextDocument(BaseModel):
    id: str
    text: str
    source: str | None = None


class Usage(BaseModel):
    input_tokens: int = Field(default=0, ge=0)
    output_tokens: int = Field(default=0, ge=0)
    cost_usd: float = Field(default=0.0, ge=0)

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens


class EvaluationCase(BaseModel):
    id: str
    prompt: str
    response: str
    reference_answer: str = ""
    expected_facts: list[str] = Field(default_factory=list)
    contexts: list[ContextDocument] = Field(default_factory=list)
    expected_behavior: Literal["answer", "refuse"] = "answer"
    required_json_fields: list[str] = Field(default_factory=list)
    latency_ms: float = Field(default=0.0, ge=0)
    usage: Usage = Field(default_factory=Usage)
    tags: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_answer_case(self) -> EvaluationCase:
        if self.expected_behavior == "answer" and not self.reference_answer:
            raise ValueError("answer cases require reference_answer")
        return self


class MetricResult(BaseModel):
    score: float = Field(ge=0, le=1)
    passed: bool
    details: str


class SafetyFinding(BaseModel):
    code: str
    severity: Literal["low", "medium", "high", "critical"]
    location: Literal["prompt", "response"]
    evidence: str


class CaseResult(BaseModel):
    case_id: str
    status: Literal["passed", "failed"]
    score: float = Field(ge=0, le=1)
    metrics: dict[str, MetricResult]
    schema_compliant: bool
    safety_findings: list[SafetyFinding] = Field(default_factory=list)
    latency_ms: float = Field(ge=0)
    usage: Usage
    tags: list[str] = Field(default_factory=list)


class SuiteSummary(BaseModel):
    total_cases: int = Field(ge=0)
    passed_cases: int = Field(ge=0)
    failed_cases: int = Field(ge=0)
    mean_score: float = Field(ge=0, le=1)
    metric_means: dict[str, float]
    latency_p95_ms: float = Field(ge=0)
    average_cost_usd: float = Field(ge=0)
    safety_case_pass_rate: float = Field(ge=0, le=1)
    schema_pass_rate: float = Field(ge=0, le=1)


class SuiteResult(BaseModel):
    suite_id: str
    dataset_version: str
    evaluator_version: str
    policy_version: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    summary: SuiteSummary
    cases: list[CaseResult]


class GateFinding(BaseModel):
    gate: str
    passed: bool
    actual: float | bool
    threshold: float | bool
    severity: Literal["blocker", "high", "medium", "low"]
    message: str


class GateReport(BaseModel):
    decision: Literal["pass", "fail"]
    findings: list[GateFinding]


class ComparisonResult(BaseModel):
    baseline_suite_id: str
    candidate_suite_id: str
    mean_delta: float
    confidence_interval_95: tuple[float, float]
    metric_deltas: dict[str, float]
    regressed_case_ids: list[str]
    compared_cases: int


class EvaluationRequest(BaseModel):
    case: EvaluationCase


class SuiteRequest(BaseModel):
    cases: list[EvaluationCase]
    suite_id: str = "api-suite"
    dataset_version: str = "api-v1"


class ErrorResponse(BaseModel):
    detail: str
    correlation_id: str | None = None


JsonObject = dict[str, Any]

