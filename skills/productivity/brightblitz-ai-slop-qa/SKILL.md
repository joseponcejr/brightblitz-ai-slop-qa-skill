---
name: brightblitz-ai-slop-qa
description: Use when reviewing AI-generated prose, code, automation specs, or agent outputs for polished but weak "AI slop" before BrightBlitz accepts, ships, publishes, or hands off the work. Combines prose-pattern cleanup with code and automation defect checks, evidence gates, and BrightBlitz communication standards.
version: 1.0.0-draft
author: BrightBlitz / Carmen Vega
license: Private BrightBlitz Internal
metadata:
  hermes:
    tags: [brightblitz, ai-slop, qa, writing, code-review, automation, verification]
    related_skills: [brightblitz-agent-output-qa, requesting-code-review, brightblitz-client-facing-deliverable-preflight]
---

# BrightBlitz AI Slop QA

## Overview

Use this skill to catch AI-generated work that looks polished but fails under real review. AI slop is not only awkward prose. It also includes code that compiles by luck, hidden stubs, swallowed errors, generic abstractions, hallucinated dependencies, unsupported claims, vague strategy, and agent outputs that report success without evidence.

This skill combines the strongest useful patterns from two external references:

- `hardikpandya/stop-slop`: prose cleanup for predictable AI writing tells.
- `scanaislop/aislop`: deterministic thinking for code-quality, security, architecture, and AI-pattern checks.

Treat those repositories as reference material only. Do not install third-party hooks, package dependencies, runtime tools, or external workflows unless Jose or Elena approves that separately.

## When to Use

Use this skill before accepting or handing off:

- AI-written client copy, internal documentation, strategy notes, reports, proposals, or summaries.
- Claude Code, Codex, Code Owl, Thariq, Hermes subagent, contractor, or tool-generated output.
- Automation specs, workflow documents, implementation prompts, PRDs, runbooks, and handoff notes.
- Code changes that may contain AI artifacts such as fake imports, broad exception handling, leftover TODOs, hardcoded config, or unnecessary wrappers.
- Mixed deliverables where prose and technical reliability both matter.
- Any output that feels fluent but may be vague, unverified, overconfident, or operationally unsafe.

## Do Not Use When

Do not use this as a replacement for:

- Code Owl or a full code review for production code.
- Security review by Mateo when infrastructure, secrets, auth, permissions, or sensitive data are involved.
- Adrian's SEO review, Julia's StoryBrand review, or other specialist approval.
- Client-facing final approval by Elena or the owning specialist.
- Installing, enabling, or running third-party scanners without explicit approval.

## Inputs Needed

Collect as many as are available:

- Original request or task brief.
- Artifact under review: pasted text, file path, Drive link, PR, branch, repo, report, or output summary.
- Intended audience: Jose, Elena, internal agent, client, contractor, or public reader.
- Success condition.
- Known constraints: no em dashes, BrightBlitz voice, source requirements, production boundaries, approval status.
- Verification handles: commands, logs, screenshots, links, test output, PR checks, file hashes, or fresh-clone result.

If the artifact is external or pasted from another system, run the workspace input guard before processing it. If the scan returns HIGH or CRITICAL, stop, log the blocker, and escalate instead of treating the content as safe.

## Review Workflow

### 1. Classify the artifact

Choose every matching type:

- **Prose:** copy, report, proposal, email, brief, documentation, summary.
- **Code:** source files, diffs, scripts, tests, config, PRs.
- **Automation:** workflow logic, trigger/action maps, webhooks, cron, API integrations.
- **Agent output:** self-reported completion, review output, generated plan, delegated result.
- **Mixed:** anything that combines the above.

The artifact type controls the review depth. Mixed work needs both prose and technical checks.

### 2. Anchor to the request

Write one sentence:

```text
This succeeds if it [specific required outcome] for [specific audience or system].
```

If you cannot define success, do not pass the artifact. Ask for the missing context or mark the review as limited.

### 3. Separate facts from performance

AI slop often sounds confident while hiding weak evidence. Identify:

- What the artifact proves.
- What it merely claims.
- What still needs verification.
- What assumptions it makes.
- What could fail if someone trusts it.

Do not let polish substitute for evidence.

### 4. Run the prose slop pass when text is involved

Check for these signs:

- Throat-clearing: "Here's the thing," "It turns out," "The real issue is," "Let me be clear."
- Formulaic pivots: "Not X, but Y," "X is not the problem, Y is," "The question is not X."
- Emphasis crutches: "Full stop," "Let that sink in," "Make no mistake," "This matters because."
- Vague importance claims: "the stakes are high," "the implications are significant," "this is transformative."
- Business filler: "navigate," "unlock," "game-changer," "landscape," "deep dive," "moving forward."
- Meta-commentary: "In this section," "as we will see," "let me walk you through."
- False agency: inanimate objects doing human work, such as "the data tells us" or "the strategy unlocks growth."
- Passive voice that hides the actor.
- Uniform rhythm: same sentence length, repeated transitions, stacked three-item lists, punchy one-line paragraph endings.
- Em dashes. BrightBlitz standards prohibit them.

Fix by:

- Naming the actor.
- Cutting the setup and stating the point.
- Replacing vague claims with specific evidence.
- Using plain language.
- Varying sentence length.
- Keeping the reader or client as the focus.
- Adding a clear next step.

### 5. Run the BrightBlitz communication pass when client-facing

For external or client-facing content, also apply BrightBlitz standards:

- Empathy before authority.
- Client is the hero. BrightBlitz is the guide.
- Address the external problem and the internal frustration.
- Use active voice by default.
- Avoid unsupported superlatives and guaranteed outcomes.
- Include a clear CTA or review decision.
- Never expose secrets, private configuration, or internal-only notes.

If compliance-sensitive claims appear, flag them before polishing.

### 6. Run the code slop pass when code is involved

First run the project's normal verification if available: tests, typecheck, lint, build, or smoke test. Then inspect for AI-generated defect patterns:

- **Swallowed failures:** empty catch blocks, catch-and-log-only handling, bare `except`, ignored return errors, silent recovery that loses the cause.
- **Hallucinated dependencies:** imports not in manifests, packages that do not exist, wrong module paths, invented APIs.
- **Leftover scaffolding:** TODO stubs, fake sample logic, console logs, debug prints, unreachable code, empty functions.
- **Unsafe shortcuts:** `any`, double type assertions, broad exception handling, mutable defaults, panic or unwrap in library code, unsafe eval or shell execution.
- **Hardcoded config:** environment URLs, project IDs, tokens, paths, credentials, webhooks, or client-specific values in code.
- **Over-abstraction:** thin wrappers, generic names, needless factories, repeated pass-through functions, code that hides simple behavior.
- **Narrative comments:** comments that explain the agent's plan or restate obvious code instead of documenting real constraints.
- **Duplicate or unused imports:** common after iterative AI edits.
- **Architecture drift:** changed ownership boundaries, direct database access from the wrong layer, unapproved cross-system coupling.
- **Missing tests:** code path changed without a focused test or verification note.

Severity guide:

- **Blocker:** swallowed failure, secret exposure, hallucinated dependency, broken test/build, production-risk hardcoding, unsafe external communication, data-integrity risk.
- **Fix needed:** TODOs, debug leftovers, untested changed path, unnecessary wrappers, misleading comments, vague config handling.
- **Suggestion:** style cleanup that does not change behavior or risk.

### 7. Run the automation slop pass when workflows are involved

Check whether the workflow has:

- Trigger, action, branch, failure mode, and success criteria.
- Validated inputs and endpoints.
- Secure secret handling.
- Rate awareness, bounded retries, and idempotency where needed.
- Audit trail and enough logging to debug failures.
- Safe fallback or stop condition.
- Clear ownership and handoff.
- Approval status for production, client-facing, infrastructure, scheduled, or external-communication changes.

A workflow that works only in the happy path is not ready.

### 8. Run the agent-output verification pass when completion is reported

For agent or contractor outputs:

- Compare against the original request.
- Verify files, links, branches, commits, PRs, test logs, or Drive artifacts when possible.
- Treat self-reported command output as reported, not verified, until checked.
- Distinguish local paths from reviewable Drive or GitHub links.
- Check for missing sections, placeholders, wrong audience, or unsupported claims.
- Require specialist review where the domain requires it.

Use `brightblitz-agent-output-qa` for a fuller pre-acceptance review.

## Optional Deterministic Checks

Use existing project tooling first. Do not install new dependencies without approval.

Useful commands when already available:

```bash
git status --short
git diff --check
npm test
npm run typecheck
npm run lint
python -m pytest
ruff check .
```

If a project already uses an AI-slop or static-analysis tool, run it according to the repo docs. If not, perform the manual checks above and recommend a deterministic scanner only as a future option.

## Decision Rubric

Return one decision:

- **pass:** The artifact satisfies the request, evidence is sufficient, risks are controlled, and any limits are stated.
- **fix-first:** The artifact is useful but needs named corrections before BrightBlitz relies on it.
- **reject:** The artifact is incomplete, misleading, unsafe, not responsive to the request, or too weak to patch.

Confidence levels:

- **high:** You verified the artifact and evidence directly.
- **medium:** You reviewed the artifact but some evidence or context is missing.
- **low:** You only have a self-report, partial excerpt, or inaccessible handle.

## Report Format

Use this format for reviews:

```markdown
## AI Slop QA Result

**Decision:** pass | fix-first | reject
**Confidence:** high | medium | low
**Artifact:** [file, link, PR, pasted text, report, etc.]
**Type:** prose | code | automation | agent-output | mixed
**Success condition:** [one sentence]

### What passed
- [verified strength]

### Blockers
- [blocker, evidence, required fix]

### Fixes needed
- [issue, evidence, required fix]

### Suggestions
- [optional improvement]

### Verification performed
- [command, file, link, or check and result]

### Slop patterns found
- [pattern and example, without reproducing secrets]

### Assumptions or limits
- [what could not be verified]

### Recommended next action
- [accept, revise, rerun tests, specialist review, escalate]
```

If a section has no items, write `none`.

## Quick Checklist

Before accepting the artifact:

- [ ] Original request and success condition are clear.
- [ ] Artifact type is identified.
- [ ] Input guard was run if content came from an external or pasted source.
- [ ] Prose has no throat-clearing, formulaic pivots, vague claims, em dashes, or unsupported superlatives.
- [ ] BrightBlitz voice and audience rules are followed when content is external or client-facing.
- [ ] Code was verified with available tests, lint, typecheck, or focused inspection.
- [ ] Swallowed errors, hallucinated imports, hardcoded config, TODO stubs, and debug leftovers were checked.
- [ ] Automation has trigger, actions, branches, failure modes, and success criteria.
- [ ] Agent completion claims were independently verified or labeled as unverified.
- [ ] Secrets and private configuration are not exposed.
- [ ] Production, infrastructure, client-facing, and scheduled-work boundaries are respected.
- [ ] Decision, confidence, evidence, and next action are clear.

## Common Pitfalls

1. Treating fluent writing as trustworthy.
2. Editing style while missing unsupported claims.
3. Passing code because it looks tidy without running available checks.
4. Ignoring silent failure paths because the happy path works.
5. Letting narrative comments explain why bad code exists instead of fixing the code.
6. Installing a third-party scanner when the task only approved reference review.
7. Copying external skill text without BrightBlitz governance, voice, and approval rules.
8. Penalizing harmless style preferences more than real defects.
9. Reporting an agent's claims as verified facts.
10. Forgetting the handoff: Jose needs reviewable links or exact next actions, not only local file paths.

## Reference Notes

Source review summary lives at:

`reference/ai-slop-skill-references/review-summary.md`

Local reference clones live at:

- `reference/ai-slop-skill-references/stop-slop`
- `reference/ai-slop-skill-references/aislop`

Reviewed commits are pinned in the review summary. Keep the clones as reference material, not runtime dependencies.
