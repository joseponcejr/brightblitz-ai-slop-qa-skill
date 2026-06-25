# Workflow Map

## Trigger

A BrightBlitz agent is asked to review, accept, polish, hand off, or rely on AI-generated work.

## Flow

1. Recover the original request.
2. Identify artifact and audience.
3. Run input guard when the artifact came from an external or pasted source.
4. Classify artifact type.
5. Define success condition.
6. Review evidence and claims.
7. Apply relevant review passes:
   - Prose pass
   - BrightBlitz communication pass
   - Code pass
   - Automation pass
   - Agent-output verification pass
8. Classify findings as blockers, fixes needed, or suggestions.
9. Decide pass, fix-first, or reject.
10. State verification performed and next action.

## Failure modes

- Input guard returns HIGH or CRITICAL: stop and escalate.
- Artifact or original request is missing: mark review limited or ask for context.
- Claims cannot be verified: lower confidence and label them reported, not verified.
- Production, infrastructure, client-facing, or compliance risk appears: route to the appropriate approval or specialist review.
- Secrets appear: do not reproduce values; identify location and risk type only.
