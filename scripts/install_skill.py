#!/usr/bin/env python3
"""Copy CH2025 into a host's skills directory without replacing an installation."""
import argparse
from pathlib import Path
import shutil

from build_release import ROOT, SKILL


def install(skills_directory):
    destination = Path(skills_directory).expanduser().resolve() / SKILL.name
    destination.parent.mkdir(parents=True, exist_ok=True)
    # mkdir also rejects existing or dangling symlinks; never merge installations.
    destination.mkdir()
    try:
        shutil.copytree(SKILL, destination, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.part"))
        shutil.copy2(ROOT / "LICENSE", destination / "LICENSE")
    except BaseException:
        shutil.rmtree(destination)
        raise
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skills_directory", help="e.g. ~/.agents/skills or a project's .claude/skills")
    args = parser.parse_args()
    try:
        destination = install(args.skills_directory)
    except FileExistsError:
        parser.exit(1, "Already installed: keep or move the existing ch2025 folder before reinstalling.\n")
    except OSError as exc:
        parser.exit(1, f"Installation failed: {exc}\n")
    print(f"Installed {destination}. Open a new chat and invoke ch2025 using your host's syntax.")


if __name__ == "__main__":
    main()
