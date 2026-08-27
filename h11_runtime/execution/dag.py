"""Execution DAG data structures."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class DAGNode:
    node_id: str
    agent_id: str
    capability: str
    status: str = "PENDING"
    result: Optional[Any] = None


@dataclass
class DAGEdge:
    source: str
    target: str
