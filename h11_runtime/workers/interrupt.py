"""Interrupt handling and prioritized emergency control signals."""
from __future__ import annotations

import logging
import time
from typing import Any, Callable, Dict, List, Optional
import uuid

logger = logging.getLogger(__name__)


class InterruptHandler:
    """C02 Interrupt Handler: Priority signal dispatch and emergency control (v3.0 Section 44)."""

    def __init__(self) -> None:
        self.interrupt_listeners: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}
        self.interrupt_log: List[Dict[str, Any]] = []
        self._halt_flag: bool = False

    def register_listener(self, signal_type: str, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Registers a listener for specific interrupt signal (or '*' for all)."""
        self.interrupt_listeners.setdefault(signal_type, []).append(callback)

    def trigger_interrupt(
        self,
        signal_type: str,  # HALT_ALL, PAUSE_EXECUTION, TIMEOUT, SECURITY_BREACH, ALIGN_VIOLATION
        source: str = "KERNEL",
        reason: str = "",
        payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Dispatches an interrupt event and triggers registered handlers immediately."""
        event = {
            "interrupt_id": f"INT-{uuid.uuid4().hex[:8].upper()}",
            "signal_type": signal_type,
            "source": source,
            "reason": reason,
            "payload": payload or {},
            "timestamp": time.time(),
        }
        self.interrupt_log.append(event)
        logger.warning(f"INTERRUPT TRIGGERED [{signal_type}] from {source}: {reason}")

        if signal_type in ("HALT_ALL", "SECURITY_BREACH", "ALIGN_VIOLATION"):
            self._halt_flag = True

        for cb in self.interrupt_listeners.get(signal_type, []):
            try:
                cb(event)
            except Exception as exc:
                logger.error(f"Error in interrupt listener for {signal_type}: {exc}")

        for cb in self.interrupt_listeners.get("*", []):
            try:
                cb(event)
            except Exception as exc:
                logger.error(f"Error in global interrupt listener: {exc}")

        return event

    def is_halted(self) -> bool:
        return self._halt_flag

    def is_interrupted(self) -> bool:
        return len(self.interrupt_log) > 0 or self._halt_flag

    def reset_halt(self) -> None:
        self._halt_flag = False
