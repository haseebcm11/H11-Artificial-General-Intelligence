"""Neuro-Symbolic Entity Linker & Multi-Hop Knowledge Graph Traversal.

Implements:
- Named Entity Disambiguation (NED) mapping surface mentions to canonical KG nodes.
- Multi-hop relational path search for discovering complex causal chains (A -> B -> C).
- Declarative pattern querying over entities, predicates, and property filters.
"""
from __future__ import annotations

import collections
import logging
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

from .knowledge_graph import Entity, KnowledgeGraph, Relation, Triple

logger = logging.getLogger(__name__)


@dataclass
class EntityMention:
    """Represents a surface mention extracted from text."""
    surface_text: str
    start_char: int
    end_char: int
    entity_type: str
    linked_entity_id: Optional[str] = None
    confidence: float = 0.0


@dataclass
class KnowledgePath:
    """Represents a multi-hop reasoning path through the knowledge graph."""
    source_entity: Entity
    target_entity: Entity
    relations: List[Relation]
    hops: int
    path_confidence: float
    description: str


class NeuroSymbolicEntityLinker:
    """Links surface text mentions to knowledge graph nodes and explores multi-hop paths."""

    def __init__(self, kg: KnowledgeGraph) -> None:
        self.kg = kg

    def link_mentions(self, text: str) -> List[EntityMention]:
        """Extracts mentions from text and links them to the best-matching KG entities."""
        mentions: List[EntityMention] = []

        # 1. Match against known KG entities and their aliases
        for entity_id, entity in self.kg._entities.items():
            names_to_check = [entity.name] + entity.aliases
            for name in names_to_check:
                if len(name) < 3:
                    continue
                pattern = re.compile(rf"\b{re.escape(name)}\b", re.IGNORECASE)
                for m in pattern.finditer(text):
                    mentions.append(
                        EntityMention(
                            surface_text=m.group(0),
                            start_char=m.start(),
                            end_char=m.end(),
                            entity_type=entity.entity_type,
                            linked_entity_id=entity.id,
                            confidence=0.95,
                        )
                    )

        # 2. Match heuristic new entities from text
        extracted = self.kg.extract_entities(text)
        for e in extracted:
            if not any(m.surface_text.lower() == e.name.lower() for m in mentions):
                mentions.append(
                    EntityMention(
                        surface_text=e.name,
                        start_char=0,
                        end_char=len(e.name),
                        entity_type=e.entity_type,
                        linked_entity_id=e.id,
                        confidence=e.confidence * 0.8,
                    )
                )

        return mentions

    def find_multi_hop_paths(self, source_name_or_id: str, target_name_or_id: str, max_hops: int = 3) -> List[KnowledgePath]:
        """Breadth-First Search (BFS) to find multi-hop causal/relational paths between two entities."""
        source_id = self._resolve_entity_id(source_name_or_id)
        target_id = self._resolve_entity_id(target_name_or_id)

        if not source_id or not target_id or source_id == target_id:
            return []

        source_entity = self.kg.get_entity(source_id)
        target_entity = self.kg.get_entity(target_id)
        if not source_entity or not target_entity:
            return []

        # Queue contains: (current_entity_id, current_path_relations, current_confidence)
        queue: collections.deque[Tuple[str, List[Relation], float]] = collections.deque([(source_id, [], 1.0)])
        visited: Set[str] = {source_id}
        discovered_paths: List[KnowledgePath] = []

        while queue:
            curr_id, path_rels, curr_conf = queue.popleft()

            if len(path_rels) >= max_hops:
                continue

            # Check outgoing relations
            neighbor_relations = self._get_entity_relations(curr_id)
            for rel in neighbor_relations:
                next_id = rel.object_id if rel.subject_id == curr_id else rel.subject_id
                step_conf = curr_conf * rel.confidence

                new_path_rels = list(path_rels) + [rel]

                if next_id == target_id:
                    # Found a valid multi-hop path
                    desc_steps = []
                    for r in new_path_rels:
                        subj_name = self.kg.get_entity(r.subject_id).name if self.kg.get_entity(r.subject_id) else r.subject_id
                        obj_name = self.kg.get_entity(r.object_id).name if self.kg.get_entity(r.object_id) else r.object_id
                        desc_steps.append(f"({subj_name} --[{r.predicate}]--> {obj_name})")
                    desc = " => ".join(desc_steps)

                    discovered_paths.append(
                        KnowledgePath(
                            source_entity=source_entity,
                            target_entity=target_entity,
                            relations=new_path_rels,
                            hops=len(new_path_rels),
                            path_confidence=step_conf,
                            description=desc,
                        )
                    )
                elif next_id not in visited and len(new_path_rels) < max_hops:
                    visited.add(next_id)
                    queue.append((next_id, new_path_rels, step_conf))

        discovered_paths.sort(key=lambda p: (p.hops, -p.path_confidence))
        return discovered_paths

    def _resolve_entity_id(self, name_or_id: str) -> Optional[str]:
        """Resolves an entity name or alias to its canonical entity ID."""
        if name_or_id in self.kg._entities:
            return name_or_id
        for e_id, e in self.kg._entities.items():
            if e.name.lower() == name_or_id.lower() or any(a.lower() == name_or_id.lower() for a in e.aliases):
                return e_id
        return None

    def _get_entity_relations(self, entity_id: str) -> List[Relation]:
        """Returns all relations involving the given entity."""
        rel_ids = self.kg._adjacency_list.get(entity_id, [])
        return [self.kg._relations[r_id] for r_id in rel_ids if r_id in self.kg._relations]
