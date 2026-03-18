# Next.js TypeScript Preset

This skill's first version supports one opinionated scaffold only.

## Stack

- Next.js App Router
- TypeScript
- npm
- ESLint
- Playwright
- node test runner with `tsx`

## Required commands

The generated `package.json` should expose:

- `dev`
- `build`
- `start`
- `lint`
- `typecheck`
- `test:unit`
- `test:e2e`
- `test`
- `verify`

Recommended shapes:

- `test`: unit + e2e
- `verify`: lint + typecheck + build + test

For this skill, `verify` is not advisory. Generated task contracts should treat the required test-bearing commands as hard promotion gates.

## Minimum scaffold

- app router page for `/`
- one minimal domain/service path
- one unit test
- one Playwright smoke test
- deterministic commands wired before the Ralph loop is considered ready
- promotion logic aligned so failing required test commands block advancement

## Ralph alignment

Keep these defaults aligned unless there is a strong reason not to:

- Playwright server port: `3100`
- docs tree rooted at `docs/`
- task queue at `docs/exec-plans/active/`
- state under `state/`
- Ralph scripts under `scripts/ralph/`

## Adaptation Rules

- If the scaffold's commands differ, update the copied Ralph scripts immediately.
- If the app needs a different local server command or port for Playwright, update the evaluator preflight and operator docs together.
- Do not leave the repo in a state where the docs prescribe one command contract and `package.json` exposes another.
- Do not leave the repo in a state where the evaluator can promote tasks despite failing required test commands.
