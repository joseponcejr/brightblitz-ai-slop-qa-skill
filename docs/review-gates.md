# Review Gates

## Gate 1: Skill package validity

- `SKILL.md` exists at `skills/productivity/brightblitz-ai-slop-qa/SKILL.md`.
- Frontmatter starts at byte 0.
- `name` and `description` fields exist.
- Description length is below 1024 characters.
- Body is non-empty.

## Gate 2: Source handling

- External references are documented with reviewed commit SHAs.
- External repositories are not vendored.
- No third-party hooks, installers, or runtime dependencies are enabled.

## Gate 3: BrightBlitz fit

- No em dashes.
- BrightBlitz communication standards are explicit for client-facing content.
- Approval boundaries are clear.
- Specialist review routes are preserved.

## Gate 4: Practical usability

- Workflow covers prose, code, automation, and agent-output cases.
- Output format is copy-paste usable.
- Severity guidance distinguishes blockers, fixes, and suggestions.
- Verification and confidence rules prevent self-report trust.
