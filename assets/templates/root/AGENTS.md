# AGENTS.md

## Purpose
{{PROJECT_NAME}} is a {{ONE_LINE_PRODUCT}}.

This repository is optimized for agent-legible development and a Ralph-style task-promotion loop.

## Read Order
Before changing code or plans, read these files in order:

1. `ARCHITECTURE.md`
2. `docs/PRODUCT_SENSE.md`
3. `docs/design-docs/core-beliefs.md`
4. `docs/product-specs/index.md`
5. `docs/FRONTEND.md`
6. `docs/PLANS.md`
7. active plans in `docs/exec-plans/active/`

## Scope Guardrails
### In scope for v1
{{V1_SCOPE_BULLETS}}

### Explicitly out of scope for v1
{{NON_GOALS_BULLETS}}

## Product Shape
{{PRODUCT_SHAPE_BULLETS}}

## Technical Shape
{{TECHNICAL_SHAPE_BULLETS}}

## Validation Strategy
Use layered checks:
- unit tests for domain rules
- integration tests for repository/runtime boundaries where needed
- small E2E coverage for the required user journeys only

Promotion is blocked when required checks fail. Required test commands in active task contracts are hard gates, not suggestions.

### Required E2E flows
{{REQUIRED_E2E_BULLETS}}

## Documentation Discipline
- If behavior changes, update the related spec or design doc in the same cycle.
- Prefer small, executable plans over vague TODOs.
- When a repeated mistake appears, first document it; if it keeps recurring, promote it into tests or lint rules.
- Keep the documented test strategy current; do not leave promotion gates implied.

## Done Definition
{{DONE_DEFINITION}}
