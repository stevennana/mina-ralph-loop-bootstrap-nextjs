#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

mkdir -p state scripts/ralph/generated docs/exec-plans/completed
node scripts/ralph/ensure-state.mjs >/dev/null
node scripts/ralph/render-backlog.mjs >/dev/null

RUN_LOG="state/run-log.md"
CYCLE_STATE_FILE="state/current-cycle.json"

append_log() {
  printf '%s\n' "$1" >> "$RUN_LOG"
}

last_nonempty_line() {
  local file_path="$1"
  awk 'NF { last = $0 } END { if (last) print last }' "$file_path"
}

write_cycle_state() {
  local phase="$1"
  local status="$2"
  node - "$CYCLE_STATE_FILE" "$TASK_ID" "$CYCLE_STARTED_AT" "$CYCLE_DIR" "$phase" "$status" <<'NODE'
const fs = require("fs");
const [filePath, taskId, startedAt, cycleDir, phase, status] = process.argv.slice(2);
fs.writeFileSync(
  filePath,
  `${JSON.stringify(
    {
      task_id: taskId,
      started_at: startedAt,
      artifact_dir: cycleDir,
      phase,
      status,
      updated_at: new Date().toISOString(),
    },
    null,
    2,
  )}\n`,
  "utf8",
);
NODE
}

TASK_ID="$(tr -d '\n' < state/current-task.txt || true)"
if [[ -z "${TASK_ID}" || "${TASK_ID}" == "NONE" ]]; then
  echo "No active task. Exiting run-once."
  exit 0
fi

CYCLE_STARTED_AT="$(date -Iseconds)"
CYCLE_STAMP="$(date +%Y%m%dT%H%M%S)"
CYCLE_DIR="state/artifacts/${CYCLE_STAMP}-${TASK_ID}"
mkdir -p "$CYCLE_DIR"

{
  echo ""
  echo "### cycle ${CYCLE_STARTED_AT} task=${TASK_ID}"
  echo "- artifacts: ${CYCLE_DIR}"
} >> "$RUN_LOG"

TASK_PROMPT_LOG="${CYCLE_DIR}/task-prompt.log"
write_cycle_state "prompt" "running"
if node scripts/ralph/render-task-prompt.mjs >"$TASK_PROMPT_LOG" 2>&1; then
  append_log "- prompt: rendered -> scripts/ralph/generated/current-task-prompt.txt"
else
  append_log "- prompt: failed -> ${TASK_PROMPT_LOG}"
fi

WORKER_LOG="${CYCLE_DIR}/worker.jsonl"
write_cycle_state "worker" "running"
append_log "- worker: started"
if codex exec \
  --full-auto \
  --sandbox workspace-write \
  --json \
  --output-last-message state/last-result.txt \
  "$(cat scripts/ralph/generated/current-task-prompt.txt)" \
  >"$WORKER_LOG" 2>&1; then
  append_log "- worker: completed -> ${WORKER_LOG}"
else
  append_log "- worker: failed -> ${WORKER_LOG}"
fi

if [[ -s state/last-result.txt ]]; then
  append_log "- worker-summary: $(head -n 1 state/last-result.txt)"
fi

EVALUATOR_LOG="${CYCLE_DIR}/evaluator.log"
write_cycle_state "evaluator" "running"
append_log "- evaluator: started"
if node scripts/ralph/evaluate-task.mjs >"$EVALUATOR_LOG" 2>&1; then
  :
fi

if [[ -f state/evaluation.json ]]; then
  EVALUATION_SUMMARY="$(node -e '
const fs = require("fs");
const data = JSON.parse(fs.readFileSync("state/evaluation.json", "utf8"));
const summary = (data.summary ?? "").replace(/\s+/g, " ").trim();
const head = `status=${data.status ?? "unknown"} promotion=${String(data.promotion_eligible ?? false)}`;
process.stdout.write(summary ? `${head} ${summary}` : head);
')"
  append_log "- evaluator: ${EVALUATION_SUMMARY} -> ${EVALUATOR_LOG}"
  NEXT_SERVER_LOG_PATH="$(node -e '
const fs = require("fs");
const data = JSON.parse(fs.readFileSync("state/evaluation.json", "utf8"));
const commands = Array.isArray(data?.deterministic?.commands) ? data.deterministic.commands : [];
const logPath = commands.find((command) => typeof command?.next_server_log_path === "string")?.next_server_log_path ?? "";
process.stdout.write(logPath);
')"
  if [[ -n "${NEXT_SERVER_LOG_PATH}" ]]; then
    append_log "- next-server-log: ${NEXT_SERVER_LOG_PATH}"
  fi
else
  append_log "- evaluator: failed -> ${EVALUATOR_LOG}"
fi

COMMIT_LOG="${CYCLE_DIR}/commit.log"
write_cycle_state "commit" "running"
if ./scripts/ralph/commit-if-changed.sh >"$COMMIT_LOG" 2>&1; then
  append_log "- commit: $(last_nonempty_line "$COMMIT_LOG")"
else
  append_log "- commit: failed -> ${COMMIT_LOG}"
fi

PROMOTE_LOG="${CYCLE_DIR}/promote.log"
write_cycle_state "promote" "running"
if node scripts/ralph/promote-task.mjs >"$PROMOTE_LOG" 2>&1; then
  append_log "- promote: $(last_nonempty_line "$PROMOTE_LOG")"
else
  append_log "- promote: failed -> ${PROMOTE_LOG}"
fi

BACKLOG_LOG="${CYCLE_DIR}/backlog.log"
write_cycle_state "backlog" "running"
if node scripts/ralph/render-backlog.mjs >"$BACKLOG_LOG" 2>&1; then
  NEXT_TASK="$(tr -d '\n' < state/current-task.txt || true)"
  append_log "- backlog: rendered current=${NEXT_TASK:-NONE}"
else
  append_log "- backlog: failed -> ${BACKLOG_LOG}"
fi

write_cycle_state "finished" "finished"
append_log "- cycle: finished"
