# Interview Checklist

Use this checklist to decide whether the user's answers are complete enough to write the baseline docs.
If the repo is already bootstrapped and the user wants the next feature wave, combine this with `references/expansion-mode.md` and ask only for the delta.
Preferred interaction style: at interview start, recommend `Plan` mode if the user wants selectable option lists; then ask one question at a time, give suggested options when useful, and always allow a free-form answer.

## Identity

- project name
- one-line product definition
- primary user
- why this product exists

## Scope

- v1 goals
- explicit non-goals
- what must be demoable in v1

## Domain model

- primary entities
- ownership rules
- key relationships
- any attachment/document/media/search/share concepts

## User-facing shape

- routes or screens
- core flows
- required read-only or admin surfaces
- what absolutely must be test-covered end-to-end
- which external-resource flows must be test-covered end-to-end before promotion

## Technical basis

- storage/runtime assumptions
- external dependencies or APIs
- secrets/config shape
- single-user vs multi-user expectations
- whether any user-visible feature depends on outside resources such as AI or third-party services

## Quality bar

- deterministic commands
- unit-test expectations
- integration-test expectations if any
- required E2E flows
- explicit E2E coverage for external-resource features before promotion
- promotion-blocking test gates
- what `npm run verify` is expected to prove
- reliability or security caveats that must be documented

## Ralph loop readiness

- initial task queue sequencing
- first vertical slice
- hardening/maintenance task
- operator expectations for `run-once` and unattended loop runs
- confirmation that failing required tests prevent promotion

## Stop Asking When

You can clearly write:

- `AGENTS.md`
- `ARCHITECTURE.md`
- the top-level docs
- at least one design doc
- at least one product spec
- an initial active task queue with deterministic checks
- a concrete test strategy with explicit promotion-blocking commands

If any of those still requires guessing, keep asking.
