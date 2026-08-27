from __future__ import annotations

import json
import logging
import re
import uuid
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any, Tuple

logger = logging.getLogger(__name__)

@dataclass
class Entity:
    """Represents a node in the knowledge graph."""
    id: str
    name: str
    entity_type: str
    aliases: List[str] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)
    source_url: Optional[str] = None
    confidence: float = 1.0

@dataclass
class Relation:
    """Represents an edge (relation) between two entities in the knowledge graph."""
    id: str
    subject_id: str
    predicate: str
    object_id: str
    confidence: float = 1.0
    source_url: Optional[str] = None
    extracted_from: str = ""

@dataclass
class Triple:
    """A flattened representation of a subject-predicate-object triple."""
    subject: str
    predicate: str
    object: str
    confidence: float

class KnowledgeGraph:
    """A knowledge graph for entity and relation extraction and querying."""
    
    def __init__(self) -> None:
        self._entities: Dict[str, Entity] = {}
        self._relations: Dict[str, Relation] = {}
        self._adjacency_list: Dict[str, List[str]] = {} # entity_id -> list of relation_ids

    def add_entity(self, entity: Entity) -> None:
        """Adds an entity to the knowledge graph."""
        self._entities[entity.id] = entity
        if entity.id not in self._adjacency_list:
            self._adjacency_list[entity.id] = []
        logger.debug(f"Added entity: {entity.name} ({entity.entity_type})")

    def add_relation(self, relation: Relation) -> None:
        """Adds a relation to the knowledge graph."""
        self._relations[relation.id] = relation
        
        # Update adjacency list for both subject and object
        if relation.subject_id in self._adjacency_list:
            self._adjacency_list[relation.subject_id].append(relation.id)
        if relation.object_id in self._adjacency_list:
            self._adjacency_list[relation.object_id].append(relation.id)
            
        logger.debug(f"Added relation: {relation.subject_id} -[{relation.predicate}]-> {relation.object_id}")

    def extract_entities(self, text: str) -> List[Entity]:
        """
        Uses regex-based NER to extract entities from text.
        Supported types: PERSON, ORGANIZATION, LOCATION, NUMBER, DATE, URL, EMAIL.
        """
        extracted = []
        
        # PERSON: Capitalized words
        for match in re.finditer(r'\b([A-Z][a-z]+(?: [A-Z][a-z]+)+)\b', text):
            # rudimentary filter against common non-person phrases
            if not any(org_kw in match.group(1) for org_kw in ["Inc", "Corp", "Ltd", "University"]):
                extracted.append(Entity(
                    id=str(uuid.uuid4()),
                    name=match.group(1),
                    entity_type="PERSON",
                    aliases=[],
                    properties={},
                    source_url=None,
                    confidence=0.8
                ))

        # ORGANIZATION: Contains Inc, Corp, Ltd, University, etc.
        for match in re.finditer(r'\b([A-Z][a-zA-Z\s]+(?:Inc\.?|Corp\.?|Ltd\.?|University|Institute|Company))\b', text):
            extracted.append(Entity(
                id=str(uuid.uuid4()),
                name=match.group(1).strip(),
                entity_type="ORGANIZATION",
                aliases=[],
                properties={},
                source_url=None,
                confidence=0.9
            ))

        # LOCATION: Assuming basic capitalization context isn't enough, we might rely on known lists, 
        # but for this regex approach we'll look for prep + Capitalized word
        for match in re.finditer(r'\b(?:in|at|to|from) ([A-Z][a-zA-Z]+(?: [A-Z][a-zA-Z]+)?)\b', text):
            loc_candidate = match.group(1)
            # crude filter
            if loc_candidate not in ["The", "A", "An"]:
                extracted.append(Entity(
                    id=str(uuid.uuid4()),
                    name=loc_candidate,
                    entity_type="LOCATION",
                    aliases=[],
                    properties={},
                    source_url=None,
                    confidence=0.7
                ))

        # NUMBER: Digits optionally with commas/decimals
        for match in re.finditer(r'\b(\d+(?:,\d{3})*(?:\.\d+)?)\b', text):
            extracted.append(Entity(
                id=str(uuid.uuid4()),
                name=match.group(1),
                entity_type="NUMBER",
                aliases=[],
                properties={},
                source_url=None,
                confidence=0.95
            ))
            
        # URL
        for match in re.finditer(r'\b(https?://[^\s]+)\b', text):
            extracted.append(Entity(
                id=str(uuid.uuid4()),
                name=match.group(1),
                entity_type="URL",
                aliases=[],
                properties={},
                source_url=None,
                confidence=1.0
            ))
            
        # EMAIL
        for match in re.finditer(r'\b([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)\b', text):
            extracted.append(Entity(
                id=str(uuid.uuid4()),
                name=match.group(1),
                entity_type="EMAIL",
                aliases=[],
                properties={},
                source_url=None,
                confidence=1.0
            ))

        # DATE: Basic YYYY-MM-DD or Month DD, YYYY
        for match in re.finditer(r'\b(\d{4}-\d{2}-\d{2}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4})\b', text):
            extracted.append(Entity(
                id=str(uuid.uuid4()),
                name=match.group(1),
                entity_type="DATE",
                aliases=[],
                properties={},
                source_url=None,
                confidence=0.9
            ))
            
        return extracted

    def extract_relations(self, text: str, entities: List[Entity]) -> List[Relation]:
        """
        Pattern-based relation extraction using dependency-like patterns.
        """
        relations = []
        
        # Sort entities by position in text (simplified: just iterate pairs)
        # In a real scenario, we'd map entity text back to offsets.
        # For this rule-based approach, we find patterns in the raw text and map back to provided entities.
        
        patterns = [
            (r'(.+?) is an? (.+?)(?:\.|$)', 'IS_A'),
            (r'(.+?) causes (.+?)(?:\.|$)', 'CAUSES'),
            (r'(.+?) treats (.+?)(?:\.|$)', 'TREATS'),
            (r'(.+?) contains (.+?)(?:\.|$)', 'CONTAINS'),
            (r'(.+?) discovered (.+?)(?:\.|$)', 'DISCOVERED'),
            (r'(.+?) located in (.+?)(?:\.|$)', 'LOCATED_IN'),
        ]
        
        # Create a name to entity ID mapping for quick lookup
        name_to_id = {e.name.lower(): e.id for e in entities}
        
        for pattern, predicate in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                subj_text = match.group(1).strip().lower()
                obj_text = match.group(2).strip().lower()
                
                # Try to find matching entities
                subj_id = None
                obj_id = None
                
                for name, e_id in name_to_id.items():
                    if name in subj_text:
                        subj_id = e_id
                    if name in obj_text:
                        obj_id = e_id
                        
                if subj_id and obj_id and subj_id != obj_id:
                    rel = Relation(
                        id=str(uuid.uuid4()),
                        subject_id=subj_id,
                        predicate=predicate,
                        object_id=obj_id,
                        confidence=0.8,
                        source_url=None,
                        extracted_from=match.group(0)
                    )
                    relations.append(rel)
                    
        return relations

    def query(self, subject: Optional[str] = None, predicate: Optional[str] = None, object: Optional[str] = None) -> List[Triple]:
        """Queries the knowledge graph for matching triples."""
        results = []
        for rel in self._relations.values():
            subj_entity = self._entities.get(rel.subject_id)
            obj_entity = self._entities.get(rel.object_id)
            
            if not subj_entity or not obj_entity:
                continue
                
            subj_name = subj_entity.name
            obj_name = obj_entity.name
            
            if subject and subject.lower() not in subj_name.lower():
                continue
            if predicate and predicate.lower() != rel.predicate.lower():
                continue
            if object and object.lower() not in obj_name.lower():
                continue
                
            results.append(Triple(
                subject=subj_name,
                predicate=rel.predicate,
                object=obj_name,
                confidence=rel.confidence
            ))
            
        return results

    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """Retrieves an entity by its ID."""
        return self._entities.get(entity_id)

    def get_neighbors(self, entity_id: str, max_hops: int = 2) -> Dict[str, List[Relation]]:
        """
        Gets neighboring entities within max_hops.
        Returns a dictionary mapping entity IDs to a list of connecting relations.
        (Simplified implementation supporting max_hops=1 for direct neighbors)
        """
        # Note: True multi-hop would require BFS, implementing 1-hop for simplicity 
        # and outlining structure.
        neighbors: Dict[str, List[Relation]] = {}
        
        if entity_id not in self._adjacency_list:
            return neighbors
            
        visited = {entity_id}
        queue = [(entity_id, 0)]
        
        while queue:
            curr_node, depth = queue.pop(0)
            
            if depth >= max_hops:
                continue
                
            for rel_id in self._adjacency_list.get(curr_node, []):
                rel = self._relations[rel_id]
                
                neighbor_id = rel.object_id if rel.subject_id == curr_node else rel.subject_id
                
                if neighbor_id not in neighbors:
                    neighbors[neighbor_id] = []
                neighbors[neighbor_id].append(rel)
                
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    queue.append((neighbor_id, depth + 1))
                    
        return neighbors

    def save(self, path: str) -> None:
        """Saves the knowledge graph to a JSON file."""
        data = {
            "entities": [asdict(e) for e in self._entities.values()],
            "relations": [asdict(r) for r in self._relations.values()]
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Knowledge graph saved to {path}")

    @classmethod
    def load(cls, path: str) -> KnowledgeGraph:
        """Loads a knowledge graph from a JSON file."""
        kg = cls()
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for e_data in data.get("entities", []):
            kg.add_entity(Entity(**e_data))
            
        for r_data in data.get("relations", []):
            kg.add_relation(Relation(**r_data))
            
        logger.info(f"Knowledge graph loaded from {path}")
        return kg

    @property
    def stats(self) -> Dict[str, int]:
        """Returns statistics about the knowledge graph."""
        entity_types = set(e.entity_type for e in self._entities.values())
        return {
            "num_entities": len(self._entities),
            "num_relations": len(self._relations),
            "num_entity_types": len(entity_types)
        }
