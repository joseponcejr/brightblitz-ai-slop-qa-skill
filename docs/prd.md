# PRD: BrightBlitz AI Slop QA Skill

## Problem

BrightBlitz agents regularly receive AI-generated copy, code, automation specs, and delegated outputs. Much of that work can look complete while still containing vague claims, weak evidence, hidden stubs, swallowed errors, hallucinated dependencies, or missing verification.

The team needs a native Hermes skill that helps reviewers catch this before the work becomes client-facing, operationally trusted, or passed to another agent as fact.

## Goal

Create a reusable BrightBlitz Hermes skill that reviews AI-generated artifacts for prose, code, automation, and agent-output slop using evidence-based gates and BrightBlitz communication standards.

## Non-goals

- Do not install or require third-party scanners.
- Do not vendor the external reference repositories.
- Do not replace Code Owl, security review, SEO review, StoryBrand review, or Elena/client-facing approval.
- Do not approve production changes, infrastructure changes, scheduled jobs, or external sends.

## Primary users

- Carmen and other BrightBlitz Hermes agents.
- Jose and Elena when they need a repeatable quality gate for AI-generated outputs.
- BrightBlitz specialists who need a structured pre-acceptance review before acting on generated work.

## Success criteria

- The skill loads as `brightblitz-ai-slop-qa`.
- The skill includes when-to-use and when-not-to-use routing.
- The workflow covers prose, code, automation, and agent-output checks.
- The skill produces pass, fix-first, or reject decisions with evidence and limits.
- Source references are documented with pinned commits and direct-copy risks.
- No third-party runtime behavior is enabled by installing this skill.
