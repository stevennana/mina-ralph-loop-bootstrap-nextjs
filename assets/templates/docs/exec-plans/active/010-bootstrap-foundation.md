# Bootstrap foundation

```json taskmeta
{
  "id": "010-bootstrap-foundation",
  "title": "Bootstrap foundation",
  "order": 10,
  "status": "active",
  "next_task_on_success": "011-first-vertical-slice",
  "prompt_docs": [
    "AGENTS.md",
    "ARCHITECTURE.md",
    "docs/PRODUCT_SENSE.md",
    "docs/FRONTEND.md",
    "docs/PLANS.md"
  ],
  "required_commands": [
    "npm run verify"
  ],
  "required_files": [
    "package.json",
    "scripts/ralph/run-once.sh",
    "docs/exec-plans/active/index.md"
  ],
  "human_review_triggers": [
    "The task broadens into product-specific feature work",
    "The docs and scaffold disagree on the repo contract",
    "The scaffold does not support the documented deterministic commands"
  ]
}
```

## Objective

Bootstrap the repository so it has a coherent docs tree, a minimal Next.js scaffold, and a working Ralph loop foundation.

## Scope

- generate the baseline docs
- create the minimal scaffold
- install the Ralph loop
- expose deterministic commands

## Out of scope

- advanced product features
- polished UI
- optional integrations

## Exit criteria

1. The baseline docs exist.
2. The Next.js scaffold exists.
3. The Ralph scripts exist.
4. `npm run verify` passes.

## Required checks

- `npm run verify`
- targeted unit or smoke checks for the files being introduced, while iterating

## Evaluator notes

Promote only when the docs, scaffold, and Ralph scripts agree on the same repo contract.
Do not promote if `npm run verify` fails, even if the bootstrap looks complete by inspection.

## Progress log

- Start here. Append timestamped progress notes as work lands.
- Note when existing partial implementations were found and reused instead of replaced.
