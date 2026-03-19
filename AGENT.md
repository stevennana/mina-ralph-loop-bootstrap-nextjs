# AGENT.md

## Purpose

This repository defines the Codex skill `mina-ralph-loop-bootstrap-nextjs`.

The skill bootstraps a brand new or very early-stage repository into a docs-first, Ralph-style task-promotion repo using a fixed stack:

- Next.js App Router
- TypeScript
- npm
- ESLint
- Playwright
- unit tests via `node --import tsx --test`

This file is for contributors improving the skill itself, not for generated application repos.

## What Must Stay True

When enhancing this skill, preserve these invariants:

- Docs come before scaffold generation.
- The interview must produce a concrete test strategy before docs are considered complete.
- The preferred interview style is one question at a time, with suggested options and a free-form fallback.
- At interview start, the skill should recommend `Plan` mode when the user wants selectable option-list UX.
- At interview start, the skill should handle companion-skill guidance first, then `Plan` mode guidance, then a `continue` handoff before asking the first product question.
- The companion-skill install decision should happen before deep product/reference review.
- The companion-skill installation decision and the `continue` handoff should happen in separate prompts.
- The same skill should support later feature expansion by updating docs first and seeding the next exec-plan wave.
- The supported stack stays intentionally narrow unless the skill contract is explicitly expanded.
- `SKILL.md` remains the operating contract for another Codex instance.
- The references define stop conditions and baseline requirements; code and templates must agree with them.
- Generated repos must expose deterministic commands: `lint`, `typecheck`, `build`, `test:unit`, `test:e2e`, and `verify`.
- Multiple user-visible features should not collapse into one generic product spec and one oversized first-slice task.
- Each non-hardening executable task should usually map to exactly one product spec.
- Failing required test commands block promotion; evaluator judgment does not override red checks.
- Contributors should strengthen search-before-change behavior and avoid assumptions that code is missing.
- Tests should explain the behavior they protect when that context would otherwise be lost across loops.
- External-resource features should require E2E coverage before promotion.
- Optional companion skills should be considered only when the user allows them and they are actually installed.
- The pinned companion skill set should be checked and recommended before product analysis, founder discovery, and docs are written.
- If relevant companion skills are missing, the startup guidance should ask about auto-install first, use the helper installer by default, and keep the manual commands correct as fallback guidance.
- The startup guidance should use the pinned manual install commands from this skill, not guessed catalog paths.
- The pinned manual install commands and the helper installer paths must stay aligned with the actual upstream repo layout.
- The startup guidance should be emitted once, not duplicated.
- The startup guidance should summarize all relevant missing companion skills before asking about installation.
- Companion-skill installs should be proposed and run one skill at a time before the interview starts.
- The default startup install path should be the helper installer script, with manual commands as fallback only.
- Supporting architecture/design/product docs should be strengthened before exec-plan pages are written.
- Each exec-plan page should be reviewed individually for detail and scope quality.
- If doc quality is still weak, loop on docs and plans; if the blocker is missing intent, go back to interview.
- If the same environment-specific blocker repeats three times, create a dedicated RCA/fix exec-plan and then return to the original task.
- User-provided references should be analyzed into `docs/references/` and preserved as durable project knowledge.
- The bootstrap session must stop after foundation completion and must not pre-execute queued feature tasks.
- Completed tasks belong in `docs/exec-plans/completed/`, not `active/`.
- Stateful generated repos should prove their production-style startup path explicitly, not just pass build/test checks.
- Generated repos should expose an operator-visible `npm run start:logged` path, a `logs/` directory, and configurable server log levels for manual debugging.
- The copied Ralph assets are a starting point that must align with the generated repo shape.

## Read Order

Before changing behavior, read these files in order:

1. `SKILL.md`
2. `references/harness-engineering.md`
3. `references/doc-baseline.md`
4. `references/interview-checklist.md`
5. `references/feature-slicing.md`
6. `references/nextjs-ts-preset.md`
7. `references/server-logging.md`
8. `scripts/render_docs.py`
9. `scripts/install_ralph.py`
10. `scripts/companion_skills.py`
11. the relevant files under `assets/templates/`

## Repository Map

- `SKILL.md`: workflow contract followed by Codex
- `references/`: constraints, baseline docs, interview stop condition, scaffold preset
- `scripts/render_docs.py`: renders root and `docs/` templates into a target repo
- `scripts/install_ralph.py`: copies the Ralph loop assets into a target repo
- `scripts/template_utils.py`: placeholder rendering and tree-copy helpers
- `assets/templates/root/`: generated root-file templates
- `assets/templates/docs/`: generated docs-tree templates
- `assets/templates/ralph/`: Ralph loop adaptation base copied into target repos
- `agents/openai.yaml`: optional agent manifest/shortcut metadata for this skill

## Enhancement Rules

- Update the contract first when behavior changes materially.
- Keep templates and references synchronized. Do not let a template promise behavior the references do not describe.
- Keep placeholder names stable and uppercase snake case unless a migration is intentional.
- If you add required generated files, reflect that in `references/doc-baseline.md`.
- If you change command names, ports, or repo paths, update `references/nextjs-ts-preset.md` and the Ralph assets together.
- If you change how follow-on planning works after the initial queue, keep `SKILL.md`, `references/expansion-mode.md`, and the generated plan templates aligned.
- Do not broaden this into a general multi-framework bootstrapper by accident.

## Typical Change Workflow

1. Adjust `SKILL.md` if the execution contract changes.
2. Update the relevant `references/` file so the stop condition and baseline stay explicit.
3. Update templates under `assets/templates/`.
4. Update `scripts/render_docs.py`, `scripts/install_ralph.py`, or `scripts/template_utils.py` if generation behavior changes.
5. Regenerate into a scratch repo and verify the resulting repo shape and commands.

## Manual Validation

At minimum, validate these outcomes in a scratch target repo:

- root docs and the `docs/` tree render without unresolved placeholders unless intentionally allowed
- the generated app matches the fixed Next.js preset
- Ralph files install under `scripts/ralph/`
- `state/README.md` exists
- the initial active queue exists under `docs/exec-plans/active/`
- operator guidance for one cycle and unattended loop runs is present

## Out of Scope

Unless deliberately expanding the product, avoid:

- adding non-Next.js frameworks
- adding alternative package managers
- adding unrelated product logic into this repo
- turning generalized templates into Minakeep-specific copies
