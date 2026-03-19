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


def _product_spec_doc(filename: str) -> str:
    return f"docs/product-specs/{filename}"


def _is_hardening_task(task: dict[str, object]) -> bool:
    title = str(task.get("title") or "").lower()
    task_id = str(task.get("id") or "").lower()
    prompt_docs = _as_list(task.get("prompt_docs"))
    return (
        "hardening" in title
        or "maintenance" in title
        or "hardening" in task_id
        or "maintenance" in task_id
        or any(doc in {"docs/QUALITY_SCORE.md", "docs/RELIABILITY.md", "docs/SECURITY.md"} for doc in prompt_docs)
    )


def _product_spec_docs(prompt_docs: list[str]) -> list[str]:
    return [doc for doc in prompt_docs if doc.startswith("docs/product-specs/")]


def derive_exec_tasks_from_feature_specs(feature_specs: list[dict[str, object]], project_name: str) -> list[dict[str, object]]:
    derived: list[dict[str, object]] = []
    ordered_specs: list[tuple[str, dict[str, object]]] = []
    for spec in feature_specs:
        title = str(spec.get("title", "")).strip()
        slug = str(spec.get("slug") or _slugify(title))
        filename = str(spec.get("filename") or f"{slug}.md")
        ordered_specs.append((filename, spec))

    hardening_order = 10 + len(ordered_specs) + 1
    hardening_id = f"{hardening_order:03d}-hardening-and-maintenance"

    for index, (filename, spec) in enumerate(ordered_specs, start=1):
        order = 10 + index
        task_id = f"{order:03d}-{str(spec.get('slug') or _slugify(str(spec.get('title') or 'feature')))}"
        title = str(spec.get("title") or "Feature slice")
        validation = _as_list(spec.get("validation_bullets"))
        behavior = _as_list(spec.get("behavior_bullets"))
        out_of_scope = _as_list(spec.get("out_of_scope_bullets")) or [
            "unrelated feature fronts",
            "future product expansion beyond this feature",
        ]
        required_files = _as_list(spec.get("required_files"))
        required_commands = _as_list(spec.get("required_commands")) or ["npm run verify"]
        required_checks = _as_list(spec.get("required_checks")) or required_commands
        human_review_triggers = _as_list(spec.get("human_review_triggers")) or [
            "The task broadens into unrelated feature work.",
            "The deterministic checks do not actually prove the claimed behavior.",
        ]
        evaluator_notes = _as_list(spec.get("evaluator_notes")) or [
            f"Promote only when the {title.lower()} behavior works end-to-end in substance.",
        ]
        summary = str(spec.get("summary") or str(spec.get("scope") or str(spec.get("goal") or title))).strip()
        prompt_docs = [
            "AGENTS.md",
            "ARCHITECTURE.md",
            "docs/FRONTEND.md",
            _product_spec_doc(filename),
        ]

        next_task_on_success = (
            f"{11 + index:03d}-{str(ordered_specs[index][1].get('slug') or _slugify(str(ordered_specs[index][1].get('title') or 'feature')))}"
            if index < len(ordered_specs)
            else hardening_id
        )
        status = "active" if index == 1 else "queued"
        derived.append(
            {
                "id": task_id,
                "title": title,
                "order": order,
                "status": status,
                "next_task_on_success": next_task_on_success,
                "prompt_docs": prompt_docs,
                "required_commands": required_commands,
                "required_files": required_files,
                "human_review_triggers": human_review_triggers,
                "objective": str(spec.get("goal") or f"Implement {title} for {project_name}."),
                "scope_bullets": behavior,
                "out_of_scope_bullets": out_of_scope,
                "exit_criteria": validation,
                "required_checks": required_checks,
                "evaluator_notes": evaluator_notes,
                "summary": summary,
            }
        )

    derived.append(
        {
            "id": hardening_id,
            "title": "Hardening and maintenance",
            "order": hardening_order,
            "status": "queued",
            "next_task_on_success": None,
            "prompt_docs": [
                "AGENTS.md",
                "ARCHITECTURE.md",
                "docs/QUALITY_SCORE.md",
                "docs/RELIABILITY.md",
                "docs/SECURITY.md",
            ],
            "required_commands": ["npm run verify"],
            "required_files": ["scripts/ralph/README.md"],
            "human_review_triggers": [
                "The task expands into broad feature work.",
                "Reliability or security docs do not match the actual code.",
            ],
            "objective": f"Close the reliability, security, and automation gaps after the {project_name} feature slices land.",
            "scope_bullets": [
                "reconcile docs and implementation drift",
                "keep the deterministic checks healthy",
                "record remaining debt explicitly",
            ],
            "out_of_scope_bullets": [
                "major new product features",
                "unrelated infrastructure expansion",
            ],
            "exit_criteria": [
                "`npm run verify` passes.",
                "Reliability and security docs match the implementation.",
                "Remaining debt is explicit.",
            ],
            "required_checks": ["npm run verify"],
            "evaluator_notes": [
                "Promote only when the repository is ready for longer unattended Ralph-loop runs under the current task contract.",
            ],
            "summary": "reconcile reliability, security, and loop guidance after the feature slices land",
        }
    )
    return derived


def validate_exec_tasks(feature_specs: list[dict[str, object]], exec_tasks: list[dict[str, object]]) -> None:
    if not feature_specs:
        return

    spec_doc_map: dict[str, str] = {}
    for spec in feature_specs:
        title = str(spec.get("title", "")).strip()
        slug = str(spec.get("slug") or _slugify(title))
        filename = str(spec.get("filename") or f"{slug}.md")
        spec_doc_map[_product_spec_doc(filename)] = title or filename

    if len(exec_tasks) < len(feature_specs) + 1:
        raise ValueError(
            "EXEC_TASKS is too small for the feature set. Provide at least one task per feature spec plus a separate hardening/maintenance task."
        )

    if not any(_is_hardening_task(task) for task in exec_tasks):
        raise ValueError("EXEC_TASKS must include a separate hardening/maintenance task.")

    covered_specs: set[str] = set()
    for task in exec_tasks:
        prompt_docs = _as_list(task.get("prompt_docs"))
        product_docs = _product_spec_docs(prompt_docs)
        if _is_hardening_task(task):
            continue
        if len(product_docs) != 1:
            raise ValueError(
                f"Task '{task.get('id') or task.get('title')}' must reference exactly one product spec in prompt_docs to keep the slice narrow."
            )
        covered_specs.add(product_docs[0])

    missing = [spec_doc_map[doc] for doc in spec_doc_map if doc not in covered_specs]
    if missing:
        raise ValueError(
            "EXEC_TASKS does not cover every feature spec. Missing task coverage for: " + ", ".join(missing)
        )


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

    feature_spec_objects = feature_specs if isinstance(feature_specs, list) else []

    if exec_tasks is None and feature_spec_objects:
        exec_tasks = derive_exec_tasks_from_feature_specs(feature_spec_objects, repo_root.name)

    if exec_tasks is not None:
        if not isinstance(exec_tasks, list):
            raise ValueError("EXEC_TASKS must be a list when provided.")
        validate_exec_tasks(feature_spec_objects, exec_tasks)

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
            why_now = str(task.get("why_now") or "")
            evaluator_notes = _as_list(task.get("evaluator_notes"))
            prompt_docs = _as_list(task.get("prompt_docs"))
            required_commands = _as_list(task.get("required_commands"))
            required_files = _as_list(task.get("required_files"))
            human_review_triggers = _as_list(task.get("human_review_triggers"))
            scope = _as_list(task.get("scope_bullets"))
            out_of_scope = _as_list(task.get("out_of_scope_bullets"))
            exit_criteria = _as_list(task.get("exit_criteria"))
            required_checks = _as_list(task.get("required_checks"))
            dependencies = _as_list(task.get("dependencies_bullets"))
            implementation_notes = _as_list(task.get("implementation_notes_bullets"))
            docs_to_update = _as_list(task.get("docs_to_update"))

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
            body_lines = [
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
            ]
            if why_now:
                body_lines.extend(
                    [
                        "## Why now",
                        "",
                        why_now,
                        "",
                    ]
                )
            if dependencies:
                body_lines.extend(
                    [
                        "## Dependencies",
                        "",
                        _render_bullets(dependencies),
                        "",
                    ]
                )
            body_lines.extend(
                [
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
                ]
            )
            if implementation_notes:
                body_lines.extend(
                    [
                        "## Implementation notes",
                        "",
                        _render_bullets(implementation_notes),
                        "",
                    ]
                )
            if docs_to_update:
                body_lines.extend(
                    [
                        "## Docs to update",
                        "",
                        _render_bullets(docs_to_update),
                        "",
                    ]
                )
            body_lines.extend(
                [
                    "## Evaluator notes",
                    "",
                    "\n".join(evaluator_notes)
                    if evaluator_notes
                    else "Promote only when the task is substantively complete and the required checks prove the claimed behavior.",
                    "",
                    "## Progress log",
                    "",
                    "- Start here. Append timestamped progress notes as work lands.",
                    "- Note when existing partial implementations were found and reused instead of replaced.",
                    "",
                ]
            )
            task_path.write_text(
                "\n".join(body_lines),
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
