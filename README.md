# mina-ralph-loop-bootstrap-nextjs

`mina-ralph-loop-bootstrap-nextjs` is a Codex skill for bootstrapping or extending a brand new or very early-stage repository into a Ralph-style task-promotion repo.

The skill is intentionally opinionated in v1. It supports only:

- Next.js App Router
- TypeScript
- npm
- ESLint
- Playwright
- unit tests via `node --import tsx --test`

Its job is to:

1. interview the founder until product and architecture ambiguity is removed
2. generate a repo-local markdown knowledge base
3. scaffold the initial Next.js app to match those docs
4. install and adapt Ralph loop scripts
5. seed an initial active task queue with deterministic checks
6. document how to run one loop or an unattended loop
7. re-enter a bootstrapped repo later to define the next feature wave and its exec-plans

## Harness Flow

This is the end-to-end harness-engineering flow the skill is meant to apply, from founder discovery through repeated Ralph-loop execution and later feature-wave expansion.

![Harness-engineering Ralph loop flow](assets/readme/ralph-loop-harness-flow.svg)

## Core Model

This skill follows the harness-engineering model:

- the repository is the system of record
- `AGENTS.md` in generated repos stays short and points into `docs/`
- product, architecture, quality, reliability, security, and plans live in markdown
- active tasks are executable contracts with `taskmeta`
- promotion depends on deterministic checks, with a separate evaluator step for normal tasks and deterministic-only promotion available for UI-focused tasks
- failing required test commands block promotion

It also adopts a few practical Ralph-style operating rules:

- search the codebase before assuming something is not implemented
- keep tasks narrow and promotion-oriented
- prefer targeted checks while iterating, then use `verify` as the promotion gate
- document why important tests exist so future loops do not weaken them accidentally
- if a feature depends on an outside resource such as AI chat, it should be covered by an E2E scenario before promotion
- if a feature wave is mostly UI or UX work, require a dedicated `@ui-*` Playwright command plus screenshot, responsive, and accessibility checks before promotion
- if the same environment-specific blocker repeats three times, branch into an RCA/fix exec-plan instead of stalling the original task forever
- if the app has persistent runtime state, prove the production-style startup path explicitly instead of assuming `build` is enough
- generated Ralph loops must fail closed on prompt-render errors and must not keep running on stale `current-task.txt` state

## Repository Layout

- `SKILL.md`: operating contract for Codex
- `references/`: harness model, doc baseline, interview checklist, and Next.js preset
- `references/feature-slicing.md`: rules for turning product features into multiple specs and small executable tasks
- `references/doc-quality-loop.md`: quality gate for refining docs and exec-plan pages until they are decision-complete
- `references/environment-blockers.md`: exceptional path for repeated environment-specific verification blockers
- `references/runtime-startup.md`: contract for proving production-style startup in stateful apps
- `references/server-logging.md`: contract for operator-visible Next.js server logging, `start:logged`, and log-level configuration
- `references/ui-verification.md`: contract for deterministic UI/UX promotion via Playwright tags, screenshots, and accessibility checks
- `assets/templates/docs/references/README.md`: rule for turning user-provided references into durable repo-local reference notes
- `scripts/render_docs.py`: renders the baseline docs into a target repo
- `scripts/install_ralph.py`: installs the Ralph assets into a target repo
- `scripts/companion_skills.py`: checks, prints commands for, and installs the pinned companion skills
- `scripts/finalize_bootstrap_state.py`: archives the completed foundation task and leaves feature tasks queued for Ralph
- `scripts/template_utils.py`: shared rendering helpers
- `references/expansion-mode.md`: rules for generating the next active queue after the initial tranche is complete
- `assets/templates/root/`: root-file templates
- `assets/templates/docs/`: docs-tree templates
- `assets/templates/ralph/`: copied Ralph loop adaptation base
- `agents/openai.yaml`: optional skill shortcut metadata

## Skill Workflow

The skill is meant to run in this order:

1. inspect the target repo
2. interview the founder until the docs can be written without guessing
   The interview must also produce a concrete test strategy and explicit promotion-blocking checks.
3. map the distinct user-visible features that need their own specs and task slices
4. render the baseline docs tree
5. expand those docs into project-specific material
   User-provided local or online references should be analyzed into `docs/references/` and kept for future iterations.
6. improve the supporting architecture/design/product docs until they are specific enough
7. generate smaller exec-plan pages for individual features
8. review each exec-plan page one by one and loop on quality if needed
9. scaffold the Next.js app to match the docs
10. install and adapt the Ralph loop
11. finalize the bootstrap task state without running feature tasks
12. seed the initial active task queue
13. validate commands and hand back operator guidance

## Limitations

Current v1 limitations:

- optimized for empty or very early repositories
- not yet a generic multi-framework bootstrapper
- does not yet support FastAPI, Go, or arbitrary stacks
- copied Ralph assets are a starting point, not guaranteed drop-ins
- copied Ralph assets should still fail closed on invalid current-task state and prompt-render failures
- generated docs may still need project-specific rewriting after first render
- the skill repo does not yet include a full self-regression harness

## Bootstrap Boundary

The bootstrap session should only guarantee the harness environment:

- docs rendered and tightened
- minimal scaffold in place
- Ralph installed and aligned
- deterministic commands working
- production-style startup proven when the app depends on runtime state
- operator-visible `npm run start:logged` logging available for manual server inspection
- bootstrap foundation task archived into `docs/exec-plans/completed/`
- remaining feature tasks left in `docs/exec-plans/active/` for the Ralph loop

The skill should not pre-execute the queued feature tasks during the initial bootstrap run.

## Repeated Blockers

If a similar environment-specific verification blocker happens three times on the same task:

1. stop retrying that task unchanged
2. persist the blocker signature and RCA evidence
3. auto-create a small blocker-specific exec-plan
4. switch the queue to that blocker plan
5. return to the original task afterward through normal promotion

## Continue After The Initial Plans Are Done

The same skill should be used after the first queue is complete.

The intended follow-on workflow is:

1. inspect completed plans and current specs
2. interview only for the next feature delta
3. update product specs and design docs first
4. create the next active exec-plans
5. keep the same promotion rules and required test gates
6. stop there and hand back the refreshed queue

Important continuation boundary:

- use this skill to refresh the harness-engineering docs and create the next exec-plan wave
- do not start application-code implementation in the same continuation pass
- after the queue exists, let Ralph or a later explicit implementation request pick up one active task

Example prompt in a later Codex session:

```text
Use $mina-ralph-loop-bootstrap-nextjs to plan the next feature wave for this repo. Read the completed plans, update the docs first, and create the next active exec-plans with explicit promotion-blocking tests.
```

If you want implementation after that planning pass, do it as a separate follow-up against a specific active task, for example:

```text
Implement docs/exec-plans/active/021-search-retrieval.md and do not broaden beyond that task contract.
```

Useful follow-on prompt when implementation drift is suspected:

```text
Use $mina-ralph-loop-bootstrap-nextjs to inspect this repo, search before assuming missing implementations, update the docs first, and create the next smallest promotion-ready task wave.
```

## Enable The Skill In A New Codex Project

Codex discovers local skills from `~/.codex/skills/<skill-name>`. The simplest setup is a symlink from your skill checkout into that directory.

### 1. Install the skill into Codex

From any shell:

```bash
mkdir -p ~/.codex/skills
ln -s /absolute/path/to/mina-ralph-loop-bootstrap-nextjs ~/.codex/skills/mina-ralph-loop-bootstrap-nextjs
```

If the symlink already exists and you want to refresh it:

```bash
rm ~/.codex/skills/mina-ralph-loop-bootstrap-nextjs
ln -s /absolute/path/to/mina-ralph-loop-bootstrap-nextjs ~/.codex/skills/mina-ralph-loop-bootstrap-nextjs
```

For this repository specifically, the installed path is commonly:

```bash
ln -s /Users/stevenna/PycharmProjects/mina-ralph-loop-bootstrap-nextjs ~/.codex/skills/mina-ralph-loop-bootstrap-nextjs
```

### 2. Open the target repository in Codex

Start a Codex session with the new or early-stage project as the working directory.

### 3. Invoke the skill by name

In the Codex session, explicitly ask for the skill:

```text
Use $mina-ralph-loop-bootstrap-nextjs to bootstrap this repository.
```

You can also give the short brief inline:

```text
Use $mina-ralph-loop-bootstrap-nextjs to bootstrap this repository into a docs-first Ralph-style Next.js App Router + TypeScript project.
```

### 4. Check companion skills before product analysis

Before product analysis, before reviewing the user’s reference implementation in depth, before founder discovery, and before writing specs, the skill should check whether the pinned companion skill set is already installed in `~/.codex/skills`.

If the customer allows them, this recommendation should happen before documentation starts because these skills can affect:

- interview framing
- architecture and boundary decisions
- route and App Router structure
- database and schema choices
- UI and responsive design direction

If companion skills are missing, the skill should tell the user that clearly, summarize all missing pinned companion skills up front, and ask whether to auto-install them before continuing.
The default startup path should use `python3 scripts/companion_skills.py install <skill>` one skill at a time.
Manual clone/copy commands should be shown as fallback guidance or when the user asks for them directly.
It should not block on upstream catalog verification first; the pinned commands in this skill are the source of truth for that startup message.
It should propose and install them one skill at a time rather than dumping all missing skills at once.

### 5. Answer the discovery questions

The skill will ask staged founder questions covering:

- product identity and user
- v1 scope and non-goals
- domain model
- routes and core flows
- storage/runtime assumptions
- quality bar and required tests
- reliability and security constraints

The stop condition is not just "enough detail to scaffold." The interview must make the test strategy explicit enough that the generated plans can say which checks are required and which failures block promotion.
That includes calling out external-resource features that must be covered by E2E before promotion.
It should also identify the distinct user-visible features that need separate specs and smaller task slices.

Preferred interaction style:

- before the first substantive product question, the skill should first resolve companion-skill installation, then review the product/reference context, then separately handle `Plan` mode guidance, then separately give a short `continue` handoff
- the skill should ask one question at a time
- when appropriate, it should offer a few reasonable options and mark a recommended one
- the user should always be able to ignore the options and answer in free form
- at the start of founder discovery, it should recommend `Plan` mode if the user wants selectable option lists

In `Plan` mode, the skill should prefer selectable option lists when the session supports them. In `Default` mode, these remain plain-text options. The user does not need to prepare answers in another editor unless they prefer to draft them there.
The startup message should end by telling the user to say `continue` when ready for the first interview question.
The startup message should be printed once, not duplicated.
The companion-skill install decision and the `continue` handoff should not be asked in the same prompt.
The companion-skill install decision should happen before deep product/reference review.

## Recommended Companion Skills

If the customer allows them and they are relevant to the work, consider installing and using these companion skills before planning or implementation.

### Database skill

```bash
git clone https://github.com/prisma/skills.git
cp -r skills/prisma-cli ~/.codex/skills/prisma-cli
```

### Next.js skill

```bash
git clone https://github.com/sickn33/antigravity-awesome-skills.git
cp -r antigravity-awesome-skills/skills/nextjs-app-router-patterns ~/.codex/skills/
```

### UI design skills

```bash
git clone https://github.com/am-will/codex-skills.git
cp -r codex-skills/skills/frontend-design ~/.codex/skills/
cp -r codex-skills/skills/frontend-responsive-ui ~/.codex/skills/
```

### Architecture skill

```bash
git clone https://github.com/MKToronto/python-clean-architecture-codex.git
cp -r python-clean-architecture-codex/.agents/skills/clean-architecture ~/.codex/skills/clean-architecture
```

When available and allowed:

- use `prisma-cli` before documentation, planning, and implementation of database schema or migration work
- use `nextjs-app-router-patterns` before documentation, planning, and implementation of App Router structure
- use `frontend-design` or `frontend-responsive-ui` before documentation, planning, and implementation of significant UI work
- use `clean-architecture` before documentation, planning, and implementation of major boundaries or system structure

## Companion Skill Helper Script

This repo includes a pinned helper for the startup flow:

```bash
python3 scripts/companion_skills.py status --json
python3 scripts/companion_skills.py command nextjs-app-router-patterns
python3 scripts/companion_skills.py install nextjs-app-router-patterns
```

Recommended startup behavior:

1. check which pinned companion skills are missing
2. summarize all missing pinned companion skills
3. ask whether to auto-install them before product analysis and the interview
4. if the user accepts, install the first one
5. move to the next accepted missing skill
6. only then review the product/reference context in depth
7. start the interview only after the user is ready to continue

### 6. Let the skill materialize the repo

The expected output includes:

- `AGENTS.md`
- `ARCHITECTURE.md`
- `docs/PRODUCT_SENSE.md`
- `docs/FRONTEND.md`
- `docs/PLANS.md`
- `docs/DESIGN.md`
- `docs/QUALITY_SCORE.md`
- `docs/RELIABILITY.md`
- `docs/SECURITY.md`
- `docs/design-docs/*`
- `docs/product-specs/*`
- `docs/exec-plans/active/*`
- `scripts/ralph/*`
- `state/README.md`
- a minimal Next.js scaffold with deterministic commands

## Typical Generation Commands

When the skill is run manually or extended, these scripts are the entry points:

```bash
python3 scripts/render_docs.py --answers /tmp/ralph-bootstrap-answers.json --repo-root /path/to/target-repo
python3 scripts/install_ralph.py --repo-root /path/to/target-repo
python3 scripts/finalize_bootstrap_state.py --repo-root /path/to/target-repo
```

If the answers JSON includes structured `FEATURE_SPECS` and `EXEC_TASKS`, `scripts/render_docs.py` now materializes:

- multiple product spec files under `docs/product-specs/`
- a feature-sliced active queue under `docs/exec-plans/active/`
- refreshed `index.md` files for those directories

If `FEATURE_SPECS` is present without `EXEC_TASKS`, the renderer derives a queue whose depth follows the selected `SLICE_SIZE` and `BACKLOG_DEPTH` controls. Multiple exec-plans may point at the same product spec when that is needed to keep the tasks narrow.
If `EXEC_TASKS` is present but a task spans multiple product specs, the renderer now fails instead of accepting an oversized queue.

## Operating A Generated Repo

After the skill finishes bootstrapping a target repo, the normal operator entrypoints are the generated Ralph scripts inside that target repo.

Run one full cycle:

```bash
./scripts/ralph/run-once.sh
./scripts/ralph/status.sh
```

Run a longer unattended loop:

```bash
./scripts/ralph/run-loop.sh
```

Or with a custom sleep interval between cycles:

```bash
RALPH_LOOP_SLEEP_SECONDS=45 ./scripts/ralph/run-loop.sh
```

Run the generated Next.js server with a persistent operator log:

```bash
npm run start:logged
LOG_LEVEL=debug npm run start:logged
```

Monitor current state and logs:

```bash
./scripts/ralph/status.sh
tail -f state/run-log.md
cat state/current-cycle.json
cat state/evaluation.json
cat state/backlog.md
cat state/last-result.txt
ls logs/
tail -f logs/next-server-*.log
```

Generated Ralph loops now support a compact cycle-health line inside `state/run-log.md`:

- `o` = cycle completed and task promoted
- `x` = cycle completed but stayed not-done, failed, or auto-branched into RCA
- `!` = worker stalled during that cycle

A single `!` does not mean the blocker RCA exec-plan should be created immediately.
It means the unattended loop preserved stall evidence and recorded the blocker signature first.
Only repeated environment-specific blockers on the same task should branch into the RCA/fix exec-plan flow, and generated loops now auto-create that RCA task on the third identical blocker.

Example:

```text
- health: oo!xooo
```

Important state files in generated repos:

- `state/current-task.txt`: current active task id
- `state/current-cycle.json`: live phase/status for the current run
- `state/evaluation.json`: latest deterministic-check and evaluator result
- `state/run-log.md`: compact operator log across cycles
- `state/backlog.md`: rendered queue snapshot
- `state/task-history.md`: completed-task history
- `state/artifacts/`: per-cycle worker, evaluator, commit, and prompt artifacts
- `scripts/ralph/manual-promote.sh`: explicit operator override for stalled-but-done tasks, with optional reason and artifact arguments

Generated repos should treat server logging as part of the normal operator contract:

- `npm run start:logged` should create a timestamped log file under `logs/`
- `LOG_LEVEL` should control server verbosity for manual debugging
- server-side code should support at least `trace`, `debug`, `info`, `warn`, and `error`

## Enhancing This Skill

If you are improving the skill itself, start with `AGENT.md`, then read:

1. `SKILL.md`
2. `references/`
3. `scripts/`
4. `assets/templates/`

Keep the contract, references, templates, and generated repo expectations synchronized. The fastest way to break this skill is to update one layer and leave the others behind.
