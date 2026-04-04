from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RALPH_TEMPLATE_ROOT = REPO_ROOT / "assets" / "templates" / "ralph"


def make_task_markdown(task_id: str, title: str, status: str, next_task_on_success: str | None) -> str:
    taskmeta = {
        "id": task_id,
        "title": title,
        "order": int(task_id.split("-", 1)[0]),
        "status": status,
        "promotion_mode": "standard",
        "next_task_on_success": next_task_on_success,
        "prompt_docs": ["AGENTS.md", "docs/PLANS.md"],
        "required_commands": ["npm run verify"],
        "required_files": [],
        "human_review_triggers": [],
    }
    return textwrap.dedent(
        f"""\
        # {title}

        ```json taskmeta
        {json.dumps(taskmeta, indent=2)}
        ```

        ## Objective

        Ship {title}.

        ## Scope

        - Keep the task narrow.

        ## Out of scope

        - Unrelated changes.

        ## Exit criteria

        1. `npm run verify` passes.

        ## Required checks

        - `npm run verify`

        ## Evaluator notes

        Stay within scope.

        ## Progress log

        - initial note
        """
    )


class CurrentTaskFailClosedTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temp_dir.name)
        shutil.copytree(RALPH_TEMPLATE_ROOT, self.repo_root, dirs_exist_ok=True)

        (self.repo_root / "docs" / "exec-plans" / "active").mkdir(parents=True, exist_ok=True)
        (self.repo_root / "docs" / "exec-plans" / "completed").mkdir(parents=True, exist_ok=True)
        (self.repo_root / "AGENTS.md").write_text("Read docs.\n", encoding="utf-8")
        (self.repo_root / "docs" / "PLANS.md").write_text("# PLANS\n", encoding="utf-8")

        self.bin_dir = self.repo_root / "bin"
        self.bin_dir.mkdir()
        (self.bin_dir / "codex").write_text(
            "#!/usr/bin/env bash\n"
            "echo invoked >> codex-invoked.txt\n"
            "exit 0\n",
            encoding="utf-8",
        )
        os.chmod(self.bin_dir / "codex", 0o755)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def run_node(self, script_relative_path: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["node", script_relative_path],
            cwd=self.repo_root,
            check=True,
            capture_output=True,
            text=True,
        )

    def run_bash(self, script_relative_path: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["PATH"] = f"{self.bin_dir}:{env['PATH']}"
        return subprocess.run(
            ["bash", script_relative_path],
            cwd=self.repo_root,
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )

    def write_active_task(self, task_id: str, title: str, status: str, next_task_on_success: str | None) -> None:
        (self.repo_root / "docs" / "exec-plans" / "active" / f"{task_id}.md").write_text(
            make_task_markdown(task_id, title, status, next_task_on_success),
            encoding="utf-8",
        )

    def write_completed_task(self, task_id: str, title: str) -> None:
        (self.repo_root / "docs" / "exec-plans" / "completed" / f"{task_id}.md").write_text(
            make_task_markdown(task_id, title, "completed", None),
            encoding="utf-8",
        )

    def test_ensure_state_repairs_completed_only_current_task(self) -> None:
        self.write_active_task("026-next-task", "Next task", "active", None)
        self.write_completed_task("025-old-task", "Old task")
        (self.repo_root / "state").mkdir(exist_ok=True)
        (self.repo_root / "state" / "current-task.txt").write_text("025-old-task\n", encoding="utf-8")

        self.run_node("scripts/ralph/ensure-state.mjs")

        self.assertEqual(
            (self.repo_root / "state" / "current-task.txt").read_text(encoding="utf-8").strip(),
            "026-next-task",
        )
        backlog = (self.repo_root / "state" / "backlog.md").read_text(encoding="utf-8")
        self.assertIn("025-old-task", backlog)
        self.assertIn("026-next-task", backlog)

    def test_ensure_state_repairs_none_when_runnable_task_exists(self) -> None:
        self.write_active_task("026-next-task", "Next task", "active", None)
        (self.repo_root / "state").mkdir(exist_ok=True)
        (self.repo_root / "state" / "current-task.txt").write_text("NONE\n", encoding="utf-8")

        self.run_node("scripts/ralph/ensure-state.mjs")

        self.assertEqual(
            (self.repo_root / "state" / "current-task.txt").read_text(encoding="utf-8").strip(),
            "026-next-task",
        )

    def test_ensure_state_keeps_none_when_queue_is_exhausted(self) -> None:
        (self.repo_root / "state").mkdir(exist_ok=True)
        (self.repo_root / "state" / "current-task.txt").write_text("NONE\n", encoding="utf-8")

        self.run_node("scripts/ralph/ensure-state.mjs")

        self.assertEqual(
            (self.repo_root / "state" / "current-task.txt").read_text(encoding="utf-8").strip(),
            "NONE",
        )

    def test_run_once_aborts_before_worker_when_prompt_render_fails(self) -> None:
        self.write_active_task("026-next-task", "Next task", "active", None)
        self.run_node("scripts/ralph/ensure-state.mjs")

        render_task_prompt = self.repo_root / "scripts" / "ralph" / "render-task-prompt.mjs"
        render_task_prompt.write_text('console.error("forced prompt failure"); process.exit(1);\n', encoding="utf-8")

        result = self.run_bash("scripts/ralph/run-once.sh")

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertFalse((self.repo_root / "codex-invoked.txt").exists())

        current_cycle = json.loads((self.repo_root / "state" / "current-cycle.json").read_text(encoding="utf-8"))
        self.assertEqual(current_cycle["phase"], "prompt")
        self.assertEqual(current_cycle["status"], "failed")

        last_result = (self.repo_root / "state" / "last-result.txt").read_text(encoding="utf-8")
        self.assertIn("Prompt phase failed for task 026-next-task", last_result)

        run_log = (self.repo_root / "state" / "run-log.md").read_text(encoding="utf-8")
        self.assertIn("- prompt: failed ->", run_log)
        self.assertIn("- health: x", run_log)


if __name__ == "__main__":
    unittest.main()
