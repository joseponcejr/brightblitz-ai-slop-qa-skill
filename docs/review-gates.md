# Review Gates

## Gate 1: Skill package validity

- `SKILL.md` exists at `skills/productivity/brightblitz-ai-slop-qa/SKILL.md`.
- Frontmatter starts at byte 0.
- `name` and `description` fields exist.
- Description length is below 1024 characters.
- Body is non-empty.
- Main support files exist under the skill package: `references/review-patterns.md` and `references/maintainer-notes.md`.

## Gate 2: Source handling

- External references are documented with reviewed commit SHAs.
- External repositories are not vendored.
- No third-party hooks, installers, or runtime dependencies are enabled.
- SKILL.md points to package-local or repo-local docs, not machine-specific reference paths.

## Gate 3: BrightBlitz fit

- No em dashes.
- BrightBlitz communication standards are explicit for client-facing content.
- Approval boundaries are clear.
- Specialist review routes are preserved and phrased as routing helpers when installed.

## Gate 4: Practical usability

- Workflow covers prose, code, automation, and agent-output cases.
- Output format is copy-paste usable.
- Severity guidance distinguishes blockers, fixes, and suggestions.
- Verification and confidence rules prevent self-report trust.
- Pattern details use progressive disclosure through support files.

## Gate 5: Eval fixture coverage

- `evals/fixtures/prose-vague-claim.md` expects a prose fix-first decision.
- `evals/fixtures/code-swallowed-error.md` expects a code reject decision for swallowed failure.
- `evals/fixtures/automation-missing-failure-mode.md` expects an automation fix-first decision.
- `evals/fixtures/agent-unverified-self-report.md` expects an agent-output fix-first decision.
- `evals/fixtures/clean-pass-case.md` expects a pass decision.
- Each fixture states expected confidence and required findings.
