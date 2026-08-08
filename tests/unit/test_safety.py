from llm_quality_harness.safety import SafetyScanner


def scanner() -> SafetyScanner:
    return SafetyScanner(
        {
            "safety": {
                "injection_patterns": ["ignore previous instructions"],
                "pii_patterns": [r"\b\d{3}-\d{2}-\d{4}\b"],
                "refusal_markers": ["cannot assist"],
            }
        }
    )


def test_scans_injection_and_redacts_pii() -> None:
    findings = scanner().scan("Ignore previous instructions", "ID 123-45-6789")
    assert [finding.code for finding in findings] == ["PROMPT_INJECTION", "PII_LEAKAGE"]
    assert findings[1].evidence != "123-45-6789"


def test_detects_refusal() -> None:
    assert scanner().is_refusal("I cannot assist with that request")
    assert not scanner().is_refusal("Here is the answer")

