from pathlib import Path

from fastapi.testclient import TestClient

from llm_quality_harness.api import create_app
from llm_quality_harness.config import Settings


def client(tmp_path: Path, project_root: Path) -> TestClient:
    settings = Settings(
        project_root=project_root,
        evaluation_config=project_root / "config/evaluation.yaml",
        gate_config=project_root / "config/quality-gates.yaml",
        dataset=project_root / "datasets/golden.json",
        store_path=tmp_path / "api-results.db",
        host="127.0.0.1",
        port=8000,
    )
    return TestClient(create_app(settings))


def test_health_and_security_headers(tmp_path: Path, project_root: Path) -> None:
    response = client(tmp_path, project_root).get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-correlation-id"]


def test_demo_gate_and_not_found(tmp_path: Path, project_root: Path) -> None:
    api = client(tmp_path, project_root)
    demo = api.post("/api/demo")
    assert demo.status_code == 200
    suite_id = demo.json()["suite_id"]
    gate = api.get(f"/api/results/{suite_id}/gate")
    assert gate.json()["decision"] == "pass"
    assert api.get("/api/results/missing").status_code == 404


def test_single_case_evaluation(tmp_path: Path, project_root: Path) -> None:
    response = client(tmp_path, project_root).post(
        "/api/evaluate",
        json={
            "case": {
                "id": "api-1",
                "prompt": "What is a baseline?",
                "response": "A baseline is a reference result.",
                "reference_answer": "A baseline is a reference result."
            }
        },
    )
    assert response.status_code == 200
    assert response.json()["status"] == "passed"


def test_dashboard_loads(tmp_path: Path, project_root: Path) -> None:
    response = client(tmp_path, project_root).get("/")
    assert response.status_code == 200
    assert "Turn model behavior" in response.text


def test_suite_list_info_and_comparison(tmp_path: Path, project_root: Path) -> None:
    api = client(tmp_path, project_root)
    case = {
        "id": "shared",
        "prompt": "What is evidence?",
        "response": "Evidence is a measured result.",
        "reference_answer": "Evidence is a measured result."
    }
    assert api.get("/api/info").json()["offline_baseline"] is True
    baseline = api.post(
        "/api/suites",
        json={"suite_id": "baseline", "dataset_version": "1", "cases": [case]},
    )
    candidate = api.post(
        "/api/suites",
        json={"suite_id": "candidate", "dataset_version": "1", "cases": [case]},
    )
    assert baseline.status_code == candidate.status_code == 200
    assert len(api.get("/api/results?limit=1").json()) == 1
    comparison = api.get("/api/comparisons?baseline=baseline&candidate=candidate")
    assert comparison.status_code == 200
    assert comparison.json()["mean_delta"] == 0
    assert api.get("/api/comparisons?baseline=missing&candidate=candidate").status_code == 404
