# Adoption roadmap

| Phase | Outcome | Key deliverables | Measurable exit criteria |
|---|---|---|---|
| 1. Reference MVP | Reproducible offline quality gate | Current repository, synthetic suite, CI evidence | Deterministic pipeline passes; limitations documented |
| 2. Pilot | Calibrated evaluation for one bounded use case | Domain data, provider adapter, semantic/task metrics, baseline | Approved risk coverage; target judge/human agreement; SLA/cost met |
| 3. Governed platform | Controlled enterprise release decisions | SSO/RBAC, isolation, approvals, immutable evidence, monitoring | Audit/rollback drill succeeds; zero unowned exceptions |
| 4. Scale | Reusable service across teams/models | Async workers, registry, templates, portfolio dashboards | SLO met at forecast volume; reuse/adoption and cost targets met |
| 5. Continuous assurance | Production feedback improves evaluation | Drift sampling, incident-to-test loop, periodic recalibration | Escaped-defect and detection-time trends improve |

## Prioritized capabilities

Near term: OpenAI/Azure/Anthropic/local adapter examples behind interfaces; embedding and rubric metrics; retrieval precision/recall; prompt/model/index registry; richer HTML/JSON/JUnit reporting; dataset slices and coverage matrix.

Medium term: model-judge calibration workbench; human-review queues; red-team packs; tool/agent trajectory evaluation; OpenTelemetry and experiment-platform integration; protected threshold workflow; SSO/RBAC and managed persistence.

Long term: distributed evaluation, continuous production sampling, drift alerts, portfolio risk dashboards, fairness/multilingual programs, signed evidence/attestations, and automated rollback recommendations with human authority.

## Pilot selection

Choose a high-value but bounded internal or QA/UAT use case with accessible domain experts, reversible outcomes, synthetic test data, measurable baseline, and no autonomous high-impact action. Avoid making the first pilot a regulated or irreversible production decision.

