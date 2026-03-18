# Hardening and maintenance

```json taskmeta
{
  "id": "012-hardening-and-maintenance",
  "title": "Hardening and maintenance",
  "order": 12,
  "status": "queued",
  "next_task_on_success": null,
  "prompt_docs": [
    "AGENTS.md",
    "ARCHITECTURE.md",
    "docs/QUALITY_SCORE.md",
    "docs/RELIABILITY.md",
    "docs/SECURITY.md"
  ],
  "required_commands": [
    "npm run verify"
  ],
  "required_files": [
    "scripts/ralph/README.md"
  ],
  "human_review_triggers": [
    "The task expands into broad feature work",
    "Reliability or security docs do not match the actual code",
    "Loop scripts mutate unrelated repo state without clear reason"
  ]
}
```

## Objective

Close the gap between the implemented slice and the repository's reliability, security, and automation posture.

## Scope

- reconcile docs and implementation drift
- keep the deterministic checks healthy
- tighten operator guidance for the Ralph loop
- record remaining debt explicitly

## Out of scope

- major new product features
- unrelated infrastructure expansion

## Exit criteria

1. `npm run verify` passes.
2. Loop documentation matches the actual scripts.
3. Reliability/security docs reflect the current implementation.
4. Remaining debt is explicit.

## Required checks

- `npm run verify`
- targeted checks for the reliability or hardening change being made, while iterating

## Evaluator notes

Promote only when the repository is ready for longer unattended Ralph-loop runs under the current task contract.
Do not promote if `npm run verify` fails, even if the hardening changes look correct by inspection.

## Progress log

- Start here. Append timestamped progress notes as work lands.
- Note when existing partial implementations were found and reused instead of replaced.
