from __future__ import annotations

import argparse
import re
from pathlib import Path

TEXT_SUFFIXES = {".py", ".js", ".ts", ".json", ".yaml", ".yml", ".md", ".html", ".css", ".toml"}
IGNORED_PARTS = {".git", ".venv", "node_modules", "playwright-report", "test-results"}
PATTERNS = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "aws-access-key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "github-token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "generic-secret": re.compile(
        r"(?i)(?:api[_-]?key|secret|password)\s*[:=]\s*['\"](?!example|placeholder|change-me)[^'\"]{12,}['\"]"
    ),
}


def scan(root: Path) -> list[str]:
    findings: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in IGNORED_PARTS for part in path.parts):
            continue
        if path.name == "secret_scan.py" and path.parent.name == "scripts":
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in PATTERNS.items():
            if pattern.search(content):
                findings.append(f"{name}: {path.relative_to(root)}")
    return findings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".", type=Path)
    args = parser.parse_args()
    findings = scan(args.root.resolve())
    if findings:
        print("SECRET SCAN: FAIL")
        print("\n".join(findings))
        raise SystemExit(1)
    print("SECRET SCAN: PASS (0 findings)")


if __name__ == "__main__":
    main()
