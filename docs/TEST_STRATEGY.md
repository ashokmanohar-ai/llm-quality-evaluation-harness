# Test strategy

## Objectives

Prove that evaluation math, safety/schema hard controls, aggregation, persistence, API behavior, dashboard evidence, and CI release decisions are deterministic and auditable. Tests cover both the harness and the reference AI behavior; these are separate assurance targets.

## Test layers

| Layer | Scope | Evidence |
|---|---|---|
| Unit | Tokenization, metrics, safety, schema, config, adapters | pytest result and coverage |
| Integration | Dataset-to-suite flow, gate, statistics, SQLite | pytest result and structured objects |
| API | Health, security headers, evaluation, storage, not-found behavior | FastAPI TestClient results |
| AI behavior | RAG, structure, governance, observability, injection, privacy | `reports/evaluation.json` |
| Browser/API E2E | Dashboard run and service endpoints | Playwright HTML, JUnit, trace/media on failure |
| Static/security | Ruff, dataset contract, repository secret patterns | CI logs |

## Coverage model

The reference dataset includes positive answers, RAG grounding/citations, structured output, quality/release rules, agent governance, observability/cost, prompt injection, and sensitive-data refusal. Production suites must additionally cover domain tasks, alternate and boundary behavior, multilingual/accessibility needs, fairness slices, provider failures, retrieval failures, tool failures, concurrency, drift, and realistic latency/cost distributions.

## Determinism and isolation

The default provider replays recorded synthetic responses. Tests do not call an LLM, external endpoint, or live tool. Temporary databases isolate API/store tests. Stable case IDs enable paired comparison. Playwright uses bounded retries only in CI and retains every retry as visible evidence.

## Failure classification

Classify failures as candidate behavior, evaluator/automation defect, dataset/reference defect, policy/gate failure, environment/dependency failure, data/access failure, or AI uncertainty. Never transform a blocked or failed run into a pass. Quarantine requires owner, evidence, scope, expiry, and visible reporting.

## Entry and exit criteria

Entry: approved scope, valid versioned dataset, synthetic/approved data, evaluator/policy versions, available runtime, and no unresolved critical security/data issue.

Exit: lint and deterministic tests pass; coverage is at least 85%; reference suite and hard gates pass; E2E evidence is available in a supported browser environment; no secrets are detected; limitations and residual risks are recorded; accountable review occurs for release use.

