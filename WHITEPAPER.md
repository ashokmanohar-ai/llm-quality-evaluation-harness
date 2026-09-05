# LLM Evaluation for Quality Engineers

## From Functional Testing to AI Quality Metrics

**Technical White Paper — Version 1.0**  
**September 2026**

**Author:** Ashok Kumar Manohar  
**GitHub:** [ashokmanohar-ai](https://github.com/ashokmanohar-ai)  
**Reference implementation:** [LLM Quality Evaluation Harness](https://github.com/ashokmanohar-ai/llm-quality-evaluation-harness)

> **Publication note:** This is an independent technical white paper supported by an open-source reference implementation. It is not a peer-reviewed academic publication, legal opinion, security certification, compliance certification, or statement of production readiness.

---

## Abstract

Large language model applications change the meaning of software quality. Traditional functional testing assumes that a known input can usually be mapped to a deterministic expected output. LLM systems are probabilistic: valid answers may differ in wording, quality may vary across repeated runs, a response may be fluent but unsupported, and a release can regress in safety, grounding, latency, cost, or structured-output compliance without producing a conventional test failure.

This white paper presents a practical **LLM Evaluation framework for Quality Engineers**. It explains how software testing disciplines can evolve from pass/fail assertions toward evidence-driven evaluation of correctness, relevance, completeness, groundedness, citation integrity, safety, privacy, refusal behavior, structured output, robustness, latency, token consumption, cost, stability, and regression risk.

The framework advocates four principles. First, evaluate systems against **versioned, representative datasets** rather than ad hoc prompts. Second, prefer **deterministic measurements** when an outcome can be proven from structured evidence. Third, use model-based judges only for dimensions that genuinely require semantic judgment, and calibrate them against human labels. Fourth, convert evaluation results into **explicit release policies and CI/CD quality gates** so AI quality becomes an engineering control rather than a dashboard observed after deployment.

A companion open-source reference implementation demonstrates versioned golden datasets, provider-neutral adapters, deterministic metrics, hard safety and schema controls, candidate-versus-baseline comparison, confidence intervals, API/CLI workflows, retained JSON evidence, Docker, Playwright validation, GitHub Actions quality gates, and governance artifacts.

The central proposition is:

> **LLM quality should be treated as measurable software behavior: define expected outcomes, collect evidence, evaluate multiple dimensions, gate critical risks, compare every change against a baseline, and retain enough context to explain why a release passed or failed.**

---

## 1. Executive Summary

LLM-powered applications are now embedded in search, knowledge assistants, customer support, software engineering, document processing, analytics, test design, decision support, and agentic workflows. Their quality cannot be established by checking whether several hand-picked responses look good.

A production-oriented evaluation program must answer questions such as:

- Is the answer factually correct for the task?
- Does it include the facts the user actually needs?
- Is it grounded in supplied or retrieved evidence?
- Are citations real and traceable?
- Does it refuse requests that should be refused?
- Does it leak sensitive information?
- Does it follow the required JSON, schema, or tool contract?
- Does it remain robust under prompt injection or adversarial inputs?
- How often does the same request produce materially different quality?
- Did a new model, prompt, retrieval strategy, or configuration improve quality or only move cost and latency?
- Can a release be blocked automatically when a critical property regresses?

Quality Engineering provides the operating discipline needed to answer those questions consistently. The core shift is from **example-based demonstration** to **dataset-based evaluation and regression control**.

This paper proposes the following lifecycle:

```text
Quality Requirements
      ↓
Versioned Evaluation Dataset
      ↓
Model / Application Execution
      ↓
Deterministic + Semantic Evaluators
      ↓
Case-Level Evidence
      ↓
Suite Metrics + Safety Findings
      ↓
Candidate vs Baseline Comparison
      ↓
Policy / Quality Gate
      ↓
Release Decision + Retained Evidence
```

The framework does not assume a particular LLM vendor. Evaluation should remain stable even when the underlying model, deployment, prompt, RAG layer, application framework, or gateway changes.

---

## 2. Why Traditional Functional Testing Is Not Enough

Traditional testing is excellent at deterministic contracts:

```text
Input → Processing → Expected Output
```

Examples include HTTP status codes, database state, UI transitions, arithmetic, role permissions, file creation, and schema validation.

LLM behavior adds uncertainty:

```text
Prompt + Context + Model + Sampling + Policy + Retrieval + History
                         ↓
                 Probabilistic Output
```

Two outputs can differ lexically while both are acceptable. Conversely, a polished answer can be wrong, incomplete, unsupported, unsafe, or structurally invalid.

Therefore, an assertion such as:

```python
assert actual == expected
```

is often too strict for semantics and too weak for risk. LLM evaluation needs multiple dimensions and multiple evidence sources.

The right question is not only **“Did the output match?”** but **“Did the system satisfy the quality contract for this task?”**

---

## 3. The LLM Quality Surface

A practical evaluation strategy should separate quality into distinct surfaces.

| Quality surface | Example question | Typical evidence |
|---|---|---|
| Correctness | Is the answer true for the expected task? | Reference facts, domain checks, human labels |
| Relevance | Did the response address the actual request? | Prompt-to-response comparison |
| Completeness | Were all required facts/actions included? | Required-fact coverage |
| Groundedness | Are claims supported by supplied evidence? | Context-to-claim mapping |
| Citation integrity | Do cited sources exist and support the claim? | Source IDs and context chunks |
| Safety | Did the system avoid prohibited behavior? | Red-team cases, refusal expectations |
| Privacy | Did the response expose protected data? | PII/secret detectors, case policy |
| Structure | Did the output satisfy the required contract? | JSON Schema/Pydantic validation |
| Robustness | Does quality survive adversarial phrasing? | Perturbation and attack datasets |
| Stability | Does behavior remain acceptable across repeated runs? | Distribution across runs |
| Performance | Is latency within an acceptable service envelope? | P50/P95/P99 timings |
| Efficiency | Are token and tool costs controlled? | Usage and cost metadata |
| Regression | Did the candidate degrade relative to baseline? | Paired case comparison |

A single aggregate score must never hide critical failures. A system with a 95% average score can still be unreleasable if one case leaks confidential data or performs an unauthorized action.

---

## 4. Quality Requirements Before Metrics

Teams often begin by selecting tools or metrics. The better starting point is to define what good behavior means for the product.

For each LLM feature, document:

1. **User goal** — what outcome the user is trying to achieve.
2. **Required behavior** — facts, actions, structure, tone, or workflow expectations.
3. **Forbidden behavior** — unsafe content, unsupported claims, data leakage, unauthorized actions.
4. **Evidence requirement** — whether claims must be grounded or cited.
5. **Operational bounds** — latency, token, and cost limits.
6. **Failure behavior** — refuse, ask a clarifying question, abstain, escalate, or return a safe error.
7. **Risk class** — informational, decision-support, write-action, or high-impact.

Metrics should be selected only after these quality requirements exist.

---

## 5. Build a Versioned Evaluation Dataset

A reliable LLM evaluation program starts with a stable dataset. The dataset is the AI equivalent of a regression test suite.

Each case should have a durable identifier and enough metadata to explain why it exists.

Example:

```json
{
  "id": "POLICY-017",
  "prompt": "What approval is required before releasing this AI feature?",
  "reference_answer": "A designated human approver must review the release evidence.",
  "expected_facts": ["human approval", "release evidence"],
  "contexts": [
    {"id": "POL-01", "text": "AI releases require human approval based on retained evaluation evidence."}
  ],
  "expected_behavior": "answer",
  "tags": ["governance", "grounding", "release"]
}
```

A mature dataset should include:

- happy-path tasks;
- negative and refusal cases;
- ambiguous prompts;
- long-context cases;
- adversarial cases;
- domain edge cases;
- outdated or conflicting context;
- privacy-sensitive inputs;
- structured-output cases;
- multilingual cases where relevant;
- known historical incidents;
- high-business-impact scenarios.

Datasets should be version-controlled with the application. Changes to the dataset need review because changing the test set can change the apparent quality of the system.

---

## 6. Dataset Coverage Matters More Than Dataset Size

A thousand duplicated easy prompts do not create a strong evaluation suite.

Coverage should be measured across dimensions such as:

- business journey;
- user persona;
- product capability;
- risk level;
- prompt pattern;
- language;
- knowledge domain;
- safety category;
- expected behavior;
- structured-output contract;
- integration or tool path;
- model context length;
- known defect category.

A practical coverage matrix may look like:

| Area | Low risk | Medium risk | High risk | Adversarial |
|---|---:|---:|---:|---:|
| Knowledge Q&A | ✓ | ✓ | ✓ | ✓ |
| Summarization | ✓ | ✓ |  | ✓ |
| Recommendations | ✓ | ✓ | ✓ | ✓ |
| Sensitive data |  | ✓ | ✓ | ✓ |
| Structured extraction | ✓ | ✓ | ✓ | ✓ |

The objective is not maximum case count. It is sufficient evidence for the risk and use case.

---

## 7. Deterministic-First Evaluation

When a property can be proven exactly, use deterministic evaluation.

Examples:

- Was the JSON valid?
- Was a required field present?
- Did a citation ID exist?
- Did the response contain a forbidden secret pattern?
- Did the application call an unauthorized tool?
- Did the request exceed a latency threshold?
- Did token use increase beyond the agreed budget?

These should not be delegated to an LLM judge.

Deterministic checks are:

- reproducible;
- inexpensive;
- explainable;
- easy to regression-test;
- suitable for hard release gates.

The companion implementation follows this pattern by keeping schema and safety controls separate from weighted semantic quality.

---

## 8. Correctness Evaluation

Correctness is task-dependent. There is no universal LLM correctness metric.

Possible strategies include:

- exact normalized matching for identifiers and codes;
- required-fact coverage;
- numeric tolerance checks;
- database or API truth checks;
- reference-answer token overlap;
- embedding similarity;
- domain-specific rules;
- expert human labels;
- calibrated model judges.

A crucial distinction is between **semantic similarity** and **truth**. Two answers can be semantically similar while both are wrong. For high-value facts, compare against an authoritative source or deterministic system when possible.

---

## 9. Relevance Evaluation

A correct statement can still be a poor answer if it does not address the user's need.

Relevance asks whether the response:

- answers the requested question;
- avoids unrelated material;
- follows the requested scope;
- respects requested length or format;
- does not bury the answer under unnecessary content.

Relevance is often partly semantic, making it a reasonable candidate for a calibrated judge. However, basic deterministic signals such as required sections, expected fields, or keyword families may still be useful.

---

## 10. Completeness and Required-Fact Coverage

Completeness is one of the most practical Quality Engineering metrics.

If a test case expects five required facts and the output includes four, fact coverage is:

\[
Completeness = \frac{4}{5} = 0.80
\]

This is more actionable than a generic “good answer” score because the report can show exactly which fact is missing.

Required-fact evaluation works particularly well for:

- policy Q&A;
- product support;
- regulated disclosures;
- technical procedures;
- test-case generation;
- data extraction;
- onboarding instructions.

---

## 11. Groundedness

Groundedness measures whether claims are supported by the evidence available to the model.

For RAG and enterprise knowledge applications, an answer can be relevant and plausible but still contain unsupported claims.

A groundedness evaluator should distinguish:

```text
Claim supported by supplied evidence      → supported
Claim contradicted by supplied evidence   → contradicted
Claim absent from supplied evidence       → unsupported
```

Where the product requires evidence-bound answers, unsupported claims should be surfaced explicitly rather than hidden inside an overall quality score.

---

## 12. Citation Integrity

Citations create the appearance of trust, so they deserve independent testing.

Validate at least:

1. **Existence** — does the citation point to a real source?
2. **Authorization** — was the source permitted for this user?
3. **Relevance** — does the cited source relate to the claim?
4. **Entailment/support** — does the source actually support the claim?
5. **Freshness** — is the cited version current for the question?

A made-up citation is not a formatting defect. It is an evidence-integrity failure.

---

## 13. Safety Evaluation

Safety testing should be represented as explicit cases and policies, not as an informal red-team exercise performed before launch.

Examples include:

- prompt injection;
- system prompt disclosure;
- sensitive-data extraction;
- policy bypass attempts;
- malicious code generation where prohibited;
- improper refusals;
- unsafe tool instructions;
- secrets or credential leakage;
- cross-user data exposure.

The **OWASP GenAI LLM Top 10 2026** provides current community guidance on major security risks affecting LLM applications. Security evaluation should map relevant threats to reproducible test cases and controls rather than treating the OWASP list as a compliance checklist.

Critical safety failures should normally be **hard blockers**.

---

## 14. Refusal Quality

A refusal test has two failure modes:

- the system should refuse but answers;
- the system should answer but refuses.

Therefore refusal evaluation should measure both **safety correctness** and **over-refusal**.

A high refusal rate is not automatically safer. It may make the product unusable.

Useful refusal test categories include:

```text
Clearly allowed
Clearly disallowed
Ambiguous / dual-use
Allowed with constraints
Sensitive but legitimate
```

The ideal policy behavior should be defined before execution.

---

## 15. Privacy and Data Leakage

LLM applications can expose information through prompts, retrieved context, model output, logs, traces, or tools.

Quality Engineering should test:

- PII in output;
- secrets and access tokens;
- data from another tenant/user;
- hidden system instructions;
- confidential document fragments;
- excessive logging of prompts or retrieved content.

Detectors should be combined with policy-aware cases. A phone number in a response is not always a privacy defect; the defect depends on authorization and context.

---

## 16. Structured Output as a Hard Contract

Many production LLM features do not produce prose. They produce JSON, function parameters, SQL fragments, workflow objects, test cases, or API payloads.

If downstream software expects:

```json
{
  "priority": "HIGH",
  "reason": "...",
  "test_ids": ["TC-101", "TC-102"]
}
```

then schema validity is a software contract.

Validate:

- JSON syntax;
- required fields;
- enum values;
- types;
- bounds;
- identifier patterns;
- forbidden extra fields;
- semantic cross-field constraints.

A response that “looks right” but fails its schema should fail the case.

---

## 17. LLM-as-a-Judge

Model-based judges are useful when the quality dimension is genuinely semantic, such as:

- clarity;
- relevance;
- style adherence;
- nuanced completeness;
- reasoning quality where observable;
- semantic groundedness.

But judges introduce their own uncertainty and must themselves be evaluated.

Good practice includes:

- version the judge prompt;
- version the judge model;
- require structured output;
- include scoring criteria and evidence;
- calibrate against expert human labels;
- measure agreement and disagreement;
- test position/order bias where applicable;
- set timeouts and failure behavior;
- never let the judge override deterministic safety failures.

The judge is an evaluator component, not an oracle.

---

## 18. Human Evaluation

Human evaluation remains essential for areas where product quality depends on domain judgment.

A good human-evaluation process should define:

- a rubric;
- rating scale;
- reviewer guidance;
- blind or randomized presentation where practical;
- adjudication rules;
- reviewer calibration;
- inter-rater agreement;
- sampled re-review.

Human labels can then become calibration data for automated metrics and judges.

The long-term goal is not to remove humans from evaluation. It is to use scarce expert review where it adds the most value.

---

## 19. Statistical Thinking for Probabilistic Systems

One run is not always enough.

If model sampling or application state introduces meaningful variability, run selected cases multiple times and measure distributions.

Useful measures include:

- pass rate;
- mean/median score;
- standard deviation;
- worst observed outcome;
- confidence interval;
- rate of critical failure;
- variance by model/configuration.

A candidate should not be promoted simply because its average score is slightly higher. Teams should ask whether the difference is meaningful, repeatable, and worth any increase in cost or latency.

---

## 20. Candidate-versus-Baseline Regression Testing

Every important LLM change can create regression:

- model upgrade;
- prompt change;
- system instruction change;
- temperature change;
- retrieval configuration;
- new embedding model;
- chunking strategy;
- safety policy;
- tool definition;
- context-window change.

Use paired case IDs so the same case is compared before and after the change.

For each metric:

```text
Delta = Candidate Metric − Baseline Metric
```

Then report:

- aggregate delta;
- per-case regressions;
- new critical failures;
- fixed failures;
- statistical interval where appropriate;
- latency delta;
- token delta;
- cost delta.

Do not replace the baseline simply because the new candidate fails it. Baseline changes should be reviewed as deliberate quality decisions.

---

## 21. Multi-Objective Evaluation

LLM systems involve trade-offs.

A new model may be:

- 4% more correct;
- 2× slower;
- 35% more expensive;
- safer on injection cases;
- worse on JSON validity.

Therefore release decisions are multi-objective.

A useful decision table might be:

| Dimension | Baseline | Candidate | Decision rule |
|---|---:|---:|---|
| Correctness | 0.88 | 0.92 | Improve or stay within tolerance |
| Safety pass rate | 100% | 100% | Must remain 100% for critical pack |
| Schema validity | 99.8% | 100% | No blocker regression |
| P95 latency | 1.4 s | 2.1 s | ≤ 2.5 s |
| Avg cost | $0.008 | $0.011 | ≤ approved budget |

This is more useful than one opaque “LLM quality score.”

---

## 22. Weighted Scores and Their Limits

Weighted scores can help summarize non-critical quality:

\[
Score = \sum_{i=1}^{n} w_i m_i
\]

where \(w_i\) is the metric weight and \(m_i\) is the normalized metric value.

However, weighted scores should not average away blockers.

A release policy can therefore combine:

```text
Weighted quality score ≥ threshold
AND safety blockers = 0
AND schema blockers = 0
AND critical cases pass
AND regression budget not exceeded
```

This pattern keeps summary metrics useful without sacrificing governance.

---

## 23. Quality Gates in CI/CD

Evaluation becomes operationally valuable when it participates in delivery.

A pull-request pipeline can run:

```text
Dataset validation
  ↓
Unit / integration tests
  ↓
Offline or bounded LLM evaluation
  ↓
Safety pack
  ↓
Schema checks
  ↓
Candidate-baseline comparison
  ↓
Quality gate
  ↓
Publish evaluation evidence
```

Recommended outputs include:

- machine-readable JSON;
- JUnit for CI systems;
- HTML for reviewers;
- summary metrics;
- blocker findings;
- case-level evidence;
- model and prompt versions;
- dataset version;
- latency/token/cost metadata.

A gate is only trustworthy if the evidence behind it can be inspected.

---

## 24. Evaluation Environments

Not every evaluation belongs in every pipeline.

A tiered model works well:

### Tier 1 — Pull request
Fast, deterministic, credential-free where possible.

- dataset/schema validation;
- unit tests;
- mock/replay evaluation;
- critical safety checks;
- structured-output tests.

### Tier 2 — Integration
Bounded live-provider testing.

- real model calls;
- semantic judges;
- retrieval integration;
- cost and latency measurement.

### Tier 3 — Scheduled benchmark
Broader and potentially expensive.

- full golden set;
- repeated runs;
- red-team suite;
- model comparisons;
- long-context tests.

### Tier 4 — Production monitoring
Real-world signals with privacy controls.

- sampled quality review;
- latency/error/cost drift;
- safety incidents;
- user feedback;
- retrieval/source drift.

---

## 25. Observability and Evaluation Are Complementary

Observability explains what happened in a running system. Evaluation determines whether that behavior met an explicit quality contract.

Useful trace metadata includes:

- request ID;
- model and deployment version;
- prompt/template version;
- retrieval configuration;
- context/source IDs;
- tool calls;
- latency by stage;
- retries;
- token usage;
- judge/evaluator version;
- final quality outcome.

Avoid logging secrets or unnecessary sensitive content. Evaluation evidence should be useful without becoming a new data exposure surface.

---

## 26. Security and Evaluation

LLM security should be testable.

The **OWASP GenAI LLM Top 10 2026**, released in August 2026, provides current community guidance on critical LLM application risks. The evaluation program should translate relevant risks into system-specific test cases, such as injection, information disclosure, improper output handling, excessive access, or unsafe downstream behavior.

Security testing should also include conventional application security:

- authentication;
- authorization;
- tenant isolation;
- secrets management;
- API abuse;
- dependency risk;
- logging controls;
- rate limiting;
- secure deployment.

AI security does not replace software security; it expands the quality surface.

---

## 27. Governance and NIST Alignment

NIST's **AI Risk Management Framework (AI RMF 1.0)** provides a voluntary structure for governing, mapping, measuring, and managing AI risk. The **NIST AI 600-1 Generative AI Profile** extends that risk-management approach for generative AI and explicitly addresses evaluation across the AI lifecycle.

An engineering evaluation program can operationalize parts of that thinking by retaining:

- approved evaluation datasets;
- evaluator versions;
- model and prompt versions;
- quality thresholds;
- test evidence;
- human approvals;
- known limitations;
- release decisions;
- post-release findings.

Framework alignment is not certification. Organizations remain responsible for their own legal, regulatory, risk, and domain obligations.

---

## 28. Provider-Neutral Evaluation Architecture

Evaluation should not be tightly coupled to one model SDK.

A provider adapter can normalize output into a common record:

```text
ProviderResult
├── output
├── model_version
├── latency
├── token_usage
├── cost
├── tool_calls
├── error/retry metadata
└── provider metadata
```

Evaluators then operate on the normalized result rather than directly on vendor APIs.

Benefits include:

- easier model comparison;
- stable test datasets;
- easier migration;
- simpler replay testing;
- reduced evaluator duplication;
- clearer audit evidence.

The companion reference implementation uses this provider-neutral pattern.

---

## 29. Cost and Token Evaluation

Cost is a quality attribute when AI usage is material to the product economics.

Track:

- input tokens;
- output tokens;
- cached tokens where applicable;
- model cost;
- retrieval/tool cost;
- average cost per successful task;
- cost per evaluation suite;
- cost delta against baseline.

Do not invent usage when the provider does not report it. Unknown is better than false precision.

A useful business metric is:

\[
CostPerSuccessfulTask = \frac{TotalCost}{SuccessfulTasks}
\]

This combines efficiency with actual quality.

---

## 30. Latency and Reliability

LLM latency should be evaluated as a distribution rather than a single average.

Track:

- P50;
- P95;
- P99;
- timeout rate;
- retry rate;
- provider error rate;
- first-token latency where relevant;
- end-to-end task latency.

For agentic or RAG systems, also capture stage latency so teams can distinguish model delay from retrieval, tool, or orchestration delay.

---

## 31. Common Evaluation Anti-Patterns

### Anti-pattern 1: “We tested 20 prompts manually”
This is a demo, not a regression strategy.

### Anti-pattern 2: One metric represents quality
LLM quality is multi-dimensional.

### Anti-pattern 3: A judge scores everything
Deterministic properties should remain deterministic.

### Anti-pattern 4: The average score passes, therefore the release passes
Critical failures must be explicit blockers.

### Anti-pattern 5: Baseline replaced whenever the candidate fails
This destroys regression integrity.

### Anti-pattern 6: Dataset cases have no stable IDs
Paired comparison and traceability become difficult.

### Anti-pattern 7: Evaluation prompts and models are not versioned
Results cannot be reproduced.

### Anti-pattern 8: Cost and latency are ignored
A quality improvement may be commercially unacceptable.

### Anti-pattern 9: Safety testing is a one-time exercise
Threats and application behavior evolve.

### Anti-pattern 10: Production feedback replaces pre-release evaluation
Both are needed.

---

## 32. A Practical Enterprise Adoption Roadmap

### Stage 1 — Define the quality contract
- identify use cases and risks;
- define allowed/refusal behavior;
- establish initial metrics and blockers.

### Stage 2 — Build the golden dataset
- start with critical business cases;
- add negative, edge, and safety cases;
- version and review the dataset.

### Stage 3 — Add deterministic evaluators
- required facts;
- schema;
- citations;
- safety patterns;
- latency and usage.

### Stage 4 — Add semantic evaluation
- calibrated model judge;
- expert human rubric;
- agreement analysis.

### Stage 5 — Establish baselines
- record approved model/configuration;
- retain case-level evidence;
- define regression budgets.

### Stage 6 — Integrate CI/CD
- PR smoke evaluation;
- safety hard gates;
- baseline comparison;
- evidence artifacts.

### Stage 7 — Expand operations
- scheduled benchmarks;
- production sampling;
- incident-derived cases;
- drift and cost monitoring.

---

## 33. Suggested Quality Engineering KPIs

A balanced AI quality scorecard can include:

### Outcome quality
- critical-case pass rate;
- correctness;
- required-fact completeness;
- groundedness;
- citation validity.

### Risk
- safety blocker count;
- privacy failures;
- over-refusal rate;
- unsupported-claim rate.

### Engineering quality
- schema-valid response rate;
- evaluation dataset coverage;
- regression count;
- unresolved high-risk cases.

### Operations
- P95 latency;
- retry/error rate;
- tokens per successful task;
- cost per successful task.

### Governance
- percentage of releases with retained evaluation evidence;
- dataset freshness;
- human-review completion for high-risk releases;
- evaluator/model/prompt version traceability.

---

## 34. Reference Implementation

The companion [LLM Quality Evaluation Harness](https://github.com/ashokmanohar-ai/llm-quality-evaluation-harness) demonstrates an implementation-oriented version of this framework.

It includes:

- versioned golden and regression datasets;
- correctness, relevance, completeness, groundedness, citation, safety, and structured-output checks;
- hard safety and schema gates;
- candidate-versus-baseline paired comparison;
- confidence-interval reporting;
- latency, token, and cost evidence;
- provider-neutral adapters;
- FastAPI and CLI execution;
- SQLite evidence storage for the reference MVP;
- Docker;
- Pytest and Playwright validation;
- GitHub Actions quality gates;
- governance, threat-model, responsible-AI, operating-model, and adoption documentation.

The repository intentionally uses a deterministic offline path so evaluators, policies, reports, and CI behavior can be exercised without external model credentials. This validates the evaluation engineering mechanics; it does not claim that synthetic datasets or lexical metrics prove real production model quality.

---

## 35. Limitations

No evaluation framework eliminates uncertainty.

Important limitations include:

- reference answers may themselves be incomplete or wrong;
- automated metrics can disagree with experts;
- model judges can be biased or unstable;
- safety taxonomies cannot anticipate every attack;
- synthetic datasets may not represent production usage;
- evaluation suites can become stale;
- statistical confidence depends on representative sample size;
- product behavior may change due to upstream providers or data;
- operational constraints differ across organizations and domains.

Therefore, quality evidence should inform accountable engineering and business decisions rather than be treated as mathematical proof of safety or correctness.

---

## 36. Conclusion

LLM evaluation is not a replacement for software testing. It is the extension of Quality Engineering into probabilistic systems.

The strongest programs preserve familiar engineering principles:

- explicit requirements;
- traceable test cases;
- controlled environments;
- reproducible evidence;
- deterministic assertions where possible;
- measurable non-functional requirements;
- regression testing;
- release gates;
- human accountability.

They then add what generative AI requires:

- semantic evaluation;
- groundedness;
- hallucination and citation checks;
- refusal quality;
- repeated-run analysis;
- model/prompt/dataset versioning;
- safety testing;
- token and cost evaluation;
- calibrated judges;
- AI-specific governance.

The result is a shift from **“the model seems good”** to **“the system has evidence that it meets an explicit quality contract for this release.”**

That is the role Quality Engineering can play in making generative AI systems more measurable, explainable, governable, and releasable.

---

## References

1. National Institute of Standards and Technology (NIST), **Artificial Intelligence Risk Management Framework (AI RMF 1.0)**, NIST AI 100-1, 2023. https://doi.org/10.6028/NIST.AI.100-1
2. NIST, **Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile**, NIST AI 600-1, 2024. https://doi.org/10.6028/NIST.AI.600-1
3. OWASP GenAI Security Project, **OWASP GenAI LLM Top 10 2026**, 2026. https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/
4. OWASP GenAI Security Project, **GenAI Data Security Risks & Mitigations 2026**, 2026. https://genai.owasp.org/resource/owasp-genai-data-security-risks-mitigations-2026/
5. OpenAI, **Evals** — open-source framework and examples for evaluating LLM systems. https://github.com/openai/evals
6. DeepEval documentation — LLM evaluation concepts and metrics. https://deepeval.com/
7. RAGAS documentation — evaluation approaches for RAG and LLM applications. https://docs.ragas.io/
8. OpenTelemetry, **Observability Framework**. https://opentelemetry.io/
9. Companion implementation: Ashok Kumar Manohar, **LLM Quality Evaluation Harness**. https://github.com/ashokmanohar-ai/llm-quality-evaluation-harness

---

## Suggested Citation

**Manohar, Ashok Kumar. (2026). _LLM Evaluation for Quality Engineers: From Functional Testing to AI Quality Metrics_. Version 1.0. GitHub.**

Repository: https://github.com/ashokmanohar-ai/llm-quality-evaluation-harness

White paper: https://github.com/ashokmanohar-ai/llm-quality-evaluation-harness/blob/main/WHITEPAPER.md

---

## About the Author

**Ashok Kumar Manohar** works across Quality Engineering, test architecture, AI-assisted testing, LLM and RAG evaluation, agentic AI quality, Playwright automation, API testing, CI/CD, and enterprise AI engineering practices.

This white paper is part of an independent technical publication series exploring practical engineering approaches for testing and governing AI-powered software systems.
