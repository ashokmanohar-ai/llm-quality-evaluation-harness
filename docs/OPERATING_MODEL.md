# Operating model and RACI

## Roles

- Business/Product Owner: accountable for purpose, value, user impact, and acceptable behavior.
- AI Quality Lead: owns strategy, dataset/evaluator portfolio, thresholds, evidence, and release-quality recommendation.
- AI/ML Engineering: owns model, prompt, retrieval, tool, and serving changes.
- Domain Expert: owns reference truth and ambiguity resolution.
- Security/Privacy/Risk: owns risk acceptance and required security/privacy controls.
- Platform/SRE: owns CI, environments, telemetry, reliability, deployment, and rollback.
- Release Approver: makes the accountable deployment decision for the assigned risk tier.

## RACI

| Activity | Product | AI Quality Lead | AI/ML Eng | Domain | Security/Risk | Platform | Release Approver |
|---|---|---|---|---|---|---|---|
| Define purpose and harm | A/R | C | C | C | C | I | I |
| Design evaluation strategy | C | A/R | C | C | C | I | I |
| Approve references/dataset | C | R | C | A/R | C | I | I |
| Build candidate system | C | C | A/R | C | C | C | I |
| Calibrate evaluators | I | A/R | C | R | C | I | I |
| Approve threshold change | A | R | C | C | A/R | I | I |
| Run CI and preserve evidence | I | A | C | I | I | R | I |
| Review safety/privacy | C | R | C | C | A/R | I | I |
| Release decision | C | R | C | C | C | C | A/R |
| Monitor and rollback | A | C | C | I | C | R | C |

R = Responsible, A = Accountable, C = Consulted, I = Informed. Organizations should adjust titles without collapsing incompatible duties for high-risk changes.

## Cadence and service levels

| Cadence/event | Review |
|---|---|
| Every change | Fast deterministic suite and changed-slice comparison |
| Nightly/scheduled | Broader provider and adversarial suites within budget |
| Before release | Full approved suite, baseline comparison, evidence review |
| Monthly | Drift, feedback, escaped defects, cost, flaky/uncertain cases |
| Quarterly or material change | Dataset/threshold calibration and risk review |
| Incident | Containment, rollback, evidence preservation, root cause, new regression case |

Suggested service metrics are release-gate escape rate, safety-case pass rate, evaluator/human agreement, dataset risk coverage, cost per successful evaluation, P95 evaluation duration, flaky/uncertain rate, mean time to diagnose, and exception ageing.

## Exception process

An exception records failed control, business need, affected scope, quantified risk, compensating controls, owner, approvers, monitoring, rollback trigger, and expiry. Critical privacy/security failures and missing evidence are not routine waiver candidates.

