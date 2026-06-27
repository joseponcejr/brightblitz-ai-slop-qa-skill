# BrightBlitz AI Slop QA Skill

BrightBlitz Hermes skill package for reviewing AI-generated prose, code, automation specs, and agent outputs before BrightBlitz accepts, ships, publishes, or hands off the work.

The skill catches polished but weak output: vague writing, unsupported claims, swallowed errors, hallucinated imports, hidden stubs, hardcoded config, over-abstraction, weak automation failure handling, and unverified agent completion reports.

## Skill

- Skill name: `brightblitz-ai-slop-qa`
- Category: `productivity`
- Main file: `skills/productivity/brightblitz-ai-slop-qa/SKILL.md`

## What it does

Use this skill before accepting or handing off:

- AI-written client copy, internal documentation, strategy notes, reports, proposals, or summaries.
- Claude Code, Codex, Code Owl, Thariq, Hermes subagent, contractor, or tool-generated output.
- Automation specs, workflow documents, implementation prompts, PRDs, runbooks, and handoff notes.
- Code changes that may contain AI artifacts such as fake imports, broad exception handling, TODO stubs, hardcoded config, or unnecessary wrappers.
- Mixed deliverables where prose and technical reliability both matter.

## Source references

This package adapts patterns from two external MIT-licensed repositories as reference material only:

- `hardikpandya/stop-slop`, reviewed at `8da1f030185bdfe8471220585162991eaeb970e9`
- `scanaislop/aislop`, reviewed at `5922154b18d38370974d50d79f0478ba8eeee545`

See `docs/source-reference-review.md` for the source review summary, input-guard notes, useful patterns, and direct-copy risks. The external repositories are not vendored here and no third-party hooks or package dependencies are enabled by this skill.

## Repository contents

```text
skills/productivity/brightblitz-ai-slop-qa/SKILL.md
skills/productivity/brightblitz-ai-slop-qa/references/review-patterns.md
skills/productivity/brightblitz-ai-slop-qa/references/maintainer-notes.md
docs/prd.md
docs/skill-spec.md
docs/workflow-map.md
docs/review-gates.md
docs/source-reference-review.md
evals/fixtures/prose-vague-claim.md
evals/fixtures/code-swallowed-error.md
evals/fixtures/automation-missing-failure-mode.md
evals/fixtures/agent-unverified-self-report.md
evals/fixtures/clean-pass-case.md
examples/ai-slop-qa-report-example.md
scripts/validate_skill_package.py
```

## Install into a Hermes profile

Copy the skill directory into the target profile:

```bash
mkdir -p ~/.hermes/profiles/<profile>/skills/productivity
cp -R skills/productivity/brightblitz-ai-slop-qa ~/.hermes/profiles/<profile>/skills/productivity/
hermes -p <profile> skills list --source local | grep brightblitz-ai-slop
```

Then restart or reload the target Hermes session so the skill loader sees the new skill.

This copies the runtime skill package only. Repository-root files such as `docs/`, `evals/`, `examples/`, and `scripts/` are maintainer and release-validation assets that remain in this source repository unless a rollout package explicitly includes them.

## Validation

Run the package validator before publishing or installing the skill into another profile:

```bash
python scripts/validate_skill_package.py
```

Validated checks:

- YAML frontmatter starts at byte 0 and parses.
- Required `name` and `description` fields are present.
- Description is below the Hermes limit.
- Body is non-empty.
- No em dashes or en dashes are present in skill, docs, examples, or eval fixtures.
- Eval fixtures exist for prose, code, automation, agent-output, and clean/pass cases.
- The deterministic package validator passes with all smoke fixtures.
- A target Hermes profile can load the copied skill after restart or reload.

## Approval boundary

This repo provides a review skill. It does not approve production deployments, client-facing sends, infrastructure changes, third-party scanner installation, or scheduled automation changes. Those still require the appropriate BrightBlitz approval path.
