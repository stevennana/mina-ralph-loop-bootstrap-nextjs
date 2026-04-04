---
name: mina-ralph-loop-bootstrap-nextjs
description: Bootstrap or extend a new or early-stage Next.js App Router + TypeScript repository around a Ralph-style task-promotion loop. Use when Codex needs to ask the founder product and architecture questions, generate or update the repo-local markdown knowledge base, create the initial scaffold or the next feature wave, install or adapt Ralph loop scripts, and explain how to run one cycle or a longer unattended loop.
---

# Mina Ralph Loop Bootstrap Nextjs

Build the repository in this order:

1. gather intent until the markdown knowledge base can be written without guessing
2. generate the repo-local docs first
3. scaffold the Next.js TypeScript project to match those docs
4. install and adapt the Ralph loop scripts
5. validate the deterministic commands
6. hand back operator guidance

Use this skill for new repositories or very early repositories that still lack a stable docs tree, scaffold contract, and loop harness.
Also use it to extend a repo that was already bootstrapped by this skill when the current queue is complete and the founder wants the next feature wave defined.

## Read First

Read these references before asking questions or writing files:

- [references/harness-engineering.md](references/harness-engineering.md)
- [references/doc-baseline.md](references/doc-baseline.md)
- [references/interview-checklist.md](references/interview-checklist.md)
- [references/nextjs-ts-preset.md](references/nextjs-ts-preset.md)
- [references/expansion-mode.md](references/expansion-mode.md)
- [references/feature-slicing.md](references/feature-slicing.md)
- [references/doc-quality-loop.md](references/doc-quality-loop.md)
- [references/environment-blockers.md](references/environment-blockers.md)
- [references/runtime-startup.md](references/runtime-startup.md)
- [references/server-logging.md](references/server-logging.md)

Open templates and copied Ralph assets only when you need them:

- `assets/templates/root/`
- `assets/templates/docs/`
- `assets/templates/ralph/`

Use these scripts when bootstrapping:

- `scripts/render_docs.py`
- `scripts/install_ralph.py`
- `scripts/companion_skills.py`
- `scripts/finalize_bootstrap_state.py`

## Workflow

### 1. Ground the target repo

Inspect the target repository first.

- If the repo is empty, proceed with a fresh bootstrap.
- If the repo already has code, determine whether it is still early enough to be reshaped around the generated docs and Ralph scripts.
- If the repo already has the docs tree and Ralph loop installed, determine whether this is a continuation run for the next feature wave instead of a fresh bootstrap.
- Do not install the Ralph loop into a mature repo without first checking whether the existing layout, commands, and docs can support it cleanly.

For continuation runs:

- inspect `docs/exec-plans/active/`
- inspect `docs/exec-plans/completed/`
- inspect the current product specs and design docs
- identify what feature area or product expansion the founder wants next
- preserve completed plans as history rather than rewriting them

Before making implementation claims or writing replacement code, search the codebase first.
Do not assume a feature, helper, route, or test is missing just because the first search result was incomplete.

### 1b. Check companion skills before discovery

Before product analysis, before reviewing the user’s reference implementation in depth, before founder discovery, and before writing docs, check whether the pinned companion skill set is already installed under `~/.codex/skills`.
Use `python3 <skill>/scripts/companion_skills.py status` as the source of truth for that pinned companion-skill set.

If the user allows companion skills:

- treat this as a startup prerequisite step before product analysis and interview work
- if they are already installed, plan to use them during product analysis, interview framing, docs generation, and architecture/spec shaping
- if they are not installed, tell the user all missing pinned companion skills up front rather than only the first one
- ask whether the user wants those missing companion skills auto-installed before product analysis and interview start
- default to the helper installer flow (`python3 <skill>/scripts/companion_skills.py install <skill>`) instead of leading with manual clone/copy commands
- print manual clone/copy commands only as fallback guidance, or if the user explicitly asks for manual installation
- do not require network-based catalog verification before printing those commands; use the pinned commands in this skill directly
- do not block the bootstrap if the user declines or skips installation; continue with the built-in workflow
- handle installs one skill at a time: propose the first missing relevant skill, install it if the user agrees, then move to the next one

Recommended companion skills by area:

- `prisma-cli` for database and schema work
- `nextjs-app-router-patterns` for Next.js App Router patterns
- `frontend-design` and `frontend-responsive-ui` for UI and responsive design work
- `clean-architecture` for architecture and boundary shaping

Pinned manual install commands:

```bash
git clone https://github.com/prisma/skills.git
cp -r skills/prisma-cli ~/.codex/skills/prisma-cli
```

```bash
git clone https://github.com/sickn33/antigravity-awesome-skills.git
cp -r antigravity-awesome-skills/skills/nextjs-app-router-patterns ~/.codex/skills/
```

```bash
git clone https://github.com/am-will/codex-skills.git
cp -r codex-skills/skills/frontend-design ~/.codex/skills/
cp -r codex-skills/skills/frontend-responsive-ui ~/.codex/skills/
```

```bash
git clone https://github.com/MKToronto/python-clean-architecture-codex.git
cp -r python-clean-architecture-codex/.agents/skills/clean-architecture ~/.codex/skills/clean-architecture
```

Helper script usage:

```bash
python3 <skill>/scripts/companion_skills.py status --json
python3 <skill>/scripts/companion_skills.py command prisma-cli
python3 <skill>/scripts/companion_skills.py install prisma-cli
```

### 2. Interview until the docs are decision-complete

Ask the user questions in stages, not all at once.
Before the first substantive product question, follow this exact startup order:

1. companion skill recommendation and installation decision
2. if the user accepts installs, complete that skill-install flow first
3. only after the install decision flow is resolved, begin product analysis/reference review
4. then give the `Plan` mode recommendation
5. then give a short handoff telling the user to say `continue` when ready to begin the interview
6. only after that, ask the first substantive product question

Do not combine the handoff with the first product question.
Do not combine the companion-skill installation decision with the `continue` handoff in the same prompt.
Do not repeat the startup guidance twice.
At the startup handoff stage, do not ask for product intent yet; wait for the user to say `continue` or otherwise clearly indicate readiness.
Do not deeply review the user’s desired product/reference before the companion-skill installation decision is resolved.

At the startup handoff, tell the user that `Plan` mode enables selectable option lists for interview questions and recommend switching to `Plan` mode if they want that UI.
If companion skills are missing, summarize all missing pinned companion skills first, ask whether the user wants them auto-installed before product analysis and the first interview question, and then handle accepted installs one by one.
After the install decision is finished, send a separate prompt for the `Plan` mode recommendation and `continue` handoff.
Do not replace the pinned install commands with guessed `skill-installer` or upstream-catalog commands unless the user explicitly asks to use the installer flow.
Install and propose companion skills one at a time rather than dumping every missing skill at once.
If the session remains in `Default` mode, continue with one-question-at-a-time plain-text questions, suggested options, and free-form fallback.
Prefer one question at a time unless the user explicitly asks for batching.

For each interview question:

- offer a small set of reasonable options when the space is predictable
- mark one option as recommended when there is a defensible default
- always allow the user to answer in free form instead of choosing an option
- keep the question narrow enough that the user can answer without opening another editor unless they prefer to

In `Plan` mode, prefer the built-in selectable option-list flow when available.
In `Default` mode, treat those options as plain-text suggestions rather than clickable UI controls.
Do not require the user to prepare answers in a separate editor unless they want to.

For continuation runs, do a delta interview rather than repeating the full bootstrap interview.
Ask only what is needed to define the next feature tranche and its tests without guessing.

The interview must make the test strategy explicit before scaffolding starts.
Do not accept vague answers like "we should have decent coverage" or "we can add tests later."
It must also identify the distinct in-scope user-visible features so the generated specs and task queue can be sliced by feature instead of collapsing everything into one generic flow.
You need a clear statement of:

- which distinct user-visible features exist in v1
- which unit-level behaviors must be covered
- which end-to-end flows must be covered
- which external-resource features require end-to-end proof before promotion
- which deterministic commands prove the repo is healthy
- which command failures block task promotion
- which UI-heavy tasks need dedicated screenshot, responsive, and accessibility proof

Cover at least:

- project name and one-line definition
- primary user and target problem
- v1 scope and explicit non-goals
- core entities and relationships
- important routes or screens
- storage/runtime constraints
- quality bar, unit coverage expectations, and required E2E flows
- any special security or reliability constraints

If a feature depends on an outside resource such as AI chat, a third-party API, external auth, or other remote infrastructure, require that feature to appear in an E2E scenario before the related task can promote.
If a feature wave is mostly UI or UX work, use [references/ui-verification.md](references/ui-verification.md) and make the UI promotion contract explicit before plan generation starts.

Use [references/interview-checklist.md](references/interview-checklist.md) as the stop condition.
Do not start writing the docs until the answers are sufficient to fill the required markdown set in [references/doc-baseline.md](references/doc-baseline.md).
If the test strategy is still ambiguous, keep asking.
For continuation runs, also use [references/expansion-mode.md](references/expansion-mode.md) to decide whether the next wave is specific enough to write new specs and active plans.

### 3. Materialize the docs tree first

Create a temporary answers JSON file from the interview.

- Prefer `/tmp/ralph-bootstrap-answers.json` unless the user wants the answers stored in-repo.
- Use uppercase snake-case keys that match the template placeholders.
- Keep multiline sections as markdown-ready strings.

Render the baseline templates:

```bash
python3 <skill>/scripts/render_docs.py --answers /tmp/ralph-bootstrap-answers.json --repo-root <target-repo>
```

Then expand the rendered docs into project-specific content.

- Replace any remaining generic placeholders.
- Add project-specific design docs and product specs beyond the baseline templates whenever the product has more than one distinct user-visible feature.
- If the user provides local or online references, analyze them into `docs/references/` and preserve the useful project-specific takeaways there.
- Ensure `AGENTS.md` stays short and points into the docs tree.
- Ensure active execution plans contain real `taskmeta` blocks and deterministic checks.
- Ensure the docs clearly state that promotion is blocked when required test commands fail.
- Use [references/feature-slicing.md](references/feature-slicing.md) to decide how many product specs and executable tasks are needed.

When the answers JSON includes structured feature data:

- populate `FEATURE_SPECS` with one entry per distinct user-visible feature
- optionally set `SLICE_SIZE` to `micro`, `balanced`, or `coarse` to control task granularity
- optionally set `BACKLOG_DEPTH` to values such as `next wave`, `10-15 tasks`, `~2-3 days`, or a task-count target
- optionally set `TARGET_EXEC_TASK_COUNT` when the founder wants an explicit queue length
- populate `EXEC_TASKS` with a sequenced task queue rather than only the baseline trio
- keep each non-hardening task aligned to exactly one product spec whenever possible
- let `scripts/render_docs.py` materialize those feature specs and executable task files alongside the baseline docs

If `FEATURE_SPECS` is present and `EXEC_TASKS` is omitted, `scripts/render_docs.py` will derive a queue whose size follows the selected `SLICE_SIZE` and `BACKLOG_DEPTH` controls. Multiple exec-plans may map to the same product spec when that is required to keep the slices narrow.
If `EXEC_TASKS` is provided but still collapses multiple product specs into broad tasks, the renderer should fail instead of silently accepting the queue.

For continuation runs:

- update the existing product specs before adding new active plans
- add or revise design docs when the new feature changes system shape or boundaries
- update quality, reliability, and security docs if the new wave changes their posture
- keep `docs/references/` current when new user-provided references appear
- leave completed plan history intact
- stop after the docs and next active queue are refreshed; do not begin app-code implementation in the same continuation run

### 3b. Improve supporting docs before writing exec-plans

Before writing or revising exec-plans:

- review the relevant product, frontend, architecture, and design docs together
- enhance those docs if the feature description is still rough
- use installed companion skills during design and architecture work when they are available and relevant
- do not create exec-plan pages from weak supporting docs

### 3c. Generate smaller exec-plan pages

Create exec-plan pages only after the supporting docs are sufficiently detailed.

Rules:

- create one exec-plan page per small feature slice
- avoid broad milestone-style scopes
- keep each non-hardening plan focused on one feature front
- include enough description that an implementer does not need to guess from other docs alone

### 3d. Review each exec-plan page individually

After generating the queue:

- review each exec-plan page one by one
- expand any page whose scope, exit criteria, or checks are still rough
- use [references/doc-quality-loop.md](references/doc-quality-loop.md) as the quality gate
- if quality is still insufficient, loop on the docs and plans until it is sufficient
- if the blocker is missing user intent rather than weak writing, stop plan generation and return to the interview stage
- if the blocker is environment-specific rather than a real product/doc defect, use [references/environment-blockers.md](references/environment-blockers.md) and define the RCA path before continuing

### 4. Scaffold the app only after the docs exist

Use [references/nextjs-ts-preset.md](references/nextjs-ts-preset.md) as the scaffold contract.

For v1 of this skill, the scaffold is opinionated:

- Next.js App Router
- TypeScript
- npm
- ESLint
- Playwright
- `node --import tsx --test` for unit tests

If the generated app depends on persistent runtime state such as SQLite/Prisma or local runtime preparation, follow [references/runtime-startup.md](references/runtime-startup.md).
For operator-visible Next.js server logs outside the test path, also follow [references/server-logging.md](references/server-logging.md).

The generated scaffold must match the docs and expose these commands:

- `npm run lint`
- `npm run typecheck`
- `npm run build`
- `npm run test:unit`
- `npm run test:e2e`
- `npm run verify`

For stateful apps, also expose deterministic runtime-prep and startup-proof commands such as:

- `npm run db:prepare`
- `npm run start:smoke`

For operator-visible manual startup, generated repos should also expose:

- `npm run start:logged`

And document:

- the `logs/` directory location
- the supported server log levels such as `trace`, `debug`, `info`, `warn`, and `error`
- the environment variable used to select the log level

Do not install the Ralph loop before these commands and their underlying file layout make sense.
Do not describe a promotion-ready repo unless the test commands are wired into the actual promotion contract.
Do not treat `build` as proof that the shipped runtime can start.

During implementation, prefer the smallest targeted check that proves the changed unit or slice still works.
For example:

- run unit tests for the changed domain logic while iterating
- run focused E2E coverage only for the affected journey while stabilizing that slice
- keep `npm run verify` as the promotion gate for task completion
- use the runtime startup smoke when the app’s real `start` path depends on prepared runtime state
- for UI-focused tasks, add a task-scoped `@ui-*` Playwright command and make screenshots, responsive assertions, and accessibility checks part of the promotion contract

During the initial bootstrap run, stop at the foundation boundary.
Do not implement the queued feature tasks during the bootstrap session.
The skill may complete only the foundation/bootstrap task needed to guarantee the harness environment.

### 5. Install and adapt the Ralph loop

Install the copied Ralph assets into the repo:

```bash
python3 <skill>/scripts/install_ralph.py --repo-root <target-repo>
```

Then adapt the copied files to the new repo.

Required adaptations:

- keep docs and task paths aligned with the generated docs tree
- keep the deterministic commands aligned with `package.json`
- keep the port cleanup aligned with the Playwright server port
- keep state files and operator guidance accurate
- keep the prompt-generation logic aligned with the task-doc layout

Treat `assets/templates/ralph/` as the starting point, not as an immutable drop-in.

### 5b. Finalize bootstrap state

After the docs, scaffold, Ralph assets, and deterministic verification are in place:

- mark the bootstrap/foundation task as completed
- move that task contract into `docs/exec-plans/completed/`
- leave feature tasks in `docs/exec-plans/active/`
- activate the first remaining feature task for the future Ralph run
- initialize `state/` so Ralph can start from the first real feature task

Use:

```bash
python3 <skill>/scripts/finalize_bootstrap_state.py --repo-root <target-repo>
```

This step should happen during the bootstrap session.
Do not run the Ralph loop itself from the bootstrap session just to advance feature tasks.

### 6. Seed the initial queue

Create an initial active queue that fits the new product.

At minimum include:

- one bootstrap or foundation task
- one first user-visible vertical slice
- one validation or hardening task

Treat that as a floor, not a target.
If the product has multiple distinct user-visible features, generate as many small active tasks as needed to represent them.
Queue depth should follow the founder's requested backlog size. When the founder does not specify one, default to `SLICE_SIZE=balanced` and `BACKLOG_DEPTH=10-15 tasks`.
Do not stop at one task per feature spec when a large feature still needs to be broken into smaller promotion-ready slices.

Each active task must have:

- `taskmeta`
- objective
- scope and out-of-scope
- exit criteria
- required checks
- evaluator notes
- progress log section

Promotion rules must be explicit in each task:

- required commands are mandatory gates, not suggestions
- a task cannot be promoted when its required test commands fail
- evaluator approval cannot override failing deterministic checks
- if a task introduces or changes an external-resource feature, the relevant E2E scenario must pass before promotion
- if a task is UI-focused, it should use `taskmeta.promotion_mode = deterministic_only` so passing deterministic UI checks is sufficient for promotion without human review

For continuation runs, create the next queue wave rather than replacing history wholesale.
The next wave should normally include:

- one foundation or enabling task if the feature needs new infrastructure
- one user-visible vertical slice for the new feature
- one follow-up hardening or integration task

Update `docs/exec-plans/active/index.md` so the new sequence is readable as the next tranche of work.
Do not hide multiple major feature fronts inside a single “first slice” task.
If the founder asks for a longer backlog, continue splitting the in-scope feature fronts until the requested backlog depth is represented or the current docs can no longer support narrower plans without guessing.

### 6b. Expand after the initial queue is complete

When the initial queue has been completed and the founder wants more features, stay in the same skill.

Use this expansion loop:

1. inspect completed plans and current specs to understand what is already true
2. interview for the next feature wave and its explicit test strategy
3. update product specs and design docs first
4. create the next active exec-plans with `taskmeta`, checks, and promotion rules
5. validate that the new queue is coherent and that the required commands still match the repo

Do not jump straight into implementation of new features without first refreshing the docs and task queue.
For continuation runs, treat the deliverable as planning-only by default:

1. inspect what is already true
2. interview for the delta
3. update the harness-engineering docs and Ralph-loop docs first
4. create the next active exec-plans
5. stop and hand back the refreshed queue

Do not modify application code, routes, schemas, tests, or runtime wiring in the same continuation pass unless the user later gives a new explicit implementation request against a specific active exec-plan after the queue refresh is complete.
If the user says something broad like “implement the plan” while the continuation interview or queue-refresh work is still in progress, treat that as ambiguous and finish the docs/exec-plan refresh first.

### 7. Validate before handoff

Before finishing, verify as much as the environment allows.

Minimum expectation:

- docs tree exists and cross-links make sense
- scaffold commands exist
- Ralph scripts exist under `scripts/ralph/`
- `state/README.md` exists
- the active queue is renderable
- the completed directory contains the finished bootstrap/foundation task
- the active directory contains only the remaining feature tasks, not already-completed ones
- `state/current-task.txt` points at the first real feature task or `NONE` only when the queue is truly exhausted
- one-cycle and loop-run guidance are written down
- continuation guidance is clear when the current queue has ended

If the environment allows package installation and test execution, run the project verification commands and at least a dry `scripts/ralph/status.sh` check.

If subagents are available, use them primarily for exploration, search, or summarization.
Keep validation comparatively constrained: avoid fanning out broad concurrent test/build runs that create noisy backpressure or conflicting interpretations of failure.

If the same environment-specific blocker appears three times for the current task:

- stop retrying the same task as-is
- record the repeated blocker in the task log and debt tracking
- auto-create a blocker-specific RCA/fix exec-plan
- make that blocker plan the current plan automatically
- after it is resolved, return to the original task instead of abandoning the whole process

Generated Ralph loops should also treat `worker.jsonl` updates as the worker heartbeat.
If the worker phase goes silent past the configured stall timeout, mark the cycle as stalled, stop the unattended loop, preserve evidence, and hand off to operator triage instead of waiting forever on `codex exec`.
Do not treat a first stall as automatic RCA-plan creation.
Branch into the blocker/RCA path only after the same environment-specific blocker has repeated enough times to satisfy the exceptional-flow rule.

### 8. Consider companion skills when allowed

If the user explicitly allows companion skills and they are installed, consider using them before planning or implementation when they fit the work:

- `prisma-cli` for database and schema work
- `nextjs-app-router-patterns` for Next.js App Router patterns
- `frontend-design` and `frontend-responsive-ui` for UI and responsive design work
- `clean-architecture` for architecture and boundary shaping

Do not assume they are present. Prefer checking and recommending them before documentation starts. Use them only when installed and clearly relevant.

## Important Rules

- Keep the repository knowledge base as the system of record.
- Keep `AGENTS.md` short; push depth into `docs/`.
- Prefer strict boundaries and predictable structure over clever abstractions.
- Keep tasks small, vertically sliced, and promotion-oriented.
- Treat the test strategy as part of product definition, not post-hoc cleanup.
- Never allow a task to promote on narrative completeness when required tests are red.
- When a queue ends, re-enter through docs and planning before adding more feature work.
- Search before assuming a thing is not implemented.
- When adding or changing tests, capture why the test exists and what regression it prevents.
- External-resource features must be exercised by E2E before promotion.
- If the user allows companion skills and they are installed, consider them before planning and implementation.
- Before writing exec-plans, review and improve the related architecture, design, product, and frontend docs.
- Review each exec-plan page individually and keep looping until its quality is sufficient or missing user intent forces a return to interview.
- Repeated environment-specific blockers should auto-branch into a dedicated RCA/fix exec-plan after three occurrences, then return to the original task.
- Generated Ralph loops should detect stalled workers from missing `worker.jsonl` progress, not from guessed Codex internal health, and surface compact `o`/`x`/`!` cycle marks in `state/run-log.md`.
- Generated Ralph loops must abort the cycle immediately when task-prompt rendering fails; they must never continue into worker, evaluator, commit, or promotion using a stale prompt artifact.
- Generated Ralph loops must keep `state/current-task.txt` synchronized with runnable tasks in `docs/exec-plans/active/`, and use `NONE` only when the runnable queue is actually exhausted.
- Repos with persistent runtime state must prove a production-style startup path, not just build/test paths.
- Generated repos should expose an operator-visible `start:logged` path and server log levels so humans can inspect real server flow without relying only on Ralph artifacts.
- Each distinct user-visible feature should normally get its own spec and one or more small executable tasks.
- Do not let the generator stop at one generic `core-flow.md` and one oversized first-slice task when the product clearly has several feature fronts.
- The bootstrap session may complete only the foundation task; remaining feature tasks must be left for the Ralph loop or a later explicit implementation session.
- Do not leave completed task contracts sitting in `docs/exec-plans/active/`.
- Prefer parallel search and analysis over parallel validation.
- Do not broaden the first version beyond the Next.js preset.
- Do not leave the repo with aspirational docs that the scaffold contradicts.
- If the generated scaffold diverges from the copied Ralph scripts, adapt the scripts immediately instead of documenting the mismatch.

## Deliverables

A successful run leaves the target repo with:

- a complete repo-local docs tree
- a working initial Next.js TypeScript scaffold
- installed Ralph loop scripts under `scripts/ralph/`
- state file guidance under `state/README.md`
- an initial active task queue
- a clear path for generating the next active queue after the initial tranche is complete
- concrete operator guidance for:
  - one cycle
  - unattended loop
  - status inspection
  - where logs and artifacts live
