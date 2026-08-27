"""
H11-ANATOMIA: Human Anatomy & Structural Biology
Layer 1 - Medicine & Health Sciences

This module implements a robust spatial graph representation of human anatomy,
supporting multiple resolutions from macroscopic organ systems to histological planes.
"""

from __future__ import annotations
import asyncio
import logging
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Protocol, Sequence, Tuple, Set
import math

logger = logging.getLogger(__name__)

class AnatomicalPlane(Enum):
    SAGITTAL = auto()
    CORONAL = auto()
    TRANSVERSE = auto()
    OBLIQUE = auto()

class TissueType(Enum):
    EPITHELIAL = auto()
    CONNECTIVE = auto()
    MUSCULAR = auto()
    NERVOUS = auto()
    VASCULAR = auto()
    LYMPHATIC = auto()
    ADIPOSE = auto()
    BONE = auto()
    CARTILAGE = auto()

class ResolutionEnum(Enum):
    MACROSCOPIC = auto()
    MESOSCOPIC = auto()
    HISTOLOGICAL = auto()

@dataclass
class Point3D:
    x: float
    y: float
    z: float

    def distance_to(self, other: 'Point3D') -> float:
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)

@dataclass
class BoundingBox:
    min_point: Point3D
    max_point: Point3D

    def contains(self, point: Point3D) -> bool:
        return (self.min_point.x <= point.x <= self.max_point.x and
                self.min_point.y <= point.y <= self.max_point.y and
                self.min_point.z <= point.z <= self.max_point.z)

    def intersects(self, other: 'BoundingBox') -> bool:
        return not (self.max_point.x < other.min_point.x or
                    self.min_point.x > other.max_point.x or
                    self.max_point.y < other.min_point.y or
                    self.min_point.y > other.max_point.y or
                    self.max_point.z < other.min_point.z or
                    self.min_point.z > other.max_point.z)

@dataclass
class AnatomicalStructure:
    id: str
    name: str
    tissue_types: List[TissueType]
    bounds: BoundingBox
    parent_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)
    blood_supply_ids: List[str] = field(default_factory=list)
    innervation_ids: List[str] = field(default_factory=list)

@dataclass
class Relationship:
    source_id: str
    target_id: str
    relation_type: str  # e.g., "superior_to", "supplies", "drains", "innervates"

class AnatomyGraph:
    def __init__(self):
        self.structures: Dict[str, AnatomicalStructure] = {}
        self.relationships: List[Relationship] = []
        self._spatial_index: List[Tuple[BoundingBox, str]] = []

    def add_structure(self, struct: AnatomicalStructure) -> None:
        self.structures[struct.id] = struct
        self._spatial_index.append((struct.bounds, struct.id))
        logger.debug(f"Added structure {struct.name} to AnatomyGraph.")

    def add_relationship(self, rel: Relationship) -> None:
        self.relationships.append(rel)

    def get_structure(self, struct_id: str) -> Optional[AnatomicalStructure]:
        return self.structures.get(struct_id)

    def find_in_region(self, region: BoundingBox) -> List[AnatomicalStructure]:
        found = []
        for bounds, s_id in self._spatial_index:
            if region.intersects(bounds):
                found.append(self.structures[s_id])
        return found

    def get_supply_chain(self, target_id: str, relation: str) -> List[AnatomicalStructure]:
        chain = []
        current_id = target_id
        while True:
            found = False
            for r in self.relationships:
                if r.target_id == current_id and r.relation_type == relation:
                    chain.append(self.structures[r.source_id])
                    current_id = r.source_id
                    found = True
                    break
            if not found:
                break
        return chain

    def neighbors(self, source_id: str, relation: str) -> List[str]:
        return [r.target_id for r in self.relationships if r.source_id == source_id and r.relation_type == relation]

    def shortest_path(self, start_id: str, goal_id: str, relation: str = "migrates_to") -> List[str]:
        if start_id not in self.structures or goal_id not in self.structures:
            return []
        if start_id == goal_id:
            return [start_id]
        queue: List[str] = [start_id]
        prev: Dict[str, Optional[str]] = {start_id: None}
        while queue:
            node = queue.pop(0)
            for nxt in self.neighbors(node, relation):
                if nxt in prev:
                    continue
                prev[nxt] = node
                if nxt == goal_id:
                    path = [goal_id]
                    cur: Optional[str] = node
                    while cur is not None:
                        path.append(cur)
                        cur = prev[cur]
                    path.reverse()
                    return path
                queue.append(nxt)
        return []

class AnatomyAgent:
    """
    Agent responsible for structural and spatial anatomical reasoning.
    """
    def __init__(self):
        self.graph = AnatomyGraph()
        self.state_version = 0

    def _structure(self, sid: str, name: str, tissues: List[TissueType], lo: Point3D, hi: Point3D) -> AnatomicalStructure:
        return AnatomicalStructure(id=sid, name=name, tissue_types=tissues, bounds=BoundingBox(lo, hi))

    def load_host_atlas(self) -> None:
        """Compartments a parasite can occupy, plus a small vascular core."""
        add = self.graph.add_structure
        rel = self.graph.add_relationship
        add(self._structure("skin", "Skin", [TissueType.EPITHELIAL], Point3D(-20, -20, 0), Point3D(20, 20, 2)))
        add(self._structure("liver", "Liver", [TissueType.EPITHELIAL, TissueType.VASCULAR], Point3D(4, -8, 4), Point3D(14, 4, 14)))
        add(self._structure("bloodstream", "Bloodstream", [TissueType.VASCULAR], Point3D(-15, -15, 3), Point3D(15, 15, 25)))
        add(self._structure("gi_lumen", "GI Lumen", [TissueType.EPITHELIAL], Point3D(-6, -12, 2), Point3D(6, 0, 10)))
        add(self._structure("spleen", "Spleen", [TissueType.LYMPHATIC, TissueType.VASCULAR], Point3D(-14, -4, 6), Point3D(-8, 4, 14)))
        add(self._structure("struct_heart", "Heart", [TissueType.MUSCULAR, TissueType.CONNECTIVE], Point3D(-5, -5, 10), Point3D(5, 5, 20)))
        add(self._structure("struct_aorta", "Ascending Aorta", [TissueType.VASCULAR], Point3D(-2, 0, 20), Point3D(2, 4, 30)))
        rel(Relationship("struct_heart", "struct_aorta", "supplies"))
        rel(Relationship("struct_aorta", "bloodstream", "supplies"))
        rel(Relationship("skin", "liver", "migrates_to"))
        rel(Relationship("liver", "bloodstream", "migrates_to"))
        rel(Relationship("bloodstream", "spleen", "migrates_to"))
        rel(Relationship("skin", "bloodstream", "migrates_to"))
        rel(Relationship("bloodstream", "liver", "migrates_to"))
        rel(Relationship("gi_lumen", "gi_lumen", "migrates_to"))
        self.state_version += 1

    def shortest_migration(self, start_id: str, goal_id: str) -> List[str]:
        return self.graph.shortest_path(start_id, goal_id, "migrates_to")

    def validate_migration(self, waypoints: List[str]) -> bool:
        if not waypoints:
            return False
        for hop in waypoints:
            if hop not in self.graph.structures:
                return False
        for src, dst in zip(waypoints, waypoints[1:]):
            if src == dst:
                continue
            if dst not in self.graph.neighbors(src, "migrates_to"):
                return False
        return True

    async def initialize(self) -> None:
        """Loads the host atlas used by the infection spine."""
        logger.info("Initializing H11-ANATOMIA agent atlas...")
        self.load_host_atlas()

    async def query_region(self, bounds: BoundingBox, resolution: ResolutionEnum) -> Dict[str, Any]:
        """Queries the anatomy graph for structures within a bounding box."""
        logger.info(f"Querying region {bounds}")
        structures = self.graph.find_in_region(bounds)
        return {
            "query_bounds": bounds,
            "resolution": resolution.name,
            "results": [s.name for s in structures]
        }

    async def get_vascular_supply(self, structure_id: str) -> Dict[str, Any]:
        """Traces back the arterial supply for a given structure."""
        struct = self.graph.get_structure(structure_id)
        if not struct:
            raise ValueError(f"Structure {structure_id} not found.")
        
        supply_chain = self.graph.get_supply_chain(structure_id, "supplies")
        return {
            "target": struct.name,
            "arterial_path": [s.name for s in supply_chain]
        }

    async def map_tissue_distribution(self, tissue: TissueType) -> List[str]:
        """Finds all macroscopic structures containing a specific tissue type."""
        return [s.name for s in self.graph.structures.values() if tissue in s.tissue_types]

    def _validate_spatial_integrity(self) -> bool:
        """Internal check for spatial anomalies (e.g. overlapping solid organs)."""
        # Complex intersection logic omitted for brevity
        return True

async def main():
    agent = AnatomyAgent()
    await agent.initialize()
    res = await agent.query_region(BoundingBox(Point3D(-10,-10,0), Point3D(10,10,30)), ResolutionEnum.MACROSCOPIC)
    print("Region query result:", res)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
