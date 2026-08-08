# Responsible AI controls

## Purpose

Responsible AI is treated as measurable product and operational quality, not a one-time checklist. Controls are selected according to the use case, affected people, data, decision impact, and failure recoverability.

| Principle | Engineering control | Evidence |
|---|---|---|
| Valid and reliable | Representative datasets, calibrated metrics, regression/slice tests | Versioned results and uncertainty |
| Safe and secure | Red-team packs, refusal tests, injection/leakage checks, tool allowlists | Safety findings and incident drills |
| Fair | Harm analysis and quality comparison across relevant cohorts | Slice metrics and expert review |
| Private | Data minimization, synthetic data, redaction, retention/deletion | Data inventory and privacy assessment |
| Transparent | Source citations, limitations, user disclosures, decision records | UX review and model/system cards |
| Accountable | Named owners, approval gates, exceptions, monitoring, rollback | RACI and audit history |

## Harm-based test design

Begin with people and outcomes: who could be harmed, how severe/reversible the harm is, what misuse is plausible, and which safeguards detect or prevent it. Convert each material risk into prevention controls, evaluation cases, monitoring signals, response ownership, and rollback triggers.

## Human oversight

Human review must be meaningful: the reviewer receives understandable evidence, has authority and time to reject, can see uncertainty and limitations, and is not encouraged to rubber-stamp automation. High-impact decisions require appropriate subject-matter and risk expertise.

## Known MVP gaps

The synthetic reference set does not establish fairness, multilingual quality, domain validity, accessibility, legal sufficiency, or real-world safety. Those require use-case-specific data, affected-stakeholder input, domain review, production monitoring, and organization-approved governance.

