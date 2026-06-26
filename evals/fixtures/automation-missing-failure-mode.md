# Fixture: Automation Missing Failure Mode

## Artifact type

automation

## Input

Trigger: new form submission.
Action: send the lead to the CRM and notify sales.
Success: the lead appears in the CRM.

## Expected decision

fix-first

## Expected confidence

high

## Required findings

- Missing failure mode for CRM API errors.
- Missing retry or safe stop behavior.
- Missing audit trail or alerting path.
- Required fix: define failure handling, ownership, and verification.
