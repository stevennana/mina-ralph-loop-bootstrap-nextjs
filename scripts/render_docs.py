#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from template_utils import copy_rendered_tree, load_answers


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
    answers = load_answers(Path(args.answers).expanduser().resolve())

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

    print(f"Rendered docs into {repo_root}")
    if all_missing:
        print("Unresolved placeholders left in place:", ", ".join(all_missing))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
