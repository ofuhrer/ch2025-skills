"""Exercise installations and the distributed helper outside the checkout."""
import importlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
install = importlib.import_module("install_skill").install


class PackagingTests(unittest.TestCase):
    def check_helper(self, skill):
        result = subprocess.run([sys.executable, str(skill / "scripts/ch2025.py"), "products"],
                                cwd=skill.parent, capture_output=True, text=True, check=True)
        self.assertEqual(len(json.loads(result.stdout)), 8)
        self.assertTrue((skill / "LICENSE").is_file())

    def test_installation_in_path_with_spaces_and_refusal_to_merge(self):
        with tempfile.TemporaryDirectory() as tmp:
            skills = Path(tmp) / "project with spaces/.agents/skills"
            installed = install(skills)
            self.check_helper(installed)
            marker = installed / "my-changes.txt"
            marker.write_text("keep")
            with self.assertRaises(FileExistsError):
                install(skills)
            self.assertEqual(marker.read_text(), "keep")
            self.assertFalse((installed / "ch2025").exists())
            self.assertFalse(list(installed.rglob("__pycache__")))

    def test_existing_dangling_symlink_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            link = Path(tmp) / "ch2025"
            link.symlink_to(Path(tmp) / "missing")
            with self.assertRaises(FileExistsError):
                install(tmp)
            self.assertTrue(link.is_symlink())

    def test_zip_runs_without_checkout(self):
        with tempfile.TemporaryDirectory() as tmp:
            with zipfile.ZipFile(ROOT / "releases/ch2025.zip") as archive:
                archive.extractall(tmp)
            self.check_helper(Path(tmp) / "ch2025")


if __name__ == "__main__":
    unittest.main()
