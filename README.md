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

## Core Model

This skill follows the harness-engineering model:

- the repository is the system of record
- `AGENTS.md` in generated repos stays short and points into `docs/`
- product, architecture, quality, reliability, security, and plans live in markdown
- active tasks are executable contracts with `taskmeta`
- promotion depends on deterministic checks plus a separate evaluator step
- failing required test commands block promotion

It also adopts a few practical Ralph-style operating rules:

- search the codebase before assuming something is not implemented
- keep tasks narrow and promotion-oriented
- prefer targeted checks while iterating, then use `verify` as the promotion gate
- document why important tests exist so future loops do not weaken them accidentally
- if a feature depends on an outside resource such as AI chat, it should be covered by an E2E scenario before promotion

## Repository Layout

- `SKILL.md`: operating contract for Codex
- `references/`: harness model, doc baseline, interview checklist, and Next.js preset
- `scripts/render_docs.py`: renders the baseline docs into a target repo
- `scripts/install_ralph.py`: installs the Ralph assets into a target repo
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
3. render the baseline docs tree
4. expand those docs into project-specific material
5. scaffold the Next.js app to match the docs
6. install and adapt the Ralph loop
7. seed the initial active task queue
8. validate commands and hand back operator guidance

## Limitations

Current v1 limitations:

- optimized for empty or very early repositories
- not yet a generic multi-framework bootstrapper
- does not yet support FastAPI, Go, or arbitrary stacks
- copied Ralph assets are a starting point, not guaranteed drop-ins
- generated docs may still need project-specific rewriting after first render
- the skill repo does not yet include a full self-regression harness

## Continue After The Initial Plans Are Done

The same skill should be used after the first queue is complete.

The intended follow-on workflow is:

1. inspect completed plans and current specs
2. interview only for the next feature delta
3. update product specs and design docs first
4. create the next active exec-plans
5. keep the same promotion rules and required test gates

Example prompt in a later Codex session:

```text
Use $mina-ralph-loop-bootstrap-nextjs to plan the next feature wave for this repo. Read the completed plans, update the docs first, and create the next active exec-plans with explicit promotion-blocking tests.
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

### 4. Answer the discovery questions

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

Preferred interaction style:

- the skill should ask one question at a time
- when appropriate, it should offer a few reasonable options and mark a recommended one
- the user should always be able to ignore the options and answer in free form

In the current Codex CLI flow, these are plain-text options, not guaranteed clickable choice widgets. The user does not need to prepare answers in another editor unless they prefer to draft them there.

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
cp -r python-clean-architecture-codex ~/.codex/skills/clean-architecture
```

When available and allowed:

- use `prisma-cli` before planning database schema or migration work
- use `nextjs-app-router-patterns` before shaping App Router structure
- use `frontend-design` or `frontend-responsive-ui` before planning or implementing significant UI work
- use `clean-architecture` before defining major boundaries or system structure

### 5. Let the skill materialize the repo

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
```

## Enhancing This Skill

If you are improving the skill itself, start with `AGENT.md`, then read:

1. `SKILL.md`
2. `references/`
3. `scripts/`
4. `assets/templates/`

Keep the contract, references, templates, and generated repo expectations synchronized. The fastest way to break this skill is to update one layer and leave the others behind.
