from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

DEFAULT_WEIGHTS = {
    "correctness": 0.25,
    "groundedness": 0.20,
    "relevance": 0.15,
    "completeness": 0.20,
    "citation_validity": 0.10,
    "safety": 0.10,
}


@dataclass(frozen=True)
class Settings:
    project_root: Path
    evaluation_config: Path
    gate_config: Path
    dataset: Path
    store_path: Path
    host: str
    port: int

    @classmethod
    def from_env(cls) -> Settings:
        root = Path(os.getenv("LLMQ_PROJECT_ROOT", Path.cwd())).resolve()
        return cls(
            project_root=root,
            evaluation_config=root / "config/evaluation.yaml",
            gate_config=root / os.getenv("LLMQ_GATE_CONFIG", "config/quality-gates.yaml"),
            dataset=root / os.getenv("LLMQ_DATASET", "datasets/golden.json"),
            store_path=root / os.getenv("LLMQ_STORE_PATH", "reports/results.db"),
            host=os.getenv("LLMQ_HOST", "127.0.0.1"),
            port=int(os.getenv("LLMQ_PORT", "8000")),
        )


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"configuration must be an object: {path}")
    return payload


def load_evaluation_config(path: Path) -> dict[str, Any]:
    config = load_yaml(path)
    weights = config.get("weights", DEFAULT_WEIGHTS)
    if not isinstance(weights, dict) or not weights:
        raise ValueError("evaluation weights must be a non-empty mapping")
    if abs(sum(float(value) for value in weights.values()) - 1.0) > 0.0001:
        raise ValueError("evaluation weights must sum to 1.0")
    config["weights"] = {str(key): float(value) for key, value in weights.items()}
    return config

