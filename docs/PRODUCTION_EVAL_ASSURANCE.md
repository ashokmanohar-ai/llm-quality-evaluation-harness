# Production Evaluation & Agent Assurance

This document defines the next production layer for the evaluation harness.

## Objective

Move from deterministic offline evaluation into a governed production architecture that supports semantic evaluators, agent trajectory evidence, observability, regression control and release decisions without hiding deterministic checks behind an LLM judge.

## Target architecture

```text
Golden datasets
    -> Provider / agent adapter
    -> Deterministic evaluators
    -> Optional semantic evaluators (Ragas / DeepEval)
    -> Agent trajectory evaluator
    -> Regression comparison
    -> Quality gates
    -> Evidence store
    -> CI/CD decision
    -> Human release authority
```

## Engineering principles

1. Deterministic checks remain deterministic and separately inspectable.
2. Semantic judges are calibrated against human labels before they influence release decisions.
3. Dataset, prompt, model, evaluator and threshold versions are retained with each run.
4. Safety and policy blockers cannot be averaged away by a high aggregate score.
5. Agent quality is evaluated at trajectory level: completion, tool choice, retries, recovery and efficiency.
6. Production traces can be promoted into regression assets after incidents or reviewer findings.
7. Release authority remains accountable and human for consequential decisions.

## Optional integration layer

The harness now exposes optional integration discovery for:

- `ragas` — RAG semantic evaluation
- `deepeval` — LLM and agent evaluation
- `langgraph` — agent workflow orchestration
- `opentelemetry` — traces and production observability

These are intentionally not mandatory runtime dependencies. The baseline harness remains offline and deterministic. Teams can add integrations without changing the core evidence and gate model.

## Agent trajectory evidence

The deterministic trajectory evaluator scores:

- task completion — 40%
- correct tool selection — 25%
- trajectory efficiency — 20%
- recovery success — 15%

The weighting is explicit so teams can version and review it. A semantic trajectory judge can later complement this score but should not replace tool-call and execution evidence.

## Recommended next implementation slices

### Slice 1 — Ragas adapter
Map harness cases into Ragas datasets and normalize returned metrics into the common 0..1 metric contract. Preserve Ragas version, embedding/model identity and evaluator configuration in evidence.

### Slice 2 — DeepEval adapter
Add groundedness, hallucination, task-completion and custom policy metrics. Store judge prompt/rubric version and calibration metadata alongside each semantic result.

### Slice 3 — LangGraph trace adapter
Capture nodes, edges, tools, arguments, retries, errors and final task completion from a LangGraph execution and convert them into `AgentStep` trajectory evidence.

### Slice 4 — OpenTelemetry
Emit one trace per evaluation run with spans for provider execution, retrieval, tool calls, evaluators, gate calculation and evidence persistence. Do not place sensitive prompt or PII content in telemetry by default.

### Slice 5 — CI quality gate
Run deterministic evaluation on every pull request. Run semantic suites on controlled branches or scheduled workflows when model credentials are available. Candidate releases should be blocked when mandatory policy thresholds fail.

## UK interview evidence

This architecture demonstrates the engineering concerns commonly expected in senior AI quality, evaluation, assurance and agentic AI roles:

- versioned golden datasets
- reproducible evaluation
- RAG quality
- agent trajectory quality
- regression analysis
- LLM-as-Judge governance
- safety and policy gates
- FastAPI and CI/CD integration
- observability-ready design
- accountable human release decisions

The key interview message is not that every metric requires an LLM. The stronger engineering story is that deterministic, statistical, semantic and human evidence are combined according to explicit policy and retained for auditability.
