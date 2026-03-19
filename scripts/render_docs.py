#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from template_utils import copy_rendered_tree, load_answers, load_answers_json


def _slugify(text: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "-" for ch in text.strip())
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-") or "item"


def _as_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        result: list[str] = []
        for item in value:
            if not isinstance(item, str):
                raise ValueError("Structured list values must contain strings only.")
            result.append(item)
        return result
    if isinstance(value, str):
        return [value]
    raise ValueError("Expected a string or list of strings.")


def _render_bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else "- TODO"


def _render_numbered(items: list[str]) -> str:
    return "\n".join(f"{index}. {item}" for index, item in enumerate(items, start=1)) if items else "1. TODO"


def _json_block(payload: object) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)


def render_structured_feature_artifacts(repo_root: Path, answers_json: dict[str, object], *, overwrite: bool) -> None:
    feature_specs = answers_json.get("FEATURE_SPECS")
    exec_tasks = answers_json.get("EXEC_TASKS")

    if feature_specs is None and exec_tasks is None:
        return

    docs_root = repo_root / "docs"
    specs_dir = docs_root / "product-specs"
    active_dir = docs_root / "exec-plans" / "active"

    if feature_specs is not None:
        if not isinstance(feature_specs, list):
            raise ValueError("FEATURE_SPECS must be a list when provided.")

        spec_rows: list[str] = []
        for spec in feature_specs:
            if not isinstance(spec, dict):
                raise ValueError("Each FEATURE_SPECS entry must be an object.")
            title = str(spec.get("title", "")).strip()
            if not title:
                raise ValueError("Each FEATURE_SPECS entry must include a non-empty title.")
            slug = str(spec.get("slug") or _slugify(title))
            filename = str(spec.get("filename") or f"{slug}.md")
            status = str(spec.get("status") or "confirmed")
            scope = str(spec.get("scope") or title)
            goal = str(spec.get("goal") or "")
            trigger = str(spec.get("trigger") or "")
            behavior = _as_list(spec.get("behavior_bullets"))
            validation = _as_list(spec.get("validation_bullets"))

            if not goal or not trigger or not behavior or not validation:
                raise ValueError(
                    f"Feature spec '{title}' must include goal, trigger, behavior_bullets, and validation_bullets."
                )

            spec_path = specs_dir / filename
            if spec_path.exists() and not overwrite:
                continue

            spec_path.parent.mkdir(parents=True, exist_ok=True)
            spec_path.write_text(
                "\n".join(
                    [
                        f"# {title}",
                        "",
                        "## Goal",
                        goal,
                        "",
                        "## Trigger / Entry",
                        trigger,
                        "",
                        "## User-Visible Behavior",
                        _render_bullets(behavior),
                        "",
                        "## Validation",
                        _render_bullets(validation),
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            spec_rows.append(f"| `{filename}` | {status} | {scope} |")

        if spec_rows:
            index_path = specs_dir / "index.md"
            index_path.write_text(
                "\n".join(
                    [
                        "# Product Specs Index",
                        "",
                        "## Purpose",
                        "This directory contains user-facing behavior specs.",
                        "If a UI or API behavior is visible to users, it should be defined here before implementation drifts.",
                        "",
                        "## Current Spec Set",
                        "| Spec | Status | Scope |",
                        "|---|---|---|",
                        *spec_rows,
                        "",
                        "## Editing Rule",
                        "When product behavior changes:",
                        "1. update the relevant spec",
                        "2. update the affected design or architecture docs if needed",
                        "3. only then adjust implementation plans",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

    if exec_tasks is not None:
        if not isinstance(exec_tasks, list):
            raise ValueError("EXEC_TASKS must be a list when provided.")

        sequence_lines: list[str] = []
        # The baseline templates always create generic 011/012 task files.
        # When the caller provides a structured task queue, those generic
        # contracts should not remain eligible for loop selection.
        for baseline_name in ("011-first-vertical-slice.md", "012-hardening-and-maintenance.md"):
            baseline_path = active_dir / baseline_name
            if baseline_path.exists():
                baseline_path.unlink()

        for task in exec_tasks:
            if not isinstance(task, dict):
                raise ValueError("Each EXEC_TASKS entry must be an object.")

            task_id = str(task.get("id", "")).strip()
            title = str(task.get("title", "")).strip()
            if not task_id or not title:
                raise ValueError("Each EXEC_TASKS entry must include non-empty id and title.")

            filename = str(task.get("filename") or f"{task_id}.md")
            objective = str(task.get("objective") or "")
            evaluator_notes = _as_list(task.get("evaluator_notes"))
            prompt_docs = _as_list(task.get("prompt_docs"))
            required_commands = _as_list(task.get("required_commands"))
            required_files = _as_list(task.get("required_files"))
            human_review_triggers = _as_list(task.get("human_review_triggers"))
            scope = _as_list(task.get("scope_bullets"))
            out_of_scope = _as_list(task.get("out_of_scope_bullets"))
            exit_criteria = _as_list(task.get("exit_criteria"))
            required_checks = _as_list(task.get("required_checks"))

            if not objective or not prompt_docs or not required_commands or not scope or not exit_criteria:
                raise ValueError(
                    f"Exec task '{task_id}' must include objective, prompt_docs, required_commands, scope_bullets, and exit_criteria."
                )

            order = int(task.get("order", 0))
            taskmeta = {
                "id": task_id,
                "title": title,
                "order": order,
                "status": str(task.get("status") or "queued"),
                "next_task_on_success": task.get("next_task_on_success"),
                "prompt_docs": prompt_docs,
                "required_commands": required_commands,
                "required_files": required_files,
                "human_review_triggers": human_review_triggers,
            }

            task_path = active_dir / filename
            if task_path.exists() and not overwrite:
                continue

            task_path.parent.mkdir(parents=True, exist_ok=True)
            task_path.write_text(
                "\n".join(
                    [
                        f"# {title}",
                        "",
                        "```json taskmeta",
                        _json_block(taskmeta),
                        "```",
                        "",
                        "## Objective",
                        "",
                        objective,
                        "",
                        "## Scope",
                        "",
                        _render_bullets(scope),
                        "",
                        "## Out of scope",
                        "",
                        _render_bullets(out_of_scope),
                        "",
                        "## Exit criteria",
                        "",
                        _render_numbered(exit_criteria),
                        "",
                        "## Required checks",
                        "",
                        _render_bullets(required_checks or required_commands),
                        "",
                        "## Evaluator notes",
                        "",
                        "\n".join(evaluator_notes) if evaluator_notes else "Promote only when the task is substantively complete and the required checks prove the claimed behavior.",
                        "",
                        "## Progress log",
                        "",
                        "- Start here. Append timestamped progress notes as work lands.",
                        "- Note when existing partial implementations were found and reused instead of replaced.",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            summary = str(task.get("summary") or objective)
            sequence_lines.append(f"{len(sequence_lines) + 1}. `{filename}` -> {summary}")

        if sequence_lines:
            active_index_path = active_dir / "index.md"
            active_index_path.write_text(
                "\n".join(
                    [
                        "# Ralph Loop Task Queue",
                        "",
                        f"This queue is the task-level promotion source of truth for {repo_root.name}.",
                        "",
                        "Only task files in this directory that contain a `taskmeta` JSON block are eligible for automatic selection, evaluation, and promotion.",
                        "",
                        "## Current recommended sequence",
                        *sequence_lines,
                        "",
                        "## Operating rule",
                        "",
                        "A task may be promoted only when all of the following are true:",
                        "",
                        "- deterministic checks pass",
                        "- the evaluator marks the task as `done`",
                        "- the evaluator recommends promotion",
                        "- the task metadata declares a `next_task_on_success`, or explicitly declares that the queue ends here",
                        "",
                        "## When this queue ends",
                        "",
                        "When the active sequence is exhausted, do not continue with ad hoc prompts alone.",
                        "Update the relevant product specs and design docs first, then seed the next active queue for the next feature wave.",
                        "",
                    ]
                ),
                encoding="utf-8",
            )


def main() -> int:
    parser = argparse.ArgumentParser(description="Render root/doc templates into a target repo.")
    parser.add_argument("--answers", required=True, help="Path to the bootstrap answers JSON.")
    parser.add_argument("--repo-root", required=True, help="Target repository root.")
    parser.add_argument(
        "--allow-missing",
        action="store_true",
        help="Leave unresolved {{PLACEHOLDER}} values in place instead of failing.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing files instead of skipping them.",
    )
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parent.parent
    repo_root = Path(args.repo_root).expanduser().resolve()
    answers_path = Path(args.answers).expanduser().resolve()
    answers = load_answers(answers_path)
    answers_json = load_answers_json(answers_path)

    roots = [
        (skill_root / "assets" / "templates" / "root", repo_root),
        (skill_root / "assets" / "templates" / "docs", repo_root / "docs"),
    ]

    all_missing: list[str] = []
    for source, destination in roots:
        if not source.exists():
            continue
        all_missing.extend(
            copy_rendered_tree(
                source,
                destination,
                answers,
                allow_missing=args.allow_missing,
                overwrite=args.overwrite,
            )
        )

    all_missing = sorted(set(all_missing))
    if all_missing and not args.allow_missing:
        print("Missing placeholders:", ", ".join(all_missing), file=sys.stderr)
        return 1

    render_structured_feature_artifacts(repo_root, answers_json, overwrite=args.overwrite)

    print(f"Rendered docs into {repo_root}")
    if all_missing:
        print("Unresolved placeholders left in place:", ", ".join(all_missing))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
