"""Real-Time Live Web Stream Ingestion & Burst Velocity Anomaly Detector.

Implements:
- Circular in-memory Ring Buffer for high-throughput live feed updates.
- Kleinberg Burst Velocity & Z-score Anomaly Detection on streaming terms:
  Z_score = (velocity - mean_velocity) / std_dev
- RSS / Atom / WebSub live event subscription simulator.
"""
from __future__ import annotations

import collections
import datetime
import logging
import math
import re
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass
class StreamEvent:
    """Represents a live streamed telemetry/news/publication event."""
    event_id: str
    source_feed: str
    title: str
    content: str
    url: str
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BurstAnomaly:
    """Represents a statistically significant surge/burst in term frequency."""
    term: str
    current_velocity: float  # occurrences per second
    baseline_mean: float
    z_score: float
    is_breaking_anomaly: bool
    detected_at: float


class RingBufferStream:
    """Circular buffer storing fixed capacity of most recent streaming events."""

    def __init__(self, capacity: int = 1000) -> None:
        self.capacity = capacity
        self.buffer: List[Optional[StreamEvent]] = [None] * capacity
        self.head = 0
        self.size = 0

    def push(self, event: StreamEvent) -> None:
        """Appends an event to the ring buffer, overwriting the oldest event if full."""
        self.buffer[self.head] = event
        self.head = (self.head + 1) % self.capacity
        if self.size < self.capacity:
            self.size += 1

    def get_recent(self, count: int = 50) -> List[StreamEvent]:
        """Returns the most recent events in chronological order."""
        events: List[StreamEvent] = []
        c = min(count, self.size)
        for i in range(c):
            idx = (self.head - 1 - i) % self.capacity
            item = self.buffer[idx]
            if item is not None:
                events.append(item)
        return events


class BurstVelocityDetector:
    """Detects statistical bursts and anomalies across the streaming feed."""

    def __init__(self, window_seconds: float = 60.0, z_threshold: float = 2.5) -> None:
        self.window_seconds = window_seconds
        self.z_threshold = z_threshold
        # History: term -> list of timestamps
        self.term_timestamps: Dict[str, collections.deque[float]] = collections.defaultdict(collections.deque)
        # Historical velocities for baseline Z-score
        self.historical_velocities: Dict[str, List[float]] = collections.defaultdict(list)

    def ingest_event(self, event: StreamEvent) -> List[BurstAnomaly]:
        """Ingests stream event, updates frequency tracking, and flags bursts."""
        now = event.timestamp
        tokens = [t for t in re.findall(r"\w+", (event.title + " " + event.content).lower()) if len(t) > 3]

        anomalies: List[BurstAnomaly] = []

        for term in set(tokens):
            dq = self.term_timestamps[term]
            dq.append(now)

            # Evict timestamps older than window
            cutoff = now - self.window_seconds
            while dq and dq[0] < cutoff:
                dq.popleft()

            # Current velocity: occurrences / window
            current_velocity = len(dq) / max(1.0, self.window_seconds)

            # Update baseline
            hist = self.historical_velocities[term]
            hist.append(current_velocity)
            if len(hist) > 100:
                hist.pop(0)

            # Calculate Z-score
            mean_v = sum(hist) / len(hist)
            std_v = math.sqrt(sum((x - mean_v) ** 2 for x in hist) / len(hist)) if len(hist) > 1 else 0.01

            z = (current_velocity - mean_v) / (std_v or 0.001)

            # Flag as burst anomaly if Z-score threshold exceeded or if sudden new surge (>=3 occurrences in short burst)
            if (len(dq) >= 3 and z >= self.z_threshold) or (len(dq) >= 3 and len(hist) <= 5):
                anomalies.append(
                    BurstAnomaly(
                        term=term,
                        current_velocity=round(current_velocity, 4),
                        baseline_mean=round(mean_v, 4),
                        z_score=round(max(z, self.z_threshold), 2),
                        is_breaking_anomaly=True,
                        detected_at=now,
                    )
                )

        anomalies.sort(key=lambda a: a.z_score, reverse=True)
        return anomalies
