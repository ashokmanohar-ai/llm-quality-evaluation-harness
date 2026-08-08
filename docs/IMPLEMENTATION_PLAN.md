# Detailed implementation plan

## MVP delivery status

| Workstream | MVP outcome | Status |
|---|---|---|
| Contracts | Typed cases, contexts, usage, metrics, findings, suites, gates, comparisons | Complete |
| Evaluation | Six explainable metrics, refusal validation, schema hard control | Complete |
| Execution | Dataset replay and callable provider contracts; CLI/API suite execution | Complete |
| Regression | Paired case/metric deltas and 95% interval | Complete |
| Evidence | JSON reports, SQLite store, dashboard, API retrieval | Complete |
| Automation | Ruff, pytest/coverage, Playwright UI/API, secret scan, Actions | Complete |
| Operations | Docker, Compose, Make targets, security and contribution guidance | Complete |
| Leadership | Architecture, strategy, governance, RAI, threat model, RACI, roadmap | Complete |

## Production implementation backlog

### Phase 1 — calibrate the use case

Inputs: approved business purpose, personas, risks, source data, production baseline, and human labels.

Build domain datasets and slices; add task-specific metrics; calibrate deterministic and semantic evaluators; define risk-tiered gates and exception rules. Exit when coverage and judge/human agreement meet approved targets and owners sign the evaluation plan.

### Phase 2 — connect providers and delivery

Implement approved provider/gateway adapters, resilient concurrency, rate limits, retries, budgets, telemetry, and CI environment controls. Add prompt/model/index/tool provenance. Exit when reproducible evaluation runs meet SLA/cost limits and secrets/data controls pass review.

### Phase 3 — govern evidence and release

Add SSO/RBAC, tenant/project isolation, managed storage, retention, immutable audit, workflow approvals, signed exceptions, dashboards, alerts, and release-system integration. Exit when release and rollback drills preserve verifiable evidence and duty separation.

### Phase 4 — scale and learn

Add asynchronous distributed workers, experiment-system integration, production feedback/drift sampling, red-team packs, fairness/multilingual slices, evaluator monitoring, and portfolio analytics. Exit when scale tests, operational SLOs, incident response, and periodic calibration are demonstrated.

## Engineering work packages

1. Provider contract: response, model/prompt versions, usage, tool/retrieval traces, redaction, timeout/retry semantics.
2. Metric plug-ins: typed input/output, applicability, calibration metadata, confidence, cost, deterministic failure behavior.
3. Dataset registry: provenance, access class, schema/version, owners, slices, hashes, review/expiry.
4. Evaluation orchestrator: queues, idempotency, cancellation, budgets, partial/blocked outcomes, artifact links.
5. Policy service: risk-tier thresholds, protected changes, approval/exception workflow, expiry.
6. Evidence platform: immutable run metadata, encrypted artifacts, retention/deletion, query and export.
7. Observability: OpenTelemetry spans, quality/cost/SLA dashboards, drift and incident alerts.
8. Adoption: templates, examples, onboarding, support, pilot scorecard, maturity assessment.

## Definition of done

The product is not production-ready solely because the MVP gates pass. Production done requires use-case data, calibrated metrics, enterprise identity/security/privacy controls, deployment integration, monitoring, rollback, incident response, evidence retention, and accountable sign-off.

