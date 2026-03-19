# Interview Checklist

Use this checklist to decide whether the user's answers are complete enough to write the baseline docs.
If the repo is already bootstrapped and the user wants the next feature wave, combine this with `references/expansion-mode.md` and ask only for the delta.
Preferred interaction style: before the first substantive product question, first handle companion-skill guidance and resolve the install decision, then review the product/reference context, then in a separate prompt recommend `Plan` mode if the user wants selectable option lists, then in a separate prompt tell the user to say `continue` when ready; after that, ask one question at a time, give suggested options when useful, and always allow a free-form answer.
Before the first substantive product question, check whether the pinned companion skill set is installed and, if the user allows them, summarize all missing companion skills, ask whether to auto-install them before product analysis and documentation starts, use the helper installer flow by default, and then handle accepted installs one skill at a time.
Keep the printed manual commands aligned with the actual upstream repo paths.
For continuation runs, the stop condition is docs and queue refresh, not immediate implementation. Finish the interview only when you can update the harness docs and write the next exec-plans without guessing, then stop there.

## Identity

- project name
- one-line product definition
- primary user
- why this product exists

## Scope

- v1 goals
- explicit non-goals
- what must be demoable in v1
- which distinct user-visible features should each become their own spec or task slice

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
- a clear feature map for how many product specs and active tasks should be created
- an initial active task queue with deterministic checks
- a concrete test strategy with explicit promotion-blocking commands

If any of those still requires guessing, keep asking.
