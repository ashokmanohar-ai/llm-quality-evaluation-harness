from __future__ import annotations

import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from llm_quality_harness import __version__
from llm_quality_harness.config import Settings, load_evaluation_config, load_yaml
from llm_quality_harness.evaluator import Evaluator
from llm_quality_harness.gate import evaluate_gate
from llm_quality_harness.models import (
    CaseResult,
    ComparisonResult,
    EvaluationRequest,
    GateReport,
    SuiteRequest,
    SuiteResult,
)
from llm_quality_harness.runner import run_dataset, run_suite
from llm_quality_harness.statistics import compare_suites
from llm_quality_harness.store import ResultStore


def create_app(settings: Settings | None = None) -> FastAPI:
    active = settings or Settings.from_env()
    evaluation_config = load_evaluation_config(active.evaluation_config)
    gate_config = load_yaml(active.gate_config)
    evaluator = Evaluator(evaluation_config)
    store = ResultStore(active.store_path)
    static_dir = Path(__file__).parent / "static"

    application = FastAPI(
        title="LLM Quality Evaluation Harness",
        version=__version__,
        description="Governed evaluation and regression gates for LLM, RAG, and agentic systems.",
    )
    application.mount("/static", StaticFiles(directory=static_dir), name="static")

    @application.middleware("http")
    async def correlation_id(request: Request, call_next):  # type: ignore[no-untyped-def]
        request_id = request.headers.get("x-correlation-id", str(uuid.uuid4()))
        response = await call_next(request)
        response.headers["x-correlation-id"] = request_id
        response.headers["x-content-type-options"] = "nosniff"
        response.headers["x-frame-options"] = "DENY"
        return response

    @application.get("/", include_in_schema=False)
    def dashboard() -> FileResponse:
        return FileResponse(static_dir / "index.html")

    @application.get("/health")
    def health() -> dict[str, str]:
        return {"status": "healthy", "version": __version__}

    @application.get("/api/info")
    def info() -> dict[str, object]:
        return {
            "name": "llm-quality-evaluation-harness",
            "version": __version__,
            "evaluator": evaluator.version,
            "policy_version": str(gate_config.get("version", "unknown")),
            "offline_baseline": True,
            "metrics": list(evaluator.weights),
        }

    @application.post("/api/evaluate", response_model=CaseResult)
    def evaluate_case(request: EvaluationRequest) -> CaseResult:
        return evaluator.evaluate(request.case)

    @application.post("/api/suites", response_model=SuiteResult)
    def evaluate_suite(request: SuiteRequest) -> SuiteResult:
        result = run_suite(
            request.cases,
            evaluator,
            suite_id=request.suite_id,
            dataset_version=request.dataset_version,
            policy_version=str(gate_config.get("version", "unknown")),
        )
        store.save(result)
        return result

    @application.post("/api/demo", response_model=SuiteResult)
    def run_demo() -> SuiteResult:
        result = run_dataset(
            active.dataset, evaluator, str(gate_config.get("version", "unknown"))
        )
        store.save(result)
        return result

    @application.get("/api/results", response_model=list[SuiteResult])
    def list_results(limit: int = Query(default=20, ge=1, le=100)) -> list[SuiteResult]:
        return store.list(limit)

    @application.get("/api/results/{suite_id}", response_model=SuiteResult)
    def get_result(suite_id: str) -> SuiteResult:
        result = store.get(suite_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Suite result not found")
        return result

    @application.get("/api/results/{suite_id}/gate", response_model=GateReport)
    def gate_result(suite_id: str) -> GateReport:
        result = store.get(suite_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Suite result not found")
        return evaluate_gate(result, gate_config)

    @application.get("/api/comparisons", response_model=ComparisonResult)
    def compare(baseline: str, candidate: str) -> ComparisonResult:
        baseline_result = store.get(baseline)
        candidate_result = store.get(candidate)
        if baseline_result is None or candidate_result is None:
            raise HTTPException(status_code=404, detail="Baseline or candidate result not found")
        return compare_suites(
            baseline_result,
            candidate_result,
            regression_threshold=float(gate_config.get("maximum_regression", 0.03)),
        )

    return application


app = create_app()
