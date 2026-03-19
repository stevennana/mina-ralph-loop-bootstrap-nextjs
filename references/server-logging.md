# Server Logging Contract

Use this reference when the generated repo needs operator-visible server logs outside the test harness.

## Core Rule

Do not make the production-style `start` path observable only through transient terminal output.

Generated repos should give operators a stable way to:

- start the Next.js server with logs persisted to disk
- choose a server log level for manual debugging
- inspect the latest server log without relying on Ralph artifacts

## Required Pattern

Generated repos should expose:

- `npm run start:logged`
- a `logs/` directory for operator-visible server logs
- a server log level environment variable such as `LOG_LEVEL`

## What `start:logged` Should Do

The logged startup path should:

- start the same production-style server used by `npm run start`
- create a timestamped log file under `logs/`
- capture stdout and stderr into that log file
- print the log file path so the operator can tail it immediately

## Log Levels

The server-side logging helper should support at least:

- `trace`
- `debug`
- `info`
- `warn`
- `error`

Default to a sane production-friendly level such as `info`.

## Code-Level Logging Expectations

Generated server code should have a small logging utility so route handlers and server-side flows can emit:

- `trace` for step-by-step flow diagnostics
- `debug` for development detail that is too noisy for normal use
- `info` for expected high-level lifecycle events
- `warn` for degraded but non-fatal conditions
- `error` for failures

## Safety Rule

Do not log secrets, full tokens, or sensitive user content by default.

When documenting logging in generated repos, explain:

- where log files are written
- how to set `LOG_LEVEL`
- how to tail the newest log during manual verification
