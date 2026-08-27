"""Interrupt handler."""
class InterruptHandler:
    """C02 Interruptibility: Enables safe interruption, replanning, and halting (Section 47)."""

    def __init__(self) -> None:
        self._interrupted = False
        self._reason = ""

    def trigger_interrupt(self, reason: str = "User/System Interrupt") -> None:
        self._interrupted = True
        self._reason = reason

    def is_interrupted(self) -> bool:
        return self._interrupted

    def reset(self) -> None:
        self._interrupted = False
        self._reason = ""
