# Runtime Startup Contract

Use this reference when the generated repo has persistent runtime state such as a database, migrations, seed preparation, or local file storage.

## Core Rule

Do not treat `npm run build` as proof that the shipped runtime can actually start.

If the app depends on runtime preparation, the repo should expose deterministic commands that prove:

- the runtime state is prepared
- the production-style server can boot successfully
- the app can answer at least one basic request after startup

## Required Pattern

For repos with persistent runtime state, add:

- `db:prepare` or an equivalent explicit runtime-prep command
- `start:smoke` or an equivalent startup-smoke command
- `start:logged` or an equivalent operator-visible startup command when humans need to inspect real server behavior directly

## What `start:smoke` Should Prove

The startup smoke should:

- use the same runtime state shape the real `start` path depends on
- start the app in a production-style mode
- probe a minimal route successfully
- shut the app down cleanly

## Acceptance Rule

Do not consider the harness ready until either:

- `verify` includes the runtime startup proof, or
- the active task contract explicitly requires the startup smoke command alongside `verify`
