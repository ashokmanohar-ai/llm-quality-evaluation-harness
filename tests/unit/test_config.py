from pathlib import Path

import pytest

from llm_quality_harness.config import load_evaluation_config


def test_rejects_invalid_weights(tmp_path: Path) -> None:
    config = tmp_path / "evaluation.yaml"
    config.write_text("weights:\n  correctness: 0.5\n", encoding="utf-8")
    with pytest.raises(ValueError, match="sum to 1.0"):
        load_evaluation_config(config)

