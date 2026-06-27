# Changelog

## 1.0.0-draft.3

- Added a standard-library package validator that checks skill frontmatter, support files, public-readiness text, and all smoke fixtures.
- Added the validation command to SKILL.md and README.md.
- Replaced machine-local handoff wording with public-safe reviewable artifact wording.
- Clarified repo-root maintainer assets, confidence rules for self-reported agent output, decision mapping, and validator limits after Code Owl review.

## 1.0.0-draft.2

- Patched Code Owl review follow-ups.
- Bumped skill frontmatter version to match the post-review package state.
- Clarified input guard handling as conditional when the workspace guard is available.
- Corrected the example report so unverified self-reported tests are listed as fixes needed, not blockers.
- Corrected the profile-specific install verification command to use the global `-p <profile>` flag before the `skills` subcommand.

## 1.0.0-draft.1

- Patched Thariq review recommendations.
- Moved long review pattern lists into package-local support files.
- Replaced machine-specific reference paths with repo/package documentation pointers.
- Added eval smoke-test fixtures for prose, code, automation, agent-output, and clean/pass cases.
- Clarified related skill routing as helper behavior when those skills are installed.
- Added maintainer notes for future pattern updates.

## 1.0.0-draft

- Initial BrightBlitz AI Slop QA skill package.
- Added source reference review for `stop-slop` and `aislop`.
- Added PRD, skill spec, workflow map, review gates, and example report.
