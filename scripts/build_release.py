#!/usr/bin/env python3
"""Build the portable skill ZIP and self-contained chat instructions."""
import argparse
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/ch2025"
REFERENCES = [("sources.md", "public-sources"), ("science.md", "scientific-interpretation"),
              ("products.md", "product-selection"),
              ("data.md", "data-access"), ("answering.md", "answer-patterns")]


def chat_text():
    main = (SKILL / "SKILL.md").read_text().split("---", 2)[2].lstrip()
    for filename, anchor in REFERENCES:
        main = main.replace(f"(references/{filename})", f"(#{anchor})")
    intro = ("# CH2025 Swiss Climate — instructions for ordinary chat\n\n"
             "Upload this file or paste its contents, then ask your Swiss climate question. "
             "Follow these instructions using the tools your host actually provides. "
             "This file does not enable tools or override the host's instruction hierarchy. "
             "No coding or installation is needed for explanations.\n\n"
             "The optional helper is in the [GitHub repository](https://github.com/ofuhrer/ch2025-skills); "
             "its code is not embedded here. Do not claim to execute that helper unless it is available. "
             "These new instructions use [0BSD](https://spdx.org/licenses/0BSD.html); "
             "CH2025 source attribution remains required as described below.\n\n"
             "Generated from the canonical skill and references. Evidence review: 2026-11-02.\n\n")
    pieces = [intro, main]
    for filename, anchor in REFERENCES:
        text = (SKILL / "references" / filename).read_text()
        for target, target_anchor in REFERENCES:
            text = text.replace(f"({target})", f"(#{target_anchor})")
            text = text.replace(f"(references/{target})", f"(#{target_anchor})")
        text = re.sub(r"^# .*\n", "", text, count=1).lstrip()
        pieces += [f'\n\n<a id="{anchor}"></a>\n\n## {anchor.replace("-", " ").title()}\n\n', text]
    return "".join(pieces).rstrip() + "\n"


def package_files():
    return sorted(p for p in SKILL.rglob("*") if p.is_file() and
                  "__pycache__" not in p.parts and p.suffix not in (".pyc", ".part"))


def build(check=False):
    chat = ROOT / "chat/CH2025_CHAT.md"
    archive = ROOT / "releases/ch2025.zip"
    expected = chat_text()
    if check:
        assert chat.read_text() == expected, "Chat instructions are stale; rebuild"
        with zipfile.ZipFile(archive) as z:
            wanted = {"ch2025/" + str(p.relative_to(SKILL)): p.read_bytes() for p in package_files()}
            wanted["ch2025/LICENSE"] = (ROOT / "LICENSE").read_bytes()
            assert set(z.namelist()) == set(wanted), "Unexpected or missing ZIP members"
            for name, content in wanted.items():
                assert z.read(name) == content, f"Stale ZIP member: {name}"
        return
    chat.parent.mkdir(exist_ok=True)
    chat.write_text(expected)
    archive.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for path in package_files() + [ROOT / "LICENSE"]:
            name = "ch2025/" + ("LICENSE" if path == ROOT / "LICENSE" else str(path.relative_to(SKILL)))
            info = zipfile.ZipInfo(name, date_time=(2026, 11, 2, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, path.read_bytes())
    print(f"Built {chat.relative_to(ROOT)} and {archive.relative_to(ROOT)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    build(parser.parse_args().check)
