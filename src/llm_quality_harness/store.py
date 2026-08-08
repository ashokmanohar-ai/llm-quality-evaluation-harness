from __future__ import annotations

import sqlite3
from pathlib import Path

from llm_quality_harness.models import SuiteResult


class ResultStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS suite_results (
                    suite_id TEXT PRIMARY KEY,
                    generated_at TEXT NOT NULL,
                    payload TEXT NOT NULL
                )
                """
            )

    def save(self, result: SuiteResult) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO suite_results (suite_id, generated_at, payload)
                VALUES (?, ?, ?)
                ON CONFLICT(suite_id) DO UPDATE SET
                    generated_at = excluded.generated_at,
                    payload = excluded.payload
                """,
                (result.suite_id, result.generated_at.isoformat(), result.model_dump_json()),
            )

    def get(self, suite_id: str) -> SuiteResult | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT payload FROM suite_results WHERE suite_id = ?", (suite_id,)
            ).fetchone()
        return SuiteResult.model_validate_json(row["payload"]) if row else None

    def list(self, limit: int = 20) -> list[SuiteResult]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT payload FROM suite_results ORDER BY generated_at DESC LIMIT ?", (limit,)
            ).fetchall()
        return [SuiteResult.model_validate_json(row["payload"]) for row in rows]

