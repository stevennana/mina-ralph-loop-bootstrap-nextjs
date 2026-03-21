# UI Verification

Use this reference when a feature wave is primarily about UI or UX quality rather than new domain behavior.

## Goal

Make UI-focused tasks promotable through deterministic automation alone.
Do not rely on human taste checks or manual approval to decide whether a UI task can advance.

## When This Applies

Treat a task as UI-focused when its scope is mainly about:

- visual system or design-token work
- layout, density, spacing, or typography changes
- responsive behavior
- navigation chrome, shells, cards, panels, or reusable presentation primitives
- route-level polish that should not alter core feature logic

## Promotion Contract

UI-focused tasks should require:

- `npm run verify`
- a dedicated Playwright UI command shaped like `npm run test:e2e -- --grep @ui-<task-or-surface>`

Set `taskmeta.promotion_mode` to `deterministic_only` for those tasks so passing required commands is sufficient for promotion.

## What The UI Command Must Prove

The tagged Playwright coverage should prove all of the following for the scoped surface:

- desktop viewport at `1440x900`
- mobile viewport at `390x844`
- the key hierarchy anchors and actions are visible
- no obvious overflow or collapsed-layout regression escapes the task scope
- screenshot baselines match the expected visual result
- automated accessibility scanning passes

## Screenshot Rules

- Prefer stable surface or container screenshots over fragile whole-page snapshots.
- Use full-page screenshots only when the entire page composition is the subject of the task.
- Disable or stabilize animations.
- Use deterministic fixtures or seeded state so screenshot drift is meaningful.

## Accessibility Rules

- Use `@axe-core/playwright` inside the tagged UI spec.
- Scan the scoped UI surface after it has fully settled.
- Fail the task on serious or critical issues by default.

## Evaluator Rules

- Deterministic UI tasks should not require human review for promotion.
- If the required commands pass, the task is promotion-eligible.
- If screenshot, responsive, or accessibility checks fail, the task is not promotion-eligible.
- Do not let subjective aesthetic judgment override deterministic command results in either direction.
