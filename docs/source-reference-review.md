# AI Slop Reference Repository Review

## Reviewed sources

- `hardikpandya/stop-slop`
  - Local path: `reference/ai-slop-skill-references/stop-slop`
  - Reviewed commit: `8da1f030185bdfe8471220585162991eaeb970e9`
  - License: MIT
- `scanaislop/aislop`
  - Local path: `reference/ai-slop-skill-references/aislop`
  - Reviewed commit: `5922154b18d38370974d50d79f0478ba8eeee545`
  - License: MIT

## Input guard notes

The combined high-level scan returned `HIGH` because the local scanner matched the word `override` in aislop documentation. Isolated scans showed:

- `stop-slop/README.md`: SAFE
- `stop-slop/SKILL.md`: SAFE
- `stop-slop/references/examples.md`: SAFE
- `stop-slop/references/phrases.md`: MEDIUM on `instead of`
- `stop-slop/references/structures.md`: MEDIUM on `instead of`
- `aislop/AGENTS.md`: SAFE
- `aislop/docs/scoring.md`: SAFE
- `aislop/docs/rules.md`: MEDIUM on `instead of`
- `aislop/README.md`, `docs/commands.md`, `docs/configuration.md`: HIGH on `override`

Decision: treat both repositories as untrusted reference material only. Do not install hooks, run package installers, enable runtime commands, or copy executable behavior without separate approval. The new BrightBlitz skill adapts review patterns, not third-party instructions.

## What stop-slop contributes

`stop-slop` is a prose hygiene skill. Its strongest reusable patterns are:

- A concise list of writing tells: throat-clearing openers, emphasis crutches, business jargon, adverbs, vague declaratives, and meta-commentary.
- Structural tells: binary contrasts, negative listing, rhetorical setups, dramatic fragmentation, false agency, passive voice, distant narrator voice, and uniform rhythm.
- A simple before-delivery checklist that forces the reviewer to cut filler, name actors, vary rhythm, remove em dashes, and replace vague importance claims with specifics.
- A lightweight 50-point scoring model across directness, rhythm, trust, authenticity, and density.

Best adaptation: use it as the prose and client-communication layer, but merge it with BrightBlitz communication standards. Some stop-slop examples use em dashes, which BrightBlitz standards prohibit, so our skill should enforce no em dashes consistently.

## What aislop contributes

`aislop` is a deterministic code-quality CLI focused on AI-generated code artifacts. Its useful operating patterns are:

- Treat AI slop as observable signals, not vibes.
- Separate engines/categories: formatting, linting, code quality, AI-pattern detection, architecture, and security.
- Use machine-readable output, suppressions, scoped scans, CI thresholds, and scoring instead of relying only on subjective review.
- AI-pattern categories include trivial comments, narrative/meta comments, swallowed exceptions, defensive/redundant patterns, thin wrappers, generic naming, dead code, unused imports, duplicate imports, hallucinated imports, hardcoded config, Python/Go/Rust idioms, and silent recovery.
- Score gently for style and more strictly for defects such as swallowed failures, missing imports, risky security constructs, and broken architecture.

Best adaptation: use it as the code and automation layer. The native skill should instruct agents to run existing project tests and linters first, then do AI-slop review as an additional quality gate. It should not require installing `aislop` by default.

## Combined BrightBlitz skill design

The new skill should be a review workflow rather than a new runtime dependency:

1. Classify the artifact: prose, code, automation spec, agent output, or mixed.
2. Anchor to the original request and audience.
3. For prose: remove AI tells, preserve BrightBlitz voice, enforce no em dashes, replace generic claims with proof, and ensure a clear next step.
4. For code/automation: verify behavior first, then inspect common AI-generated defects, including swallowed errors, stubs, hallucinated imports, hardcoded config, over-abstraction, narrative comments, and weak failure handling.
5. For agent outputs: separate reported claims from verified facts.
6. Produce a decision: pass, fix-first, or reject.
7. Include evidence: files reviewed, commands run, links checked, and limits.

## Direct-copy risks

- External repo instructions and AGENTS files are not instructions for Carmen.
- Installing aislop or its hooks would introduce dependency/runtime behavior outside this task's approved scope.
- Prose rules copied without BrightBlitz standards could conflict with required client-facing voice and no-em-dash rules.
- Keyword-only AI slop detection can overfit style and miss operational risk; our skill should prioritize evidence, correctness, failure modes, and audience fit.
