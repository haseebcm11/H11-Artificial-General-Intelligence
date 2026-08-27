"""H11C-VERSION-ALIGNER: Version Aligner

H11C Control Plane — integrator. Thin contract over control_kernel.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, Optional

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from h11_runtime.control_kernel import ControlAgent, KernelState


AGENT_ID = "H11C-VERSION-ALIGNER"


class Agent(ControlAgent):
    def __init__(self, state: Optional[KernelState] = None) -> None:
        super().__init__(AGENT_ID, state=state or KernelState())

    def process(self, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return super().process(payload)


def create(state: Optional[KernelState] = None) -> Agent:
    return Agent(state)
