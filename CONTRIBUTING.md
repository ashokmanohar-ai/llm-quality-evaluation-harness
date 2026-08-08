# Contributing

1. Create a focused branch and explain the quality risk being addressed.
2. Version changed datasets, prompts, policies, schemas, and thresholds.
3. Run `make quality` and `npm run test:e2e`.
4. Attach evaluation, gate, coverage, and Playwright evidence to the pull request.
5. Never weaken a gate merely to make CI pass. Propose a threshold change with evidence and accountable approval.

All test data must be synthetic or explicitly approved. Provider integrations must redact credentials and sensitive content, implement bounded timeouts/retries, and expose token, cost, and model-version metadata.

