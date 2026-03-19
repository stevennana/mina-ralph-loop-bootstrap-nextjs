#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


CODEX_SKILLS_DIR = Path.home() / ".codex" / "skills"


@dataclass(frozen=True)
class CompanionSkill:
    name: str
    repo_url: str
    repo_name: str
    source_path: str
    install_name: str
    area: str
    purpose: str
    pinned_commands: tuple[str, ...]

    @property
    def install_path(self) -> Path:
        return CODEX_SKILLS_DIR / self.install_name

    @property
    def installed(self) -> bool:
        return self.install_path.exists()


SKILLS: dict[str, CompanionSkill] = {
    "prisma-cli": CompanionSkill(
        name="prisma-cli",
        repo_url="https://github.com/prisma/skills.git",
        repo_name="skills",
        source_path="skills/prisma-cli",
        install_name="prisma-cli",
        area="db",
        purpose="database and schema work",
        pinned_commands=(
            "git clone https://github.com/prisma/skills.git",
            "cp -r skills/prisma-cli ~/.codex/skills/prisma-cli",
        ),
    ),
    "nextjs-app-router-patterns": CompanionSkill(
        name="nextjs-app-router-patterns",
        repo_url="https://github.com/sickn33/antigravity-awesome-skills.git",
        repo_name="antigravity-awesome-skills",
        source_path="skills/nextjs-app-router-patterns",
        install_name="nextjs-app-router-patterns",
        area="nextjs",
        purpose="Next.js App Router patterns",
        pinned_commands=(
            "git clone https://github.com/sickn33/antigravity-awesome-skills.git",
            "cp -r antigravity-awesome-skills/skills/nextjs-app-router-patterns ~/.codex/skills/",
        ),
    ),
    "frontend-design": CompanionSkill(
        name="frontend-design",
        repo_url="https://github.com/am-will/codex-skills.git",
        repo_name="codex-skills",
        source_path="skills/frontend-design",
        install_name="frontend-design",
        area="ui",
        purpose="UI design work",
        pinned_commands=(
            "git clone https://github.com/am-will/codex-skills.git",
            "cp -r codex-skills/skills/frontend-design ~/.codex/skills/",
        ),
    ),
    "frontend-responsive-ui": CompanionSkill(
        name="frontend-responsive-ui",
        repo_url="https://github.com/am-will/codex-skills.git",
        repo_name="codex-skills",
        source_path="skills/frontend-responsive-ui",
        install_name="frontend-responsive-ui",
        area="ui",
        purpose="responsive UI work",
        pinned_commands=(
            "git clone https://github.com/am-will/codex-skills.git",
            "cp -r codex-skills/skills/frontend-responsive-ui ~/.codex/skills/",
        ),
    ),
    "clean-architecture": CompanionSkill(
        name="clean-architecture",
        repo_url="https://github.com/MKToronto/python-clean-architecture-codex.git",
        repo_name="python-clean-architecture-codex",
        source_path=".",
        install_name="clean-architecture",
        area="architecture",
        purpose="architecture and boundary shaping",
        pinned_commands=(
            "git clone https://github.com/MKToronto/python-clean-architecture-codex.git",
            "cp -r python-clean-architecture-codex ~/.codex/skills/clean-architecture",
        ),
    ),
}


def _resolve_skills(requested: list[str] | None) -> list[CompanionSkill]:
    if not requested:
        return list(SKILLS.values())
    resolved: list[CompanionSkill] = []
    for name in requested:
        skill = SKILLS.get(name)
        if skill is None:
            raise SystemExit(f"Unknown companion skill: {name}")
        resolved.append(skill)
    return resolved


def _print_status(skills: list[CompanionSkill], json_output: bool) -> int:
    if json_output:
        payload = [
            {
                "name": skill.name,
                "installed": skill.installed,
                "install_path": str(skill.install_path),
                "area": skill.area,
                "purpose": skill.purpose,
            }
            for skill in skills
        ]
        print(json.dumps(payload, indent=2))
        return 0

    for skill in skills:
        state = "installed" if skill.installed else "missing"
        print(f"{skill.name}: {state} ({skill.purpose})")
    return 0


def _print_commands(skill: CompanionSkill) -> int:
    print("\n".join(skill.pinned_commands))
    return 0


def _run(cmd: list[str], cwd: Path | None = None) -> None:
    result = subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def _install_skill(skill: CompanionSkill) -> int:
    CODEX_SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    if skill.install_path.exists():
        print(f"{skill.name} is already installed at {skill.install_path}", file=sys.stderr)
        return 0

    with tempfile.TemporaryDirectory(prefix="codex-companion-skill-") as tmp:
        tmp_path = Path(tmp)
        checkout_path = tmp_path / skill.repo_name
        _run(["git", "clone", "--depth", "1", skill.repo_url, str(checkout_path)])

        source_path = checkout_path / skill.source_path
        if not source_path.exists():
            raise SystemExit(f"Skill source path not found: {source_path}")

        shutil.copytree(source_path, skill.install_path)

    print(f"Installed {skill.name} to {skill.install_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect or install pinned companion skills.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    status_parser = subparsers.add_parser("status", help="Show install status for companion skills.")
    status_parser.add_argument("skills", nargs="*", help="Optional subset of skill names.")
    status_parser.add_argument("--json", action="store_true", help="Emit JSON output.")

    command_parser = subparsers.add_parser("command", help="Print pinned install commands for one skill.")
    command_parser.add_argument("skill", help="Skill name.")

    install_parser = subparsers.add_parser("install", help="Install one companion skill into ~/.codex/skills.")
    install_parser.add_argument("skill", help="Skill name.")

    args = parser.parse_args()

    if args.command == "status":
        return _print_status(_resolve_skills(args.skills), args.json)
    if args.command == "command":
        return _print_commands(_resolve_skills([args.skill])[0])
    if args.command == "install":
        return _install_skill(_resolve_skills([args.skill])[0])
    raise SystemExit(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
