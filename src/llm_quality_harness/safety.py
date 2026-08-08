from __future__ import annotations

import re
from typing import Any

from llm_quality_harness.models import SafetyFinding


class SafetyScanner:
    def __init__(self, config: dict[str, Any]) -> None:
        safety = config.get("safety", {})
        self.injection_patterns = [
            re.compile(pattern, re.IGNORECASE) for pattern in safety.get("injection_patterns", [])
        ]
        self.pii_patterns = [
            re.compile(pattern, re.IGNORECASE) for pattern in safety.get("pii_patterns", [])
        ]
        self.refusal_markers = [
            marker.lower() for marker in safety.get("refusal_markers", [])
        ]

    def scan(self, prompt: str, response: str) -> list[SafetyFinding]:
        findings: list[SafetyFinding] = []
        for pattern in self.injection_patterns:
            match = pattern.search(prompt)
            if match:
                findings.append(
                    SafetyFinding(
                        code="PROMPT_INJECTION",
                        severity="high",
                        location="prompt",
                        evidence=match.group(0)[:80],
                    )
                )
        for pattern in self.pii_patterns:
            match = pattern.search(response)
            if match:
                findings.append(
                    SafetyFinding(
                        code="PII_LEAKAGE",
                        severity="critical",
                        location="response",
                        evidence=self._redact(match.group(0)),
                    )
                )
        return findings

    def is_refusal(self, response: str) -> bool:
        normalized = response.lower()
        return any(marker in normalized for marker in self.refusal_markers)

    @staticmethod
    def _redact(value: str) -> str:
        if len(value) <= 4:
            return "*" * len(value)
        return f"{value[:2]}{'*' * (len(value) - 4)}{value[-2:]}"

