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


if __name__ == "__main__":
    unittest.main()
