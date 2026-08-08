# Validation report

## Scope

This report records validation of the reference MVP, not a production AI system or real provider. The reference data and responses are synthetic.

## Results

Validated on 2026-08-08 with Python 3.12.13 and the repository's pinned Node dependencies.

| Check | Result | Evidence |
|---|---|---|
| Dataset contract | Pass | 8 unique cases; 14 coverage tags |
| Lint | Pass | Ruff: all checks passed |
| Unit/integration/API | Pass | 35 pytest tests |
| Branch-aware coverage | Pass | 96.95%; policy minimum 85% |
| Reference evaluation | Pass | 8/8 cases; suite score 1.0000 |
| Six metric means | Pass | Correctness, groundedness, relevance, completeness, citation validity, safety: 1.0000 |
| Operational evidence | Pass | P95 latency 205 ms; average supplied cost $0.000775 |
| Release gate | Pass | All 12 findings passed, including safety and schema blocker gates |
| Secret scan | Pass | 0 repository findings |
| Node dependency audit | Pass | 0 known npm vulnerabilities reported |
| Playwright API journey | Pass | Health, metadata, and offline demo API test |
| Playwright browser journey | Environment condition | Test is defined and listed; local Chromium exited with `SIGTRAP` in this sandbox |

The perfect reference score is expected because the small synthetic golden responses intentionally match their approved references. It validates the evaluator and gate mechanics; it is not evidence that a real model is perfect or production-ready.

## Browser condition

The workspace browser proxy returned an empty/truncated Chromium archive, and the available cached Chromium binary exited with `SIGTRAP` before a page opened. No UI assertion ran locally, so the browser journey is not reported as passed. The supported Ubuntu GitHub Actions job installs Chromium, runs both Playwright cases, and retains HTML, JUnit, traces, screenshots, and video on failure.

## Decision

**Approved with one environment condition** for reference-MVP publication: confirm the browser journey in GitHub Actions. Enterprise production use remains out of scope until the controls in the architecture, threat model, and implementation plan are implemented and calibrated for an approved use case.
