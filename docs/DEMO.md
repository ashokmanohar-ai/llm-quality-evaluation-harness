# Demo guide

## Eight-minute leadership and engineering walkthrough

1. Problem (45 sec): AI changes require evidence across quality, RAG grounding, safety, structure, latency, and cost—not only deterministic assertions.
2. Architecture (60 sec): show the provider-neutral adapter, evaluator, hard controls, suite aggregation, evidence store, and policy gate.
3. Dataset (60 sec): open `datasets/golden.json`; point out stable IDs, references, contexts, expected facts, usage, and refusal cases.
4. Dashboard (90 sec): start the app, select **Run reference suite**, review scorecards and case evidence.
5. CI gate (60 sec): show `config/quality-gates.yaml` and explain why safety and schema cannot be averaged away.
6. Regression (90 sec): evaluate the intentionally degraded dataset and compare it with the baseline; show regressed IDs and uncertainty.
7. Leadership controls (90 sec): show governance, responsible-AI, threat model, RACI, and roadmap.
8. Close (45 sec): explain that the MVP proves architecture and mechanics; the next step is calibrating one real bounded use case.

## Commands

```bash
python -m pip install -e ".[dev]"
make quality
python -m llm_quality_harness.cli serve
```

Regression demonstration:

```bash
python -m llm_quality_harness.cli evaluate --dataset datasets/golden.json --output reports/baseline.json
python -m llm_quality_harness.cli evaluate --dataset datasets/regressed-candidate.json --output reports/candidate.json
python -m llm_quality_harness.cli compare --baseline reports/baseline.json --candidate reports/candidate.json
```

## Talking points

- Offline deterministic execution makes CI reliable and portfolio reviewers successful without credentials.
- Real model providers are adapters; governance and evaluation evidence do not depend on one vendor.
- A score is insufficient: case evidence, hard controls, slices, uncertainty, ownership, and approval form the release decision.
- The deliberately failing dataset makes regression behavior visible instead of showing only a happy path.

