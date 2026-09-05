# Testing Hallucinations in Generative AI

## Detection, Measurement, Root Cause and Release Controls

**Technical White Paper — Version 1.0**  
**September 2026**

**Author:** Ashok Kumar Manohar  
**GitHub:** [ashokmanohar-ai](https://github.com/ashokmanohar-ai)  
**Primary reference implementation:** [LLM Quality Evaluation Harness](https://github.com/ashokmanohar-ai/llm-quality-evaluation-harness)  
**Related implementations:** [RAG & LLM Evaluation Lab](https://github.com/ashokmanohar-ai/rag-llm-evaluation-lab), [AI Agent Evaluation Framework](https://github.com/ashokmanohar-ai/ai-agent-evaluation-framework), [Phoenix LLM Observability](https://github.com/ashokmanohar-ai/phoenix-llm-observability), [Promptfoo LLM Testing](https://github.com/ashokmanohar-ai/promptfoo-llm-testing), and [Continuous Quality Engineering](https://github.com/ashokmanohar-ai/continuous-quality-engineering)

> **Publication note:** This is an independent practitioner white paper supported by open-source reference implementations. It is not a peer-reviewed academic publication, legal opinion, compliance certification, security certification, medical or financial validation framework, or statement of production readiness. Hallucination definitions, severity levels, test datasets, judges, thresholds and release controls must be calibrated for the product domain, user population, deployment environment and risk profile.

---

## Abstract

Generative AI systems can produce fluent, confident and useful responses while also producing claims that are unsupported, contradicted, fabricated, stale, misattributed or inappropriate for the available evidence. These failures are commonly grouped under the term **hallucination**. For engineering teams, however, that label is too broad to support reliable diagnosis or release decisions.

A hallucination may originate from several different layers: the model may invent a fact; a RAG retriever may miss the correct source; a context builder may drop a critical chunk; a prompt may encourage overconfident completion; a tool-using agent may report an action that never occurred; a citation may exist but fail to support the associated claim; a model may answer from parametric memory when the product requires evidence-only behavior; or stale context may be faithfully repeated even though it is no longer correct.

This white paper presents **Hallucination Testing** as an evidence-driven Quality Engineering discipline. It proposes a **Claim–Evidence–Classify–Localize–Control–Gate model**. Generated output is decomposed into meaningful claims. Each claim is compared with authoritative evidence. Failures are classified by type and severity. Root cause is localized to the model, prompt, retrieval, context, tool, memory, citation or orchestration layer. Controls such as abstention, grounding, validation, retrieval, approval and output handling are tested. Finally, release gates evaluate hallucination risk alongside correctness, safety, authorization, latency and cost.

The framework deliberately separates **factual correctness**, **groundedness**, **citation integrity**, **answerability**, **uncertainty**, **contradiction**, **fabrication**, **staleness**, and **action hallucination**. It also distinguishes deterministic validation from semantic judgment. Exact identifiers, numbers, schemas, citations, tool calls and business state should be verified deterministically wherever possible; calibrated human or model judges should be used only where semantic interpretation is genuinely required.

The central proposition is:

> **Hallucination quality is not the absence of every possible model error. It is the ability to detect unsupported claims, understand why they occurred, constrain their impact, and block releases when the remaining risk exceeds an explicit quality policy.**

---

## 1. Executive Summary

A model response can fail in several different ways:

```text
Question / Task
      ↓
Available Evidence
      ↓
Prompt / Policy
      ↓
Model / Retrieval / Tools
      ↓
Generated Claims
      ↓
Claim-to-Evidence Verification
      ↓
Hallucination Classification
      ↓
Root-Cause Localization
      ↓
Mitigation / Regression Test
      ↓
Release Gate
```

The important engineering questions are:

1. Which statements in the response are factual claims?
2. Which claims are supported by authoritative evidence?
3. Which claims contradict evidence?
4. Which claims are fabricated or unverifiable?
5. Was the evidence itself current and authorized?
6. Did the system have enough evidence to answer?
7. Should it have abstained instead?
8. Did a retrieval, prompt, model, tool or orchestration layer cause the failure?
9. What is the business severity of the hallucination?
10. Is the failure now represented by a permanent regression case?
11. Should this release be allowed to proceed?

A useful hallucination program therefore combines **detection, measurement, diagnosis, mitigation and release governance**.

---

## 2. Terminology: Hallucination, Confabulation and Misinformation

The industry uses several overlapping terms.

For this framework:

- **Hallucination** is the umbrella engineering term for generated content that is unsupported, fabricated, contradicted or otherwise inconsistent with the evidence and task contract.
- **Confabulation** is used for confidently presented erroneous or false generated content.
- **Misinformation** refers to false or misleading information presented to users, whether its origin is hallucination, stale data, biased source material, incorrect retrieval or another system defect.
- **Unsupported claim** is a statement for which the system cannot identify sufficient evidence under the product's evidence policy.
- **Contradicted claim** conflicts with available authoritative evidence.
- **Fabricated entity or event** introduces a person, document, transaction, source, status, citation, tool result or action that did not exist in observed evidence.

A useful engineering taxonomy should not depend on one word. It should record the exact failure.

---

## 3. Why One Hallucination Score Is Not Enough

Suppose two models each have a 5% hallucination rate.

Model A occasionally adds a harmless unsupported adjective. Model B occasionally invents a payment confirmation or legal requirement. The same rate does not represent the same risk.

Hallucination measurement must therefore include:

- frequency;
- severity;
- claim type;
- evidence strength;
- user impact;
- actionability;
- detectability;
- domain criticality;
- whether the error affects a consequential action;
- whether the system expressed uncertainty or false confidence.

---

## 4. The Claim–Evidence–Classify–Localize–Control–Gate Model

The proposed model has six stages.

### Claim
Decompose the response into atomic, testable assertions.

### Evidence
Identify the authoritative evidence that could support or refute each claim.

### Classify
Assign each claim a status such as grounded, unsupported, contradicted, stale, fabricated, unverifiable or non-factual.

### Localize
Determine which system layer most likely caused the failure.

### Control
Test the mitigation: retrieval, prompt, validation, abstention, approval, tool verification or other control.

### Gate
Apply release policy using case severity, rates, regressions and evidence completeness.

---

## 5. Claim-Level Evaluation Is More Useful Than Answer-Level Evaluation

An answer may contain ten factual statements and only one may be unsupported.

A single answer-level label such as `PASS` or `FAIL` loses diagnostic detail.

A claim record should retain at least:

```json
{
  "claim_id": "C-03",
  "text": "The order was refunded on 5 September.",
  "type": "transaction_status",
  "status": "CONTRADICTED",
  "evidence_ids": ["payment-781", "refund-events"],
  "severity": "HIGH",
  "source_stage": "generation",
  "confidence_label": "high"
}
```

---

## 6. Separate Factual Claims from Non-Factual Content

Not every sentence requires factual verification.

Typical categories include:

- factual claim;
- recommendation;
- opinion;
- stylistic text;
- question;
- uncertainty statement;
- instruction;
- citation;
- action statement;
- policy or refusal statement.

Hallucination metrics should use an appropriate denominator. Counting greetings or stylistic transitions as factual claims distorts results.

---

## 7. Groundedness and Correctness Are Different

A claim may be:

| Correct in reality | Supported by supplied evidence | Interpretation |
|---|---|---|
| Yes | Yes | Desired grounded answer |
| Yes | No | Correct but ungrounded; may violate evidence-only policy |
| No | Yes | Evidence itself may be wrong, stale or misread |
| No | No | Unsupported or fabricated claim |

This distinction is especially important for RAG and regulated workflows.

---

## 8. Define the Evidence Policy Before Testing

A product must decide what evidence counts.

Possible policies include:

- model may use general world knowledge;
- model may use only supplied context;
- model may use approved enterprise knowledge plus tool results;
- model may use current external sources from an allowlist;
- model must cite every material factual claim;
- model must abstain when evidence is insufficient.

Without an evidence policy, “hallucination” becomes subjective.

---

## 9. A Practical Hallucination Taxonomy

Recommended classes include:

1. **Unsupported factual claim**
2. **Contradicted claim**
3. **Fabricated entity**
4. **Fabricated source or citation**
5. **Fabricated tool call or action**
6. **Stale claim**
7. **Misattributed claim**
8. **Numerical hallucination**
9. **Temporal hallucination**
10. **Relationship hallucination**
11. **Overgeneralization**
12. **False-premise acceptance**
13. **Scope hallucination**
14. **Cross-tenant or cross-user fact leakage**
15. **Instruction hallucination**
16. **Unsupported recommendation**
17. **Inconsistent self-contradiction**
18. **Cascading agent hallucination**

The taxonomy should evolve from observed failures.

---

## 10. Unsupported Claims

An unsupported claim may be plausible and even true, but if the application requires evidence-backed output and no approved evidence supports it, it should be flagged.

This category is useful because it avoids forcing the evaluator to prove universal falsity.

---

## 11. Contradictions Are Stronger Evidence Than Mere Absence

If the response says:

> “The ticket is closed.”

while the authoritative tool result says:

```json
{"ticket_id":"INC-102","status":"OPEN"}
```

this is a deterministic contradiction.

Contradictions should generally carry greater severity than evidence absence because the system ignored known evidence.

---

## 12. Fabricated Entities and Sources

Test for invented:

- people;
- customers;
- tickets;
- orders;
- documents;
- regulations;
- URLs;
- product features;
- package names;
- citations;
- transactions;
- approval decisions.

Where identifiers follow known formats, deterministic existence checks are preferable to semantic judges.

---

## 13. Numerical Hallucinations

Numbers deserve dedicated validation because small differences can have high impact.

Examples:

- price;
- quantity;
- tax;
- percentage;
- dates;
- SLA duration;
- leave entitlement;
- risk score;
- dosage-like quantities in high-stakes domains;
- token or cost claims;
- performance metrics.

Extract and compare numerical facts deterministically wherever possible.

---

## 14. Temporal Hallucinations and Staleness

A statement can be grounded in an old source and still be operationally wrong.

Test:

- effective dates;
- superseded policies;
- latest status;
- stale cached results;
- expired offers;
- old model knowledge presented as current;
- conflicting historical versions.

Freshness is a first-class quality dimension.

---

## 15. Citation Hallucination

Citation testing should distinguish:

1. citation syntax valid;
2. cited source exists;
3. source was actually available to the system;
4. source supports the associated claim;
5. material claims have adequate citation coverage;
6. citations are current and authorized.

A real source attached to an unsupported claim is still a citation failure.

---

## 16. Action Hallucination in Agents

Agentic systems create a special class of hallucination: claiming that an action occurred when execution evidence says otherwise.

Examples:

- “I created the ticket” without a `create_ticket` tool call;
- “The refund was approved” when approval is still pending;
- “I sent the email” when the tool failed;
- “The deployment succeeded” when the pipeline returned an error.

For actions, the primary oracle is **tool and system evidence**, not text similarity.

---

## 17. Tool-Result Hallucination

An agent may call the correct tool but misstate the result.

Evaluate:

- exact tool selected;
- arguments;
- result status;
- returned identifiers;
- side-effect evidence;
- final-answer consistency with the tool result.

A successful tool call followed by an incorrect summary is still a quality failure.

---

## 18. False-Premise Questions

Users may ask questions containing incorrect assumptions.

Example:

> “Why was my approved refund of £500 reversed?”

when no such refund exists.

A robust system should challenge or verify the premise rather than invent an explanation.

False-premise datasets are important because they test whether fluency pressure overrides evidence.

---

## 19. Answerability Must Be Measured

Before asking “Was the answer correct?”, ask:

> **Was the question answerable from the permitted evidence?**

Datasets should include:

- answerable cases;
- partially answerable cases;
- unanswerable cases;
- contradictory-evidence cases;
- stale-evidence cases;
- unauthorized-evidence cases.

This enables meaningful abstention testing.

---

## 20. Abstention Is a Quality Capability

When evidence is insufficient, a safe response may be:

- admit uncertainty;
- request clarification;
- state what evidence is missing;
- route to a human;
- suggest a safe next step.

Measure both:

- **false answer rate** — system answers when it should abstain;
- **over-refusal rate** — system abstains when sufficient evidence exists.

---

## 21. Confidence Language Must Be Tested

Models can express unwarranted certainty.

Test wording such as:

- “definitely”;
- “confirmed”;
- “guaranteed”;
- “the record shows”;
- “I verified”;

against actual evidence strength.

A hallucination stated with high confidence may deserve higher severity because it increases overreliance risk.

---

## 22. Deterministic Checks First

Use software assertions before model judges when the fact is machine-verifiable.

Deterministic candidates include:

- JSON schema;
- identifier existence;
- exact numbers;
- tool calls;
- arguments;
- database state;
- citation IDs;
- source versions;
- timestamps;
- approval status;
- required/forbidden text;
- regex and format constraints;
- known facts from structured fixtures.

**If software can prove it, do not ask another model to guess it.**

---

## 23. Semantic Evaluation for Genuine Meaning

Semantic judges are useful for:

- whether evidence entails a paraphrased claim;
- whether a recommendation is supported by the supplied facts;
- whether the response overgeneralizes;
- whether uncertainty is communicated appropriately;
- whether a complex claim preserves material qualifiers.

Judge outputs should be structured, versioned and calibrated against human-reviewed examples.

---

## 24. LLM-as-a-Judge Is a Measurement Instrument

A hallucination judge can itself hallucinate or show bias.

Track:

- judge model and version;
- judge prompt version;
- rubric;
- temperature/configuration;
- human agreement;
- repeated-run stability;
- false-positive rate;
- false-negative rate;
- disagreement cases;
- adversarial inputs;
- position and style bias where relevant.

Do not allow one unvalidated judge score to become the only release oracle.

---

## 25. Human Evaluation Remains Important

Human review is especially useful for:

- high-severity domain claims;
- ambiguous evidence;
- policy interpretation;
- judge calibration;
- novel failure types;
- disagreements between evaluators;
- samples near release thresholds.

Human labels should be retained as versioned evaluation evidence, not informal comments.

---

## 26. Hallucination Density

A useful metric is:

\[
HallucinationDensity = \frac{Unsupported + Contradicted + Fabricated\;Claims}{Total\;Factual\;Claims}
\]

This is more informative than counting failed answers when answers vary greatly in length.

Use it with severity, not alone.

---

## 27. Unsupported-Claim Rate

\[
UnsupportedClaimRate = \frac{Unsupported\;Claims}{Factual\;Claims}
\]

This metric is particularly useful for evidence-only assistants and RAG systems.

---

## 28. Contradiction Rate

\[
ContradictionRate = \frac{Contradicted\;Claims}{Claims\;with\;Authoritative\;Evidence}
\]

A contradiction budget may be zero for critical structured facts.

---

## 29. Fabrication Rate

Track fabricated identifiers, citations, entities and actions separately.

A generic hallucination percentage can hide a dangerous increase in fabricated actions even while unsupported descriptive text decreases.

---

## 30. Severity-Weighted Hallucination Risk

A practical risk model can assign severity weights:

```text
LOW      = stylistic or low-impact unsupported detail
MEDIUM   = material factual error with limited consequence
HIGH     = business decision, user state or policy error
CRITICAL = safety, authorization, financial, legal or destructive-action error
```

A weighted metric may support trend analysis, but **critical failures must remain hard gates**.

---

## 31. Hallucination Root-Cause Localization

A useful root-cause taxonomy includes:

- corpus missing;
- corpus stale;
- access filter wrong;
- chunking defect;
- retriever miss;
- bad ranking;
- context truncation;
- prompt ambiguity;
- prompt overreach;
- model generation error;
- tool error;
- tool-result misuse;
- memory contamination;
- agent planning error;
- judge/evaluator error;
- post-processing corruption;
- stale cache;
- product requirement ambiguity.

Do not fix every hallucination by editing the prompt.

---

## 32. RAG Hallucination Diagnosis

For RAG, classify the path:

```text
Was authoritative source available?
  ↓ yes
Was it retrieved?
  ↓ yes
Was it ranked into context?
  ↓ yes
Was it preserved after truncation/deduplication?
  ↓ yes
Did the model use it correctly?
  ↓ yes
Did the citation support the claim?
```

Each `no` points to a different engineering owner and remediation.

---

## 33. Prompt-Induced Hallucination

Prompt changes can increase hallucination by:

- demanding an answer even when uncertain;
- rewarding completeness over truthfulness;
- requiring unsupported detail;
- suppressing abstention;
- providing conflicting instructions;
- encouraging hidden assumptions;
- requesting fake citations or examples as if factual.

Prompt regression suites should include hallucination-sensitive cases.

---

## 34. Model-Change Hallucination Regression

When changing model version or provider, hold the dataset and policy constant.

Compare:

- hallucination density;
- unsupported-claim rate;
- contradiction rate;
- false-answer rate;
- over-refusal rate;
- citation integrity;
- severity distribution;
- latency;
- token usage;
- cost.

An overall quality improvement should not hide a regression in critical hallucination categories.

---

## 35. Retrieval and Embedding Changes

Embedding model, chunking, top-K, hybrid weighting and reranker changes can alter hallucination indirectly by changing evidence availability.

Run retrieval and generation metrics together so a downstream hallucination increase can be traced back to retrieval configuration.

---

## 36. Agentic Cascading Hallucinations

In agents and multi-agent systems, one unsupported claim can become state for later steps.

A possible chain is:

```text
Agent A invents status
      ↓
Memory stores status
      ↓
Agent B trusts memory
      ↓
Tool selection changes
      ↓
Agent C reports action as confirmed
```

Test provenance at every handoff and prevent unverified generated claims from becoming authoritative state.

---

## 37. Memory Hallucination

Long-lived agent memory introduces additional tests:

- did memory record a generated claim as fact?
- can one user's memory leak into another session?
- are stale memories expired?
- can incorrect memory be corrected?
- is provenance retained?
- does memory contain an approval that is no longer valid?

Memory should be treated as data with lifecycle and trust level.

---

## 38. Hallucination and Security

Hallucinations can become security problems when downstream systems trust generated output.

Examples:

- invented package names passed to installers;
- fabricated URLs opened automatically;
- unsupported SQL generated and executed;
- false authorization assumptions;
- invented tool arguments;
- fake identity or tenant references;
- hallucinated approval state.

Secure systems validate generated output before use.

---

## 39. Overreliance Is a System Risk

A technically modest hallucination can cause significant harm if users believe the system is authoritative.

Test the complete product experience:

- confidence language;
- citations;
- UI warnings;
- source visibility;
- escalation routes;
- confirmation flows;
- user ability to inspect evidence;
- irreversible actions.

Hallucination risk is partly a human-system interaction problem.

---

## 40. Build Versioned Hallucination Datasets

A strong dataset should cover:

- direct factual questions;
- multi-fact questions;
- missing evidence;
- false premises;
- conflicting evidence;
- stale evidence;
- numbers and dates;
- citations;
- authorization scope;
- adversarial prompts;
- long context;
- retrieval noise;
- tool failures;
- agent actions;
- known production regressions.

Every case needs a stable ID, evidence, expected behavior, severity and provenance.

---

## 41. Production Failures Should Become Permanent Regression Cases

The learning loop should be:

```text
Production Hallucination
        ↓
Sanitize + Reproduce
        ↓
Classify + Localize
        ↓
Add Versioned Evaluation Case
        ↓
Fix Prompt / Retrieval / Model / Control
        ↓
Verify Candidate vs Baseline
        ↓
Keep Case Permanently
```

This converts incidents into durable quality intelligence.

---

## 42. Baseline Comparison

A release should compare candidate behavior to an approved baseline on the same evaluation dataset.

Track case-level deltas, not only averages:

- newly introduced hallucinations;
- fixed hallucinations;
- severity changes;
- category shifts;
- abstention changes;
- citation changes;
- high-risk regression count.

Never replace the baseline simply to make a release pass.

---

## 43. Statistical Thinking and Repeated Runs

Probabilistic models may produce different outputs across repeated runs.

For selected cases, measure:

- hallucination frequency across N runs;
- variance in claim count;
- stability of abstention;
- judge agreement;
- tail-risk occurrence;
- worst-case severity.

One passing run does not prove stability.

---

## 44. Release Gate Design

A hallucination-aware gate may include:

### Hard gates
- zero critical fabricated actions;
- zero cross-tenant claims;
- zero fabricated approvals;
- zero invented critical identifiers;
- zero unsupported critical policy claims;
- required citation integrity for high-risk facts.

### Threshold gates
- unsupported-claim rate below calibrated limit;
- hallucination density below limit;
- false-answer rate below limit;
- high-severity regression count within budget.

### Warnings
- mild increase in low-severity unsupported content;
- latency or cost near limits;
- judge disagreement above warning threshold.

### Advisory metrics
- style;
- verbosity;
- non-critical wording preferences.

A weighted score must never override a hard hallucination gate.

---

## 45. Missing Evidence Must Fail Closed When Mandatory

If the hallucination evaluation did not run, the pipeline should not silently report success.

Distinguish:

- evaluation passed;
- evaluation failed;
- required report missing;
- evaluator crashed;
- judge unavailable;
- evidence malformed;
- dataset incompatible.

Infrastructure failure is not model success.

---

## 46. CI/CD Profiles

### Pull Request
Fast deterministic checks, representative hallucination cases, structured output and critical safety cases.

### Nightly
Broader datasets, repeated runs, semantic judges, adversarial cases and model comparisons.

### Release
Full approved dataset, baseline comparison, all hard gates, human review for configured high-risk cases and retained evidence.

### Production Change
Risk-based evaluation triggered by model, prompt, retrieval, policy or tool changes.

---

## 47. Observability for Hallucination Diagnosis

Useful telemetry includes:

- trace ID;
- prompt version;
- model/provider/version;
- retrieval query and document IDs;
- context selected/dropped;
- tool calls/results;
- generated response;
- claim evaluation results;
- citation mapping;
- judge version;
- token use;
- latency;
- cost;
- gate decision.

Sensitive content should be minimized or redacted according to policy.

---

## 48. Root-Cause KPIs

Beyond hallucination rate, track:

- % failures localized to retrieval;
- % localized to context construction;
- % localized to generation;
- % localized to stale source data;
- % localized to tool-result misuse;
- mean time to classify a hallucination;
- mean time to add regression coverage;
- recurrence rate of previously fixed hallucinations;
- escaped high-severity hallucinations;
- production-to-regression conversion rate.

These metrics improve the engineering system rather than only scoring the model.

---

## 49. Common Anti-Patterns

### “The answer sounds right”
Fluency is not evidence.

### One generic hallucination judge
A single scalar hides failure type and judge error.

### Prompt-only mitigation
Many hallucinations are retrieval, data, tool or product-design defects.

### No unanswerable cases
The system never learns when to abstain.

### Citation presence treated as citation correctness
A citation can be real and still fail to support the claim.

### Average-only release gates
Critical hallucinations disappear inside aggregate scores.

### Updating the baseline after every model change
This destroys regression meaning.

### Production incidents not entering the dataset
The same class of failure can silently return.

---

## 50. Enterprise Adoption Roadmap

### Stage 1 — Define
Agree evidence policy, hallucination taxonomy, severity levels and critical claims.

### Stage 2 — Build
Create versioned datasets with claim-level expected evidence and unanswerable cases.

### Stage 3 — Automate
Add deterministic checks, structured semantic judges and reports.

### Stage 4 — Localize
Instrument retrieval, context, tools and generation so failures can be assigned to a system layer.

### Stage 5 — Gate
Introduce candidate-vs-baseline comparison and hard release controls.

### Stage 6 — Learn
Convert production failures into permanent regression tests and tune policy with real evidence.

---

## 51. Reference Implementation Mapping

The companion **LLM Quality Evaluation Harness** demonstrates several foundations used by this paper:

- versioned evaluation datasets;
- deterministic-first quality checks;
- groundedness and hallucination-oriented evaluation;
- citation and safety dimensions;
- structured-output validation;
- candidate-versus-baseline comparison;
- hard safety/schema gates;
- latency, token and cost evidence;
- provider-neutral evaluation architecture;
- JSON/HTML evidence and CI/CD integration.

The related **RAG & LLM Evaluation Lab** adds retrieval, context, groundedness, hallucination and citation localization. The **AI Agent Evaluation Framework** adds tool/action verification and unsupported-claim checks. **Phoenix LLM Observability** provides trace-oriented diagnosis patterns. **Continuous Quality Engineering** provides normalized evidence and release-gate semantics.

These repositories are reference implementations and learning assets, not production certifications.

---

## 52. Limitations

No hallucination test suite can prove that a model will never produce false or unsupported content.

Limitations include:

- incomplete evaluation datasets;
- ambiguous or changing ground truth;
- judge error;
- domain expertise requirements;
- model nondeterminism;
- evolving external facts;
- retrieval and source-quality limitations;
- production context not represented offline;
- adversarial inputs not yet discovered.

The objective is **risk reduction with measurable evidence**, not a claim of zero hallucinations.

---

## 53. Conclusion

Hallucination is not one defect and should not be managed with one score.

A mature Quality Engineering system decomposes outputs into claims, verifies those claims against an explicit evidence policy, distinguishes unsupported statements from contradictions and fabrication, measures severity, localizes root cause, tests mitigations, preserves production failures as regressions and blocks releases when critical risk remains unacceptable.

The engineering principle is:

> **Detect the claim. Verify the evidence. Localize the cause. Control the impact. Preserve the regression. Gate the release.**

That turns hallucination from a vague concern about model behavior into an observable and governable software-quality problem.

---

## References

1. NIST, **Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile**, NIST AI 600-1, 2024; NIST publication page updated 2026.
2. OWASP GenAI Security Project, **OWASP GenAI LLM Top 10 2026**, 2026.
3. OWASP GenAI Security Project, **LLM09: Misinformation**, describing hallucination and overreliance risks.
4. Das, S., Abualhaija, S., & Bianculli, D., **How Much Do Legal RAG Systems Still Hallucinate?**, 2026.
5. Elchafei, P., Swain, M., Masoudian, S., & Schedl, M., **Facet-Level Tracing of Evidence Uncertainty and Hallucination in RAG**, 2026.
6. OpenTelemetry, GenAI semantic-convention and observability guidance.
7. Ashok Kumar Manohar, **LLM Evaluation for Quality Engineers: From Functional Testing to AI Quality Metrics**, 2026.
8. Ashok Kumar Manohar, **RAG Evaluation Beyond Accuracy: Retrieval Quality, Groundedness, Citation Integrity and Failure Localization**, 2026.
9. Ashok Kumar Manohar, **Evaluating AI Agents: Metrics, Test Strategies and Quality Gates for Autonomous Systems**, 2026.
10. Ashok Kumar Manohar, **Quality Gates for Generative AI: Designing Release Policies for LLM, RAG and Agentic Systems**, 2026.
