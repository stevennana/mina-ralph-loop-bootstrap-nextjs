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

Open templates and copied Ralph assets only when you need them:

- `assets/templates/root/`
- `assets/templates/docs/`
- `assets/templates/ralph/`

Use these scripts when bootstrapping:

- `scripts/render_docs.py`
- `scripts/install_ralph.py`

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

Before founder discovery and before writing docs, check whether relevant companion skills are already installed under `~/.codex/skills`.

If the user allows companion skills:

- recommend the relevant ones before documentation starts, not after specs are already written
- if they are already installed, plan to use them during interview framing, docs generation, and architecture/spec shaping
- if they are not installed, tell the user which ones are missing and print the relevant manual installation commands immediately
- do not block the bootstrap if the user declines or skips installation; continue with the built-in workflow

Recommended companion skills by area:

- `prisma-cli` for database and schema work
- `nextjs-app-router-patterns` for Next.js App Router patterns
- `frontend-design` and `frontend-responsive-ui` for UI and responsive design work
- `clean-architecture` for architecture and boundary shaping

### 2. Interview until the docs are decision-complete

Ask the user questions in stages, not all at once.
At the start of founder discovery, tell the user that `Plan` mode enables selectable option lists for interview questions and recommend switching to `Plan` mode if they want that UI.
If companion skills are relevant and missing, mention that before the first substantive product question, print the install commands inline, and let the user choose whether to install them first.
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
- Ensure `AGENTS.md` stays short and points into the docs tree.
- Ensure active execution plans contain real `taskmeta` blocks and deterministic checks.
- Ensure the docs clearly state that promotion is blocked when required test commands fail.
- Use [references/feature-slicing.md](references/feature-slicing.md) to decide how many product specs and executable tasks are needed.

When the answers JSON includes structured feature data:

- populate `FEATURE_SPECS` with one entry per distinct user-visible feature
- populate `EXEC_TASKS` with a small sequenced task queue rather than only the baseline trio
- let `scripts/render_docs.py` materialize those feature specs and executable task files alongside the baseline docs

For continuation runs:

- update the existing product specs before adding new active plans
- add or revise design docs when the new feature changes system shape or boundaries
- update quality, reliability, and security docs if the new wave changes their posture
- leave completed plan history intact

### 4. Scaffold the app only after the docs exist

Use [references/nextjs-ts-preset.md](references/nextjs-ts-preset.md) as the scaffold contract.

For v1 of this skill, the scaffold is opinionated:

- Next.js App Router
- TypeScript
- npm
- ESLint
- Playwright
- `node --import tsx --test` for unit tests

The generated scaffold must match the docs and expose these commands:

- `npm run lint`
- `npm run typecheck`
- `npm run build`
- `npm run test:unit`
- `npm run test:e2e`
- `npm run verify`

Do not install the Ralph loop before these commands and their underlying file layout make sense.
Do not describe a promotion-ready repo unless the test commands are wired into the actual promotion contract.

During implementation, prefer the smallest targeted check that proves the changed unit or slice still works.
For example:

- run unit tests for the changed domain logic while iterating
- run focused E2E coverage only for the affected journey while stabilizing that slice
- keep `npm run verify` as the promotion gate for task completion

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

### 6. Seed the initial queue

Create an initial active queue that fits the new product.

At minimum include:

- one bootstrap or foundation task
- one first user-visible vertical slice
- one validation or hardening task

Treat that as a floor, not a target.
If the product has multiple distinct user-visible features, generate as many small active tasks as needed to represent them.

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

For continuation runs, create the next queue wave rather than replacing history wholesale.
The next wave should normally include:

- one foundation or enabling task if the feature needs new infrastructure
- one user-visible vertical slice for the new feature
- one follow-up hardening or integration task

Update `docs/exec-plans/active/index.md` so the new sequence is readable as the next tranche of work.
Do not hide multiple major feature fronts inside a single “first slice” task.

### 6b. Expand after the initial queue is complete

When the initial queue has been completed and the founder wants more features, stay in the same skill.

Use this expansion loop:

1. inspect completed plans and current specs to understand what is already true
2. interview for the next feature wave and its explicit test strategy
3. update product specs and design docs first
4. create the next active exec-plans with `taskmeta`, checks, and promotion rules
5. validate that the new queue is coherent and that the required commands still match the repo

Do not jump straight into implementation of new features without first refreshing the docs and task queue.

### 7. Validate before handoff

Before finishing, verify as much as the environment allows.

Minimum expectation:

- docs tree exists and cross-links make sense
- scaffold commands exist
- Ralph scripts exist under `scripts/ralph/`
- `state/README.md` exists
- the active queue is renderable
- one-cycle and loop-run guidance are written down
- continuation guidance is clear when the current queue has ended

If the environment allows package installation and test execution, run the project verification commands and at least a dry `scripts/ralph/status.sh` check.

If subagents are available, use them primarily for exploration, search, or summarization.
Keep validation comparatively constrained: avoid fanning out broad concurrent test/build runs that create noisy backpressure or conflicting interpretations of failure.

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
- Each distinct user-visible feature should normally get its own spec and one or more small executable tasks.
- Do not let the generator stop at one generic `core-flow.md` and one oversized first-slice task when the product clearly has several feature fronts.
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
