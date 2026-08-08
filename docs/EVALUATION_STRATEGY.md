# Evaluation strategy

## Decision objective

The evaluation program answers one operational question: is the candidate AI behavior sufficiently useful, safe, reliable, and economical for its approved purpose and risk tier? A score is evidence for that decision, not the decision by itself.

## Quality taxonomy

| Dimension | Example measures | Decision use |
|---|---|---|
| Task quality | Correctness, relevance, completeness, instruction adherence | User-value threshold |
| RAG quality | Retrieval recall/precision, groundedness, citation validity | Hallucination and provenance control |
| Safety/privacy | Refusal, jailbreak resistance, toxicity, PII leakage | Hard release constraints |
| Structure/tools | JSON/schema compliance, tool selection, arguments, side effects | Automation reliability and action safety |
| Reliability | Consistency, flakiness, timeout/error rate | Production-operability threshold |
| Efficiency | Latency distribution, tokens, cost per successful task | SLA and unit-economics threshold |
| Fairness | Slice-specific quality and harmful disparity | Responsible deployment decision |

## Dataset lifecycle

1. Translate approved use cases, failure modes, and risk assessment into coverage categories.
2. Create representative positive, negative, boundary, adversarial, multilingual, and demographic slices where applicable.
3. Use synthetic or licensed inputs; remove unnecessary personal data.
4. Require domain-expert review of prompts, references, expected facts, and refusal behavior.
5. Assign stable IDs, owners, risk tags, source/provenance, and semantic versions.
6. Separate development, calibration, regression, red-team, and holdout sets.
7. Review drift, escaped defects, user feedback, and production incidents on a fixed cadence.

Changing a reference answer is a governed product/risk decision, not routine test maintenance.

## Evaluator portfolio

Use the simplest evaluator that reliably measures the property:

- deterministic assertions for schema, citations, forbidden content, tool calls, latency, and cost;
- lexical or embedding similarity for bounded content comparisons;
- task-specific programmatic checks for calculations and workflows;
- calibrated model-as-judge rubrics for semantic properties;
- human/domain review for ambiguity, high impact, fairness, and judge calibration.

Never use the same uncalibrated judge as the only arbiter of its own output. Judge prompts, models, sampling, rubrics, and label agreement must be versioned. Track inter-rater agreement, false-pass/false-fail rates, and disagreement escalation.

## Threshold policy

Thresholds derive from user harm, business impact, baseline behavior, and acceptable uncertainty. The MVP separates weighted score configuration from release policy. Safety-case and schema compliance are hard gates; latency and cost are maximum gates. Production policies should vary by use case and risk tier, require named owners, and record approval and expiry dates.

## Regression method

Compare candidate and baseline on identical stable case IDs. Report mean and metric deltas, per-case regressions, and uncertainty. Segment results by risk, language, scenario, tenant, model, and other relevant slices. Do not approve a candidate using aggregate improvement when a critical slice regresses.

The MVP uses a paired normal 95% confidence interval for illustration. Larger programs should select appropriate bootstrap, permutation, proportion, or sequential methods with statistical review and multiple-comparison controls.

## Release evidence checklist

- use case, users, environment, model/prompt/index/tool versions;
- dataset version, provenance, coverage, and known gaps;
- evaluator versions and calibration evidence;
- aggregate and slice results with confidence/uncertainty;
- safety, privacy, fairness, latency, cost, and reliability findings;
- candidate-versus-baseline comparison;
- failures, waivers, owners, expiry, and rollback trigger;
- accountable product, quality, security/risk, and business approvals.

