from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_SPEC = (
    "<Agent System Instructions>",
    "</Agent System Instructions>",
    "H11-PREVIOUS",
    "H11-NEXT",
)


def read_spec(path: Path) -> str:
    raw = path.read_bytes()
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


class HygieneTests(unittest.TestCase):
    def test_specs_have_no_generator_wrappers_or_placeholder_deps(self):
        hits = []
        for path in ROOT.rglob("SPEC.md"):
            if "tools" in path.parts:
                continue
            text = read_spec(path)
            for token in FORBIDDEN_SPEC:
                if token in text:
                    hits.append(f"{path.relative_to(ROOT)}: {token}")
        self.assertEqual(hits, [])

    def test_no_agent_generators_remain(self):
        banned = {
            "generate_l16.py",
            "generate_l9.py",
            "generate_layer19.py",
            "generate_l20.py",
            "gen0.py",
            "gen1.py",
            "gen2.py",
            "gen3.py",
            "builder.py",
            "build_l15.py",
            "build_control_plane.py",
            "rewrite_l03_l12.py",
            "control_expand.py",
            "uniquify_agents.py",
        }
        found = []
        for path in ROOT.rglob("*.py"):
            if path.name in banned or path.name.startswith("generate_"):
                found.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(found, [])

    def test_l03_l12_are_not_process_processed_stubs(self):
        hits = []
        for layer in ("L03_representation", "L12_world_models"):
            for path in (ROOT / layer).rglob("agent.py"):
                text = path.read_text(encoding="utf-8")
                if 'result="processed"' in text or "result='processed'" in text:
                    hits.append(str(path.relative_to(ROOT)))
        self.assertEqual(hits, [])


if __name__ == "__main__":
    unittest.main()
