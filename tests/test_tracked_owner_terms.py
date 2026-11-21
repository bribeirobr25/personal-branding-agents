"""Fail if banned owner or private-lab terms appear in tracked files."""

import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Built from parts so this file does not itself contain a banned string.
BANNED = (
    "Bre" + "no",
    "Ral" + "ston",
    "Raku" + "ten",
    "diB" + "oaS",
    "personal-branding-" + "specialist",
    "/cursor/" + "stores",
)


def tracked_texts():
    raw = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
    for name in raw.decode("utf-8").split("\0"):
        if not name or name == "LICENSE":
            continue
        path = ROOT / name
        if not path.is_file():
            continue
        yield name, path.read_text(encoding="utf-8", errors="replace")


class TrackedOwnerTermTests(unittest.TestCase):
    def test_banned_terms_are_absent_from_tracked_files(self):
        hits = []
        folded = [term.casefold() for term in BANNED]
        for name, text in tracked_texts():
            lowered = text.casefold()
            for term in folded:
                if term in lowered:
                    hits.append(f"{name}: {term}")
        self.assertEqual(hits, [])

    def test_matcher_flags_a_synthetic_line(self):
        sample = "prefix " + BANNED[0] + " suffix"
        self.assertIn(BANNED[0].casefold(), sample.casefold())


if __name__ == "__main__":
    unittest.main()
