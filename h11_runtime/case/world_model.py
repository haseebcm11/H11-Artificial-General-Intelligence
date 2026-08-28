"""Explicit World State and Cognitive Case Model (v3.0 Section 11)."""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple
import uuid

logger = logging.getLogger(__name__)


@dataclass
class WorldEntity:
    entity_id: str
    name: str
    entity_type: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0
    first_observed: float = field(default_factory=time.time)
    last_updated: float = field(default_factory=time.time)


@dataclass
class WorldRelation:
    relation_id: str
    subject_id: str
    predicate: str
    object_id: str
    confidence: float = 1.0
    evidence_ids: List[str] = field(default_factory=list)


@dataclass
class WorldEvent:
    event_id: str
    name: str
    timestamp: float
    actors: List[str] = field(default_factory=list)
    description: str = ""
    causal_factors: List[str] = field(default_factory=list)
    consequences: List[str] = field(default_factory=list)


@dataclass
class Hypothesis:
    hypothesis_id: str
    statement: str
    confidence: float = 0.5
    supporting_evidence: List[str] = field(default_factory=list)
    refuting_evidence: List[str] = field(default_factory=list)
    status: str = "PROPOSED"  # PROPOSED, SUPPORTED, REFUTED, ADOPTED


class WorldModel:
    """11 — WorldModel: Authoritative dynamic world and case state representation."""

    def __init__(self, case_id: str = "") -> None:
        self.case_id = case_id
        self.entities: Dict[str, WorldEntity] = {}
        self.relations: Dict[str, WorldRelation] = {}
        self.events: List[WorldEvent] = []
        self.hypotheses: Dict[str, Hypothesis] = {}
        self.beliefs: Dict[str, Any] = {}
        self.observations: List[Dict[str, Any]] = []
        self.temporal_index: Dict[float, str] = {}
        self.causal_graph: Dict[str, List[str]] = {}

    def add_entity(self, name: str, entity_type: str, attributes: Optional[Dict[str, Any]] = None, entity_id: str = "") -> WorldEntity:
        eid = entity_id or f"ENT-{name.upper().replace(' ', '_')}"
        entity = WorldEntity(
            entity_id=eid,
            name=name,
            entity_type=entity_type,
            attributes=attributes or {},
            last_updated=time.time(),
        )
        self.entities[eid] = entity
        return entity

    def add_relation(self, subject_id: str, predicate: str, object_id: str, confidence: float = 1.0) -> WorldRelation:
        rid = f"REL-{uuid.uuid4().hex[:8].upper()}"
        rel = WorldRelation(
            relation_id=rid,
            subject_id=subject_id,
            predicate=predicate,
            object_id=object_id,
            confidence=confidence,
        )
        self.relations[rid] = rel
        return rel

    def add_observation(self, source_agent: str, data: Any, timestamp: Optional[float] = None) -> None:
        ts = timestamp or time.time()
        obs = {
            "obs_id": f"OBS-{uuid.uuid4().hex[:8].upper()}",
            "source": source_agent,
            "data": data,
            "timestamp": ts,
        }
        self.observations.append(obs)
        self.temporal_index[ts] = obs["obs_id"]

    def propose_hypothesis(self, statement: str, initial_confidence: float = 0.5) -> Hypothesis:
        hid = f"HYP-{uuid.uuid4().hex[:8].upper()}"
        hyp = Hypothesis(hypothesis_id=hid, statement=statement, confidence=initial_confidence)
        self.hypotheses[hid] = hyp
        return hyp

    def update_hypothesis(self, hypothesis_id: str, evidence_id: str, supports: bool, weight: float = 0.1) -> None:
        if hypothesis_id not in self.hypotheses:
            return
        hyp = self.hypotheses[hypothesis_id]
        if supports:
            hyp.supporting_evidence.append(evidence_id)
            hyp.confidence = min(1.0, hyp.confidence + weight)
            if hyp.confidence >= 0.8:
                hyp.status = "SUPPORTED"
        else:
            hyp.refuting_evidence.append(evidence_id)
            hyp.confidence = max(0.0, hyp.confidence - weight)
            if hyp.confidence <= 0.2:
                hyp.status = "REFUTED"

    def record_causal_link(self, cause_event_or_entity: str, effect_event_or_entity: str) -> None:
        if cause_event_or_entity not in self.causal_graph:
            self.causal_graph[cause_event_or_entity] = []
        self.causal_graph[cause_event_or_entity].append(effect_event_or_entity)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "case_id": self.case_id,
            "entities_count": len(self.entities),
            "relations_count": len(self.relations),
            "events_count": len(self.events),
            "hypotheses": {hid: {"statement": h.statement, "confidence": h.confidence, "status": h.status} for hid, h in self.hypotheses.items()},
            "beliefs_count": len(self.beliefs),
            "observations_count": len(self.observations),
        }
