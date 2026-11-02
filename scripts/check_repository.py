#!/usr/bin/env python3
"""Check the distributable repository without network access or extra packages."""
import json
from pathlib import Path
import re

from build_release import ROOT, SKILL, build, package_files


def main():
    text = (SKILL / "SKILL.md").read_text()
    assert text.startswith("---\n")
    front = text.split("---", 2)[1]
    name = re.search(r"^name:\s*(.+)$", front, re.M).group(1)
    description = re.search(r"^description:\s*(.+)$", front, re.M).group(1)
    assert name == SKILL.name and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)
    assert len(name) <= 64 and 0 < len(description) <= 1024
    assert "license: 0BSD" in front
    assert len(text.splitlines()) < 500
    sources = json.loads((SKILL / "references/sources.json").read_text())
    assert len({s["id"] for s in sources}) == len(sources)
    assert all(s["url"].startswith("https://") for s in sources)
    build(check=True)
    documents = [ROOT / "README.md", *list((ROOT / "docs").glob("*.md")),
                 *list((ROOT / "examples").glob("*.md")), ROOT / "chat/CH2025_CHAT.md",
                 *list(SKILL.rglob("*.md"))]
    for path in documents:
        content = path.read_text()
        for target in re.findall(r"\]\(([^)]+)\)", content):
            target = target.strip("<>")
            if "://" in target or target.startswith(("#", "mailto:")):
                continue
            target = target.split("#")[0]
            assert (path.parent / target).exists(), f"Broken link: {path}: {target}"
    public = documents + package_files() + [ROOT / "LICENSE"]
    forbidden = ("/Users/", "meteoswiss.atlassian.net", "sources/internal", "service.meteoswiss.ch/git/")
    for path in public:
        if path.suffix in (".md", ".json", ".py", ".yaml"):
            content = path.read_text()
            assert not any(s in content for s in forbidden), f"Local/internal dependency: {path}"
    scenarios = json.loads((ROOT / "evaluation/scenarios.json").read_text())
    assert len({s["id"] for s in scenarios}) == len(scenarios)
    print(f"Repository checks passed: {len(documents)} Markdown documents, {len(sources)} sources, "
          f"{len(scenarios)} evaluation scenarios, current chat file and ZIP")


if __name__ == "__main__":
    main()
