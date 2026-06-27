# Maintainer Notes

## Scope

Keep `brightblitz-ai-slop-qa` positioned as pre-acceptance QA for AI-generated artifacts. It can flag quality, evidence, and safety problems, but it does not replace specialist review or approval gates.

## How to add new patterns

When a recurring slop pattern appears:

1. Add the pattern to `references/review-patterns.md` unless it changes the core workflow.
2. Add or update at least one fixture in `evals/fixtures/` that demonstrates the expected finding.
3. Keep the main `SKILL.md` focused on trigger, routing, workflow, severity, report format, and guardrails.
4. Update `docs/review-gates.md` if the new pattern changes release criteria.
5. Run the package validation script or equivalent checks before release.

The validator is a deterministic smoke test for package structure, forbidden public references, and fixture drift. It is not a reasoning-quality evaluator, and a green run does not replace human or Code Owl review when the skill behavior changes.

## What not to add

Do not add:

- One-off client details.
- Secrets, tokens, private configuration values, or webhook payloads.
- Third-party scanner setup steps unless Jose or Elena separately approves that runtime dependency.
- Long source excerpts copied from external repositories.
- New specialist review promises that the skill cannot verify.

## Related skill dependency rule

The related skills in frontmatter are routing helpers. Before broad rollout, verify each target BrightBlitz profile has those helpers installed or update the skill copy for that rollout to say "if available." Do not call a rollout complete from file copy alone.
