# Threat model

## Assets and trust boundaries

Assets include model/provider credentials, prompts and policies, proprietary retrieval content, evaluation datasets and references, candidate responses, tool-call evidence, quality thresholds, approval records, and release decisions. Trust boundaries exist at clients, provider gateways, retrieval systems, third-party evaluators, the evidence store, CI runners, dashboards, and human review.

## Priority threats and controls

| Threat | Example impact | MVP control | Enterprise control |
|---|---|---|---|
| Prompt injection | Policy bypass or data exfiltration | Pattern case and refusal gate | Content isolation, instruction hierarchy, allowlisted tools, red-team service |
| Sensitive-data leakage | Privacy/security incident | PII pattern with redacted evidence | DLP, encryption, minimization, access/retention policy |
| Poisoned evaluation data | Artificial pass/fail result | Versioned data and code review | Provenance, signed artifacts, separation of duties |
| Threshold tampering | Unsafe release passes | Policy in source control/CODEOWNERS | Protected branches, signed approval, policy service |
| Judge manipulation | Inflated semantic score | Deterministic reference path | Independent calibrated judges and adversarial judge tests |
| Cross-tenant leakage | Confidentiality breach | Out of scope and documented | Tenant keys, row/object policy, retrieval namespace isolation |
| Tool misuse | Consequential side effect | No live tools in baseline | Least privilege, allowlists, dry runs, human approval, idempotency |
| Evidence spoofing | False assurance | CI-generated structured evidence | Attestation, immutable storage, run identity and provenance |
| Cost/denial attack | Budget exhaustion | Offline CI and explicit usage | Quotas, timeouts, concurrency/token/cost budgets, circuit breakers |
| Dependency compromise | Code execution or theft | Pinned runtime ranges and least CI permissions | Lockfiles, SBOM, signed provenance, scanning and patch SLA |

## Abuse cases

- A retrieved document tells the model to ignore policy and call a privileged tool.
- A contributor weakens safety thresholds and edits golden answers in the same change.
- An evaluator receives hidden personal data and persists it indefinitely.
- A compromised provider returns a plausible answer plus fabricated usage/cost metadata.
- A dashboard user queries another tenant's evaluation evidence.

## Stop conditions

Stop evaluation or release on unexpected credential/data exposure, unapproved external transfer, critical safety finding, missing provenance, policy-version mismatch, evidence-store integrity failure, uncontrolled tool action, or inability to reproduce the decision. Escalate to the named security/risk and product owners; preserve only approved redacted evidence.

## Residual risk

Pattern checks are incomplete and bypassable. Lexical metrics can reward wording overlap without truth. SQLite has no enterprise identity or immutable audit guarantee. The MVP must not process confidential data or authorize production decisions without the target controls above.

