from __future__ import annotations

import argparse
from pathlib import Path

from llm_quality_harness.runner import dataset_manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", type=Path)
    args = parser.parse_args()
    manifest = dataset_manifest(args.dataset)
    print(
        f"VALID: {manifest['suite_id']} version={manifest['version']} "
        f"cases={manifest['case_count']} tags={','.join(manifest['tags'])}"
    )


if __name__ == "__main__":
    main()

