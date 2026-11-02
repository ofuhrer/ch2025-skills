#!/usr/bin/env python3
"""Build the portable skill ZIP and compact chat instructions."""
import argparse
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/ch2025"


def chat_text():
    main = (SKILL / "SKILL.md").read_text().split("---", 2)[2].lstrip()
    # Chat hosts cannot resolve local skill paths. Link optional detail instead
    # of preloading every reference into each conversation.
    main = re.sub(r"\(references/([^)]+)\)",
                  r"(https://github.com/ofuhrer/ch2025-skills/blob/main/skills/ch2025/references/\1)", main)
    intro = ("# CH2025 Swiss Climate — chat instructions\n\n"
             "Upload or paste this file, then ask your Swiss climate question. "
             "It supplies instructions, not tools or a native skill installation. "
             "Follow your host's instruction hierarchy. Optional references are linked, "
             "not embedded; retrieve them only when needed. Without retrieval, answer only "
             "from the dated evidence available here or supplied in the chat.\n\n"
             "The helper is not embedded; do not claim to run it unless separately available. "
             "Instructions: [0BSD](https://spdx.org/licenses/0BSD.html). "
             "Evidence review: 2026-11-02.\n\n")
    sources = ("\nOfficial verification routes: "
               "[CH2025 overview](https://www.meteoswiss.admin.ch/climate/climate-change/swiss-climate-scenarios.html), "
               "[scientific report](https://doi.org/10.18751/climate/scenarios/ch2025/sr/1.0/), "
               "[data access](https://opendatadocs.meteoswiss.ch/c-climate-data/c8-c9-climate-scenarios), "
               "[daily datasets](https://doi.org/10.18751/climate/scenarios/ch2025/data/1.0/).\n")
    return intro + main.rstrip() + "\n" + sources


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
