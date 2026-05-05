from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class RalphTemplateContractTests(unittest.TestCase):
    def test_evaluator_supports_deterministic_only_promotion(self) -> None:
        source = (REPO_ROOT / "assets" / "templates" / "ralph" / "scripts" / "ralph" / "evaluate-task.mjs").read_text(
            encoding="utf-8"
        )
        self.assertIn("promotion_mode", source)
        self.assertIn("deterministic_only", source)
        self.assertIn("task is eligible for automatic promotion", source)

    def test_ui_verification_reference_exists(self) -> None:
        reference = (REPO_ROOT / "references" / "ui-verification.md").read_text(encoding="utf-8")
        self.assertIn("@ui-<task-or-surface>", reference)
        self.assertIn("deterministic_only", reference)
        self.assertIn("@axe-core/playwright", reference)

    def test_run_once_and_docs_fail_closed_on_prompt_errors(self) -> None:
        run_once = (REPO_ROOT / "assets" / "templates" / "ralph" / "scripts" / "ralph" / "run-once.sh").read_text(
            encoding="utf-8"
        )
        ralph_readme = (
            REPO_ROOT / "assets" / "templates" / "ralph" / "scripts" / "ralph" / "README.md"
        ).read_text(encoding="utf-8")
        self.assertIn('write_cycle_state "prompt" "failed"', run_once)
        self.assertIn('append_health_mark "x"', run_once)
        self.assertIn("does not launch the worker/evaluator/promotion phases", ralph_readme)
        self.assertIn("repairs obvious drift", ralph_readme)

    def test_promotion_contract_mentions_fail_closed_successor_restore(self) -> None:
        agent_contract = (REPO_ROOT / "AGENT.md").read_text(encoding="utf-8")
        ralph_readme = (
            REPO_ROOT / "assets" / "templates" / "ralph" / "scripts" / "ralph" / "README.md"
        ).read_text(encoding="utf-8")
        promote_task = (
            REPO_ROOT / "assets" / "templates" / "ralph" / "scripts" / "ralph" / "promote-task.mjs"
        ).read_text(encoding="utf-8")

        self.assertIn("RCA return promotion must fail closed", agent_contract)
        self.assertIn("promotion fails closed", ralph_readme)
        self.assertIn("stable task identifier is", ralph_readme)
        self.assertIn("state/current-task.txt` stores the stable `taskmeta.id`", ralph_readme)
        self.assertIn("Next task", promote_task)
        self.assertIn("findTaskDoc(nextTaskId)", promote_task)
        self.assertIn("nextTask?.filePath", promote_task)
        self.assertIn("writeCurrentTaskId(nextTaskUpdate.nextCurrentTaskId)", promote_task)
        self.assertIn('normalized === "NONE"', promote_task)

    def test_active_queue_docs_allow_custom_filenames_with_stable_task_ids(self) -> None:
        active_index = (
            REPO_ROOT / "assets" / "templates" / "docs" / "exec-plans" / "active" / "index.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Filenames may be ordered or customized", active_index)
        self.assertIn("taskmeta.id", active_index)
        self.assertIn("taskmeta.next_task_on_success", active_index)


if __name__ == "__main__":
    unittest.main()
