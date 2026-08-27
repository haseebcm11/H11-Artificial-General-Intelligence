"""Asynchronous EventBus."""
from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

from .event import RuntimeEvent


class EventBus:
    """13 — H11C-EVENT-BUS: Asynchronous event transport separating events from data."""

    def __init__(self) -> None:
        self.subscribers: Dict[str, List[Callable[[RuntimeEvent], None]]] = {}
        self.event_history: List[RuntimeEvent] = []

    def subscribe(self, topic_or_event_name: str, handler: Callable[[RuntimeEvent], None]) -> None:
        if topic_or_event_name not in self.subscribers:
            self.subscribers[topic_or_event_name] = []
        self.subscribers[topic_or_event_name].append(handler)

    def publish(
        self,
        event_name_or_topic: str,
        case_id_or_payload: Any = None,
        payload: Optional[Dict[str, Any]] = None,
        source: str = "KERNEL",
    ) -> RuntimeEvent:
        if payload is not None and isinstance(case_id_or_payload, str):
            case_id = case_id_or_payload
            actual_payload = payload
        elif isinstance(case_id_or_payload, dict):
            case_id = ""
            actual_payload = case_id_or_payload
        else:
            case_id = str(case_id_or_payload) if case_id_or_payload else ""
            actual_payload = {}

        evt = RuntimeEvent(
            event_name=event_name_or_topic,
            topic=event_name_or_topic,
            case_id=case_id,
            payload=actual_payload,
            source=source,
        )
        self.event_history.append(evt)
        for h in self.subscribers.get(event_name_or_topic, []):
            h(evt)
        for h in self.subscribers.get("*", []):
            h(evt)
        return evt
