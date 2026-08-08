# ADR 0001: Start with a modular monolith

Status: accepted

The MVP uses one Python package with explicit provider, evaluator, runner, gate, statistics, store, and delivery boundaries. This minimizes operational complexity and keeps the end-to-end decision reviewable. Services should be extracted only for independent scale, deployment, ownership, or security boundaries. The trade-off is that the reference SQLite/API process is not horizontally scalable.

