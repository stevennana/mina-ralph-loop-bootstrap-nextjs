#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

node scripts/ralph/ensure-state.mjs >/dev/null

echo "## loop start $(date -Iseconds)" >> state/run-log.md

while true; do
  ./scripts/ralph/run-once.sh
  TASK_ID="$(tr -d '\n' < state/current-task.txt || true)"
  if [[ -z "${TASK_ID}" || "${TASK_ID}" == "NONE" ]]; then
    echo "No remaining task. Stopping loop." | tee -a state/run-log.md
    break
  fi
  sleep "${RALPH_LOOP_SLEEP_SECONDS:-30}"
done
