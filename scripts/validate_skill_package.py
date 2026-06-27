#!/usr/bin/env python3
"""Validate the BrightBlitz AI Slop QA skill package.

This script intentionally uses only the Python standard library so a fresh clone
can run it before publishing or installing the skill into a Hermes profile.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "productivity" / "brightblitz-ai-slop-qa" / "SKILL.md"
FIXTURE_DIR = ROOT / "evals" / "fixtures"
REQUIRED_FILES = [
    SKILL,
    ROOT / "skills" / "productivity" / "brightblitz-ai-slop-qa" / "references" / "review-patterns.md",
    ROOT / "skills" / "productivity" / "brightblitz-ai-slop-qa" / "references" / "maintainer-notes.md",
    ROOT / "docs" / "prd.md",
    ROOT / "docs" / "skill-spec.md",
    ROOT / "docs" / "workflow-map.md",
    ROOT / "docs" / "review-gates.md",
    ROOT / "docs" / "source-reference-review.md",
    ROOT / "examples" / "ai-slop-qa-report-example.md",
]
EXPECTED_FIXTURES = {
    "prose-vague-claim.md": ("fix-first", "high"),
    "code-swallowed-error.md": ("reject", "high"),
    "automation-missing-failure-mode.md": ("fix-first", "high"),
    "agent-unverified-self-report.md": ("fix-first", "low"),
    "clean-pass-case.md": ("pass", "high"),
}
FORBIDDEN_PUBLIC_REFS = [
    "/Users/",
    "carmen-clawd",
    "Carmen-only",
    "local documents",
    "local document",
    "local workspace",
]
TEXT_SUFFIXES = {".md", ".py", ".toml", ".txt"}


def fail(message: str) -> None:
    raise AssertionError(message)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        fail("SKILL.md must start with frontmatter at byte 0")
    try:
        _, fm_text, body = text.split("---\n", 2)
    except ValueError as exc:
        raise AssertionError("SKILL.md frontmatter must close with ---") from exc
    fm: dict[str, str] = {}
    for raw_line in fm_text.splitlines():
        if not raw_line.strip() or raw_line.startswith("  "):
            continue
        if ":" in raw_line:
            key, value = raw_line.split(":", 1)
            fm[key.strip()] = value.strip().strip('"')
    return fm, body.strip()


def extract_section(text: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\s*$"
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match:
        fail(f"Missing fixture section: {heading}")
    start = match.end()
    next_heading = re.search(r"^## ", text[start:], flags=re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(text)
    return text[start:end].strip()


def predict_fixture(input_text: str, artifact_type: str) -> tuple[str, str, list[str]]:
    lowered = input_text.lower()
    findings: list[str] = []
    decision = "pass"
    confidence = "high"

    if artifact_type == "prose":
        slop_terms = ["revolutionary", "unlocks", "next-level", "transforming", "game-changer", "moving forward"]
        if any(term in lowered for term in slop_terms):
            decision = "fix-first"
            findings.extend(["vague importance claims", "unsupported benefit language", "business filler"])

    elif artifact_type == "code":
        if "except exception" in lowered and "pass" in lowered:
            decision = "reject"
            findings.extend(["swallowed failure", "success signal can be false"])

    elif artifact_type == "automation":
        missing_failure = "failure" not in lowered and "error" not in lowered and "retry" not in lowered
        if missing_failure:
            decision = "fix-first"
            findings.extend(["missing failure mode", "missing retry or safe stop", "missing audit trail"])

    elif artifact_type == "agent-output":
        if "all tests pass" in lowered and ("my machine" in lowered or "local" in lowered):
            decision = "fix-first"
            confidence = "low"
            findings.extend(["self-report not verified", "missing reviewable handle"])

    elif artifact_type == "mixed":
        if "evidence:" in lowered and "no secrets" in lowered and "not applicable" in lowered:
            decision = "pass"
            findings.extend(["clear request", "reviewable artifact", "evidence and limits stated"])
        else:
            decision = "fix-first"

    return decision, confidence, findings


def validate_frontmatter() -> None:
    text = SKILL.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    for key in ("name", "description", "version", "author", "license"):
        if not fm.get(key):
            fail(f"Missing frontmatter key: {key}")
    if fm["name"] != "brightblitz-ai-slop-qa":
        fail("Unexpected skill name")
    if len(fm["description"]) > 1024:
        fail("Description exceeds Hermes limit")
    if not body:
        fail("SKILL.md body must be non-empty")


def validate_required_files() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.exists()]
    if missing:
        fail("Missing required files: " + ", ".join(missing))


def iter_public_text_files() -> list[Path]:
    ignored_parts = {".git", "__pycache__", ".pytest_cache"}
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path != Path(__file__).resolve()
        and path.suffix in TEXT_SUFFIXES
        and not any(part in ignored_parts for part in path.parts)
    )


def validate_public_text() -> None:
    for path in iter_public_text_files():
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        if "\u2014" in text or "\u2013" in text:
            fail(f"Non-ASCII dash found in {rel}")
        for forbidden in FORBIDDEN_PUBLIC_REFS:
            if forbidden.lower() in text.lower():
                fail(f"Forbidden local reference {forbidden!r} found in {rel}")


def validate_fixtures() -> None:
    for filename, expected in EXPECTED_FIXTURES.items():
        path = FIXTURE_DIR / filename
        if not path.exists():
            fail(f"Missing fixture: {filename}")
        text = path.read_text(encoding="utf-8")
        artifact_type = extract_section(text, "Artifact type").strip().splitlines()[0]
        input_text = extract_section(text, "Input")
        expected_decision = extract_section(text, "Expected decision").strip().splitlines()[0]
        expected_confidence = extract_section(text, "Expected confidence").strip().splitlines()[0]
        if (expected_decision, expected_confidence) != expected:
            fail(f"Fixture metadata mismatch in {filename}")
        actual_decision, actual_confidence, findings = predict_fixture(input_text, artifact_type)
        if (actual_decision, actual_confidence) != expected:
            fail(
                f"Fixture {filename} expected {expected} but validator predicted "
                f"{(actual_decision, actual_confidence)} with findings {findings}"
            )
        required = extract_section(text, "Required findings")
        if not required.strip().startswith("-"):
            fail(f"Fixture {filename} must include bullet required findings")


def main() -> int:
    checks = [
        validate_required_files,
        validate_frontmatter,
        validate_public_text,
        validate_fixtures,
    ]
    for check in checks:
        check()
    print("OK: skill package validation passed")
    print(f"OK: validated {len(EXPECTED_FIXTURES)} smoke fixtures")
    print("OK: no forbidden local document or machine-path references found")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
