"""H11-AGI Conversational Reasoning & Chat Server Subsystem.

Provides:
- `ConversationalReasoner`: Master multi-agent conversational reasoning engine
- `ChatResponse`: Structured reasoning trace and answer response container
- `app`: Production FastAPI / WebSocket application
"""
from __future__ import annotations

from .chat_engine import ChatResponse, ConversationalReasoner, ReasoningStep

__all__ = [
    "ConversationalReasoner",
    "ChatResponse",
    "ReasoningStep",
]
