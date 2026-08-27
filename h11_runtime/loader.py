"""Load agent.py modules from hyphenated directories that are not valid packages."""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sys
from types import ModuleType

def _get_repo_root() -> Path:
    p = Path(__file__).resolve()
    for cand in [p.parent, p.parents[1] if len(p.parents) > 1 else p.parent, p.parents[2] if len(p.parents) > 2 else p.parent]:
        if (cand / "H11Z_COGNITIVE_NETWORK").exists():
            return cand
    return p.parent

ROOT = _get_repo_root()


def _find_file(base_path: Path, rel_parts: list[str]) -> Path | None:
    if not rel_parts:
        return base_path if base_path.is_file() else None

    target = rel_parts[0].lower()
    target_clean = target.replace("_", "-").replace("h11-", "")

    if not base_path.exists() or not base_path.is_dir():
        return None

    for child in base_path.iterdir():
        child_name = child.name.lower()
        child_clean = child_name.replace("_", "-").replace("h11-", "")
        if child_name == target or child_clean == target_clean:
            found = _find_file(child, rel_parts[1:])
            if found:
                return found
    return None


def load_module(agent_id: str, relative: str) -> ModuleType:
    path = ROOT / relative
    if not path.is_file():
        parts = Path(relative).parts
        found_path = _find_file(ROOT, list(parts))
        if not found_path and (ROOT / "H11Z_COGNITIVE_NETWORK").exists():
            found_path = _find_file(ROOT / "H11Z_COGNITIVE_NETWORK", list(parts))
        if not found_path and (ROOT / "H11I_INTELLIGENCE_UNIVERSE").exists():
            found_path = _find_file(ROOT / "H11I_INTELLIGENCE_UNIVERSE", list(parts))
        if not found_path and (ROOT / "H11C_CONTROL_PLANE").exists():
            found_path = _find_file(ROOT / "H11C_CONTROL_PLANE", list(parts))

        if found_path and found_path.is_file():
            path = found_path
        else:
            raise FileNotFoundError(f"{path} (also searched pillar subdirectories)")

    key = f"h11_loaded.{agent_id.replace('-', '_')}"
    if key in sys.modules:
        return sys.modules[key]
    spec = importlib.util.spec_from_file_location(key, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[key] = module
    spec.loader.exec_module(module)
    return module
