from __future__ import annotations

import argparse
import json
from pathlib import Path

import uvicorn

from llm_quality_harness.config import Settings, load_evaluation_config, load_yaml
from llm_quality_harness.evaluator import Evaluator
from llm_quality_harness.gate import evaluate_gate
from llm_quality_harness.runner import read_result, run_dataset, write_result
from llm_quality_harness.statistics import compare_suites


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="llm-quality")
    subparsers = parser.add_subparsers(dest="command", required=True)

    evaluate = subparsers.add_parser("evaluate", help="Evaluate a versioned JSON dataset")
    evaluate.add_argument("--dataset", type=Path, required=True)
    evaluate.add_argument("--output", type=Path, required=True)
    evaluate.add_argument("--config", type=Path, default=Path("config/evaluation.yaml"))

    gate = subparsers.add_parser("gate", help="Apply release thresholds to a suite result")
    gate.add_argument("--results", type=Path, required=True)
    gate.add_argument("--config", type=Path, required=True)

    compare = subparsers.add_parser("compare", help="Compare candidate results with a baseline")
    compare.add_argument("--baseline", type=Path, required=True)
    compare.add_argument("--candidate", type=Path, required=True)
    compare.add_argument("--maximum-regression", type=float, default=0.03)

    serve = subparsers.add_parser("serve", help="Run the API and dashboard")
    serve.add_argument("--host", default=None)
    serve.add_argument("--port", type=int, default=None)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    if args.command == "evaluate":
        evaluation_config = load_evaluation_config(args.config)
        policy_path = Path("config/quality-gates.yaml")
        policy_version = str(load_yaml(policy_path).get("version", "unknown"))
        result = run_dataset(args.dataset, Evaluator(evaluation_config), policy_version)
        write_result(result, args.output)
        print(json.dumps(result.summary.model_dump(), indent=2))
        return
    if args.command == "gate":
        report = evaluate_gate(read_result(args.results), load_yaml(args.config))
        print(report.model_dump_json(indent=2))
        if report.decision == "fail":
            raise SystemExit(1)
        return
    if args.command == "compare":
        comparison = compare_suites(
            read_result(args.baseline),
            read_result(args.candidate),
            regression_threshold=args.maximum_regression,
        )
        print(comparison.model_dump_json(indent=2))
        return
    settings = Settings.from_env()
    uvicorn.run(
        "llm_quality_harness.api:app",
        host=args.host or settings.host,
        port=args.port or settings.port,
    )


if __name__ == "__main__":
    main()

