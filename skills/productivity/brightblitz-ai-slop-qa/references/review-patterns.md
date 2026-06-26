# AI Slop Review Patterns

Use this support file when the main skill says to run a detailed pass. These lists are intentionally outside `SKILL.md` so the main skill stays readable and rollout-safe.

## Prose slop patterns

Check for:

- Throat-clearing: "Here's the thing," "It turns out," "The real issue is," "Let me be clear."
- Formulaic pivots: "Not X, but Y," "X is not the problem, Y is," "The question is not X."
- Emphasis crutches: "Full stop," "Let that sink in," "Make no mistake," "This matters because."
- Vague importance claims: "the stakes are high," "the implications are significant," "this is transformative."
- Business filler: "navigate," "unlock," "game-changer," "landscape," "deep dive," "moving forward."
- Meta-commentary: "In this section," "as we will see," "let me walk you through."
- False agency: inanimate objects doing human work, such as "the data tells us" or "the strategy unlocks growth."
- Passive voice that hides the actor.
- Uniform rhythm: same sentence length, repeated transitions, stacked three-item lists, punchy one-line endings.
- Em dashes, which BrightBlitz standards prohibit.

Fix by naming the actor, cutting setup, replacing vague claims with evidence, using plain language, varying sentence length, keeping the reader or client as the focus, and adding a clear next step.

## BrightBlitz communication patterns

For external or client-facing work, check that the artifact:

- Shows empathy before authority.
- Frames the client as the hero and BrightBlitz as the guide.
- Addresses the external problem and the internal frustration.
- Uses active voice by default.
- Avoids unsupported superlatives, guaranteed outcomes, and vague benefit claims.
- Includes a clear CTA or review decision.
- Removes secrets, private configuration, and internal-only notes.

Flag compliance-sensitive claims before polishing.

## Code slop patterns

Run the project's normal verification first when available. Then inspect for:

- Swallowed failures: empty catch blocks, catch-and-log-only handling, bare `except`, ignored return errors, or silent recovery that loses the cause.
- Hallucinated dependencies: imports not in manifests, packages that do not exist, wrong module paths, or invented APIs.
- Leftover scaffolding: TODO stubs, fake sample logic, debug prints, unreachable code, or empty functions.
- Unsafe shortcuts: broad exception handling, mutable defaults, unsafe eval, shell execution with untrusted input, or type assertions that hide real uncertainty.
- Hardcoded config: environment URLs, project IDs, tokens, paths, credentials, webhooks, or client-specific values in code.
- Over-abstraction: thin wrappers, generic names, needless factories, or repeated pass-through functions.
- Narrative comments: comments that explain the agent's plan or restate obvious code instead of documenting real constraints.
- Duplicate or unused imports.
- Architecture drift: ownership boundaries changed, direct data access from the wrong layer, or unapproved cross-system coupling.
- Missing tests for changed behavior.

## Automation slop patterns

Check whether the workflow has:

- Trigger, actions, branches, failure modes, and success criteria.
- Validated inputs and endpoints.
- Secure secret handling.
- Rate awareness, bounded retries, and idempotency where needed.
- Audit trail and enough logging to debug failures.
- Safe fallback or stop condition.
- Clear ownership and handoff.
- Approval status for production, client-facing, infrastructure, scheduled, or external-communication changes.

A workflow that works only in the happy path is not ready.

## Agent-output patterns

For agent or contractor outputs:

- Compare against the original request.
- Verify files, links, branches, commits, PRs, test logs, or Drive artifacts when possible.
- Treat self-reported command output as reported, not verified, until checked.
- Distinguish local paths from reviewable Drive or GitHub links.
- Check for missing sections, placeholders, wrong audience, or unsupported claims.
- Require specialist review where the domain requires it.
