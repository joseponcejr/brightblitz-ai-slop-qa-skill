# Review AI Work for Unsupported Claims and Hidden Defects

Polished AI output can still leave you with unsupported claims, unfinished code, or a completion report that proves very little. You need to know what deserves correction before the work moves forward.

This BrightBlitz Hermes skill helps reviewers examine prose, code, automation specifications, and agent outputs for those weaknesses. It supplies review patterns and evidence gates for identifying issues and requesting corrections, rather than treating confident wording as proof of quality.

Start with three steps:

1. Open [the skill](skills/productivity/brightblitz-ai-slop-qa/SKILL.md) and identify the deliverable and review scope.
2. Apply the relevant prose, code, automation, or completion-evidence checks to the actual work.
3. Record supported findings and route the corrected deliverable through its required specialist or release review.

The skill is marked as a draft. It does not install the external reference tools, replace production code review, or authorize client sends, deployments, infrastructure changes, or scheduled automation changes.

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

Run the package smoke validator before publishing or installing the skill into another profile:

```bash
python scripts/validate_skill_package.py
```

Validated checks:

- Frontmatter starts at byte 0 and passes a lightweight required-key check.
- Required `name` and `description` fields are present.
- Description is below the Hermes limit.
- Body is non-empty.
- Public text files have no em dashes, en dashes, forbidden machine-local references, or secret-like values.
- Required source files, README, CHANGELOG, skill support files, docs, examples, and eval fixtures exist.
- Deny checks find no vendored source, package dependency manifests, hook directories, or installer scripts.
- Eval fixtures exist for prose, code, automation, agent-output, and clean/pass cases.
- The deterministic package smoke validator passes with all smoke fixtures.

Manual rollout checks:

- A target Hermes profile can load the copied skill after restart or reload.

## Approval boundary

This repo provides a review skill. It does not approve production deployments, client-facing sends, infrastructure changes, third-party scanner installation, or scheduled automation changes. Those still require the appropriate BrightBlitz approval path.
