from pathlib import Path

import pytest

from llm_quality_harness.cli import main


def test_evaluate_gate_compare_commands(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    project_root: Path,
    tmp_path: Path,
) -> None:
    monkeypatch.chdir(project_root)
    baseline = tmp_path / "baseline.json"
    main(
        [
            "evaluate",
            "--dataset",
            "datasets/golden.json",
            "--output",
            str(baseline),
            "--config",
            "config/evaluation.yaml",
        ]
    )
    assert baseline.exists()
    main(["gate", "--results", str(baseline), "--config", "config/quality-gates.yaml"])
    main(["compare", "--baseline", str(baseline), "--candidate", str(baseline)])
    output = capsys.readouterr().out
    assert '"decision": "pass"' in output
    assert '"compared_cases": 8' in output


def test_gate_command_exits_on_failure(
    monkeypatch: pytest.MonkeyPatch, project_root: Path, tmp_path: Path
) -> None:
    monkeypatch.chdir(project_root)
    result = tmp_path / "result.json"
    main(
        [
            "evaluate",
            "--dataset",
            "datasets/regressed-candidate.json",
            "--output",
            str(result),
            "--config",
            "config/evaluation.yaml",
        ]
    )
    with pytest.raises(SystemExit) as error:
        main(["gate", "--results", str(result), "--config", "config/quality-gates.yaml"])
    assert error.value.code == 1


def test_serve_calls_uvicorn(
    monkeypatch: pytest.MonkeyPatch, project_root: Path
) -> None:
    called: dict[str, object] = {}

    def fake_run(target: str, **kwargs: object) -> None:
        called.update({"target": target, **kwargs})

    monkeypatch.chdir(project_root)
    monkeypatch.setattr("llm_quality_harness.cli.uvicorn.run", fake_run)
    main(["serve", "--host", "0.0.0.0", "--port", "8123"])
    assert called["target"] == "llm_quality_harness.api:app"
    assert called["port"] == 8123
