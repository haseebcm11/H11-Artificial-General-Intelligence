"""Spine Registry managing discovery, registration, and invocation of governed pipelines."""
from __future__ import annotations

import inspect
import logging
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


class SpineRegistry:
    """H11C-SPINE-REGISTRAR: Registry and discovery engine for governed specialist spines."""

    def __init__(self) -> None:
        self.spines: Dict[str, Callable[[], Any]] = {}
        self.spine_metadata: Dict[str, Dict[str, Any]] = {}
        self.cached_instances: Dict[str, Any] = {}

    def register_spine(
        self,
        spine_name: str,
        factory: Callable[[], Any],
        description: str = "",
        input_schema: str = "",
        output_schema: str = "",
    ) -> None:
        norm_name = spine_name.lower().strip()
        self.spines[norm_name] = factory
        self.spine_metadata[norm_name] = {
            "name": spine_name,
            "description": description,
            "input_schema": input_schema,
            "output_schema": output_schema,
        }
        logger.info(f"Registered governed spine pipeline: '{spine_name}'")

    def get_spine(self, spine_name: str, use_cache: bool = False) -> Optional[Any]:
        norm_name = spine_name.lower().strip()
        if use_cache and norm_name in self.cached_instances:
            return self.cached_instances[norm_name]

        factory = self.spines.get(norm_name)
        if not factory:
            return None

        instance = factory()
        if use_cache:
            self.cached_instances[norm_name] = instance
        return instance

    def list_spines(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": meta["name"],
                "description": meta["description"],
                "input_schema": meta["input_schema"],
                "output_schema": meta["output_schema"],
            }
            for meta in self.spine_metadata.values()
        ]
