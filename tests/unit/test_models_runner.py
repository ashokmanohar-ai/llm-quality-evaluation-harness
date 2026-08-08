import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from llm_quality_harness.config import Settings, load_yaml
from llm_quality_harness.models import EvaluationCase, Usage
from llm_quality_harness.runner import dataset_manifest, load_dataset


def test_usage_total_and_answer_contract() -> None:
    assert Usage(input_tokens=2, output_tokens=3).total_tokens == 5
    with pytest.raises(ValidationError, match="require reference_answer"):
        EvaluationCase(id="bad", prompt="p", response="r")


def test_settings_from_environment(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("LLMQ_PROJECT_ROOT", str(tmp_path))
    monkeypatch.setenv("LLMQ_PORT", "9001")
    settings = Settings.from_env()
    assert settings.project_root == tmp_path
    assert settings.port == 9001


def test_load_yaml_rejects_non_object(tmp_path: Path) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text("- not\n- an\n- object\n", encoding="utf-8")
    with pytest.raises(ValueError, match="must be an object"):
        load_yaml(path)


@pytest.mark.parametrize(
    "payload,message",
    [
        ([], "cases array"),
        ({"cases": []}, "at least one"),
        (
            {
                "cases": [
                    {"id": "same", "prompt": "p", "response": "r", "reference_answer": "r"},
                    {"id": "same", "prompt": "p", "response": "r", "reference_answer": "r"},
                ]
            },
            "unique",
        ),
    ],
)
def test_invalid_dataset_contracts(tmp_path: Path, payload: object, message: str) -> None:
    path = tmp_path / "dataset.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match=message):
        load_dataset(path)


def test_dataset_manifest(project_root: Path) -> None:
    manifest = dataset_manifest(project_root / "datasets/golden.json")
    assert manifest["case_count"] == 8
    assert "safety" in manifest["tags"]

