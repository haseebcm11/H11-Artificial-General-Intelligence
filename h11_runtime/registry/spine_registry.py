"""Spine Registry."""
from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional


class SpineRegistry:
    """H11C-SPINE-REGISTRAR: Registry of governed specialist spines."""

    def __init__(self) -> None:
        self.spines: Dict[str, Callable[[], Any]] = {}

    def register_spine(self, spine_name: str, factory: Callable[[], Any]) -> None:
        self.spines[spine_name] = factory

    def get_spine(self, spine_name: str) -> Optional[Any]:
        factory = self.spines.get(spine_name)
        return factory() if factory else None
