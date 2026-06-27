#!/usr/bin/env python3
"""Validate the BrightBlitz AI Slop QA skill package.

This is a deterministic smoke validator for release packaging. It intentionally
uses only the Python standard library so a fresh clone can run it before
publishing or installing the skill into a Hermes profile.
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
    ROOT / "README.md",
    ROOT / "CHANGELOG.md",
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
    "prose-vague-claim.md": {
        "decision": "fix-first",
        "confidence": "high",
        "predicted_terms": ["vague importance", "unsupported", "business filler"],
        "required_terms": ["vague", "unsupported", "business filler", "specific evidence"],
    },
    "code-swallowed-error.md": {
        "decision": "reject",
        "confidence": "high",
        "predicted_terms": ["swallowed failure", "success signal"],
        "required_terms": ["swallowed failure", "success", "failure signal"],
    },
    "automation-missing-failure-mode.md": {
        "decision": "fix-first",
        "confidence": "high",
        "predicted_terms": ["missing failure mode", "safe stop", "audit trail"],
        "required_terms": ["failure mode", "retry", "audit trail", "ownership"],
    },
    "agent-unverified-self-report.md": {
        "decision": "fix-first",
        "confidence": "low",
        "predicted_terms": ["self-report", "reviewable handle"],
        "required_terms": ["self-reported", "pr", "commit", "test log", "reviewable"],
    },
    "clean-pass-case.md": {
        "decision": "pass",
        "confidence": "high",
        "predicted_terms": ["clear request", "reviewable artifact", "evidence and limits"],
        "required_terms": ["success condition", "reviewable artifact", "evidence", "no blocker"],
    },
}
FORBIDDEN_PUBLIC_REFS = [
    "/Users/",
    "carmen-clawd",
    "Carmen-only",
    "local documents",
    "local document",
    "local workspace",
]
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9._-]{20,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9._=-]{20,}", re.IGNORECASE),
    re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\"]?[A-Za-z0-9._=-]{12,}"),
]
DENIED_PATH_PARTS = {"node_modules", "reference-clones", "vendor", ".husky"}
DENIED_FILENAMES = {
    ".gitmodules",
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "requirements.txt",
    "poetry.lock",
    "Pipfile",
    "Pipfile.lock",
}
DENIED_EXECUTABLE_SCRIPT_NAMES = {"install.sh", "setup.sh", "postinstall.sh", "bootstrap.sh"}
TEXT_SUFFIXES = {".md", ".py", ".toml", ".txt", ".yaml", ".yml", ".json", ".csv", ".sh"}


def fail(message: str) -> None:
    raise AssertionError(message)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Lightweight frontmatter key check, not a full YAML parser."""
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
            if key.strip() in fm:
                fail(f"Duplicate top-level frontmatter key: {key.strip()}")
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
        swallowed_failure = bool(
            re.search(r"except\s*(exception)?[^:]*:\s*\n\s*pass\b", lowered)
            or re.search(r"except\s*:\s*pass\b", lowered)
            or ("except" in lowered and "return true" in lowered and ("pass" in lowered or "log" in lowered))
        )
        if swallowed_failure:
            decision = "reject"
            findings.extend(["swallowed failure", "success signal can be false"])

    elif artifact_type == "automation":
        has_failure_policy = all(term in lowered for term in ("failure", "owner")) or all(
            term in lowered for term in ("error", "alert")
        )
        has_safe_stop = "retry" in lowered or "safe stop" in lowered or "pause" in lowered
        has_audit = "audit" in lowered or "log" in lowered or "trace" in lowered
        if not (has_failure_policy and has_safe_stop and has_audit):
            decision = "fix-first"
            findings.extend(["missing failure mode", "missing retry or safe stop", "missing audit trail"])

    elif artifact_type == "agent-output":
        claims_done = any(term in lowered for term in ("done", "fixed", "ready", "all tests pass", "completed"))
        has_reviewable_handle = any(term in lowered for term in ("https://", "pr #", "pull request", "commit", "diff", "test log"))
        if claims_done and not has_reviewable_handle:
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


def validate_source_handling() -> None:
    denied_paths = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if ".git" in rel.parts or "__pycache__" in rel.parts:
            continue
        if any(part in DENIED_PATH_PARTS for part in rel.parts):
            denied_paths.append(str(rel))
        if path.name in DENIED_FILENAMES:
            denied_paths.append(str(rel))
        if path.name in DENIED_EXECUTABLE_SCRIPT_NAMES:
            denied_paths.append(str(rel))
    if denied_paths:
        fail("Denied vendored/dependency/hook artifact found: " + ", ".join(sorted(denied_paths)))


def looks_text_like(path: Path) -> bool:
    if path.suffix in TEXT_SUFFIXES:
        return True
    if path.suffix:
        return False
    try:
        data = path.read_bytes()[:4096]
    except OSError:
        return False
    return b"\0" not in data


def iter_public_text_files() -> list[Path]:
    ignored_parts = {".git", "__pycache__", ".pytest_cache"}
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path != Path(__file__).resolve()
        and looks_text_like(path)
        and not any(part in ignored_parts for part in path.parts)
    )


def validate_public_text() -> int:
    scanned = 0
    for path in iter_public_text_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(ROOT)
        scanned += 1
        if "\u2014" in text or "\u2013" in text:
            fail(f"Non-ASCII dash found in {rel}")
        for forbidden in FORBIDDEN_PUBLIC_REFS:
            if forbidden.lower() in text.lower():
                fail(f"Forbidden local reference {forbidden!r} found in {rel}")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail(f"Secret-like pattern found in {rel}")
    return scanned


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
        if expected_decision != expected["decision"] or expected_confidence != expected["confidence"]:
            fail(f"Fixture metadata mismatch in {filename}")
        actual_decision, actual_confidence, findings = predict_fixture(input_text, artifact_type)
        if actual_decision != expected["decision"] or actual_confidence != expected["confidence"]:
            fail(
                f"Fixture {filename} expected {(expected['decision'], expected['confidence'])} but validator predicted "
                f"{(actual_decision, actual_confidence)} with findings {findings}"
            )
        findings_blob = "\n".join(findings).lower()
        for term in expected["predicted_terms"]:
            if term.lower() not in findings_blob:
                fail(f"Fixture {filename} prediction missing expected finding term: {term}")
        required = extract_section(text, "Required findings")
        if not required.strip().startswith("-"):
            fail(f"Fixture {filename} must include bullet required findings")
        required_blob = required.lower()
        for term in expected["required_terms"]:
            if term.lower() not in required_blob:
                fail(f"Fixture {filename} required findings missing term: {term}")


def main() -> int:
    validate_required_files()
    validate_frontmatter()
    validate_source_handling()
    scanned = validate_public_text()
    validate_fixtures()
    print("OK: skill package smoke validation passed")
    print(f"OK: scanned {scanned} public text files for local references, secret-like values, and non-ASCII dashes")
    print(f"OK: validated {len(EXPECTED_FIXTURES)} smoke fixtures")
    print("OK: source-handling deny checks passed")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
