"""
H11-SPATIAL: Spatial Perception
Layer 11 - Perception & Sensing
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Set
from enum import Enum

class ReferenceFrame(Enum):
    EGOCENTRIC = "egocentric"    # Camera/Robot local frame
    ALLOCENTRIC = "allocentric"  # World global frame

@dataclass
class Pose3D:
    """Represents a 3D pose using translation and quaternion (x, y, z, w)."""
    translation: np.ndarray  # Shape: (3,)
    quaternion: np.ndarray   # Shape: (4,) - [x, y, z, w]
    
    def to_matrix(self) -> np.ndarray:
        """Convert to 4x4 homogenous transformation matrix."""
        mat = np.eye(4)
        mat[:3, 3] = self.translation
        
        q = self.quaternion
        # Quaternion to rotation matrix conversion
        mat[0, 0] = 1 - 2*q[1]**2 - 2*q[2]**2
        mat[0, 1] = 2*q[0]*q[1] - 2*q[2]*q[3]
        mat[0, 2] = 2*q[0]*q[2] + 2*q[1]*q[3]
        
        mat[1, 0] = 2*q[0]*q[1] + 2*q[2]*q[3]
        mat[1, 1] = 1 - 2*q[0]**2 - 2*q[2]**2
        mat[1, 2] = 2*q[1]*q[2] - 2*q[0]*q[3]
        
        mat[2, 0] = 2*q[0]*q[2] - 2*q[1]*q[3]
        mat[2, 1] = 2*q[1]*q[2] + 2*q[0]*q[3]
        mat[2, 2] = 1 - 2*q[0]**2 - 2*q[1]**2
        return mat

@dataclass
class BoundingBox3D:
    center: np.ndarray      # (3,)
    dimensions: np.ndarray  # (3,) [width, height, depth]
    orientation: np.ndarray # (4,) quaternion

@dataclass
class SpatialNode:
    node_id: str
    semantic_label: str
    pose: Pose3D
    bbox: Optional[BoundingBox3D] = None
    confidence: float = 1.0
    dynamic: bool = False
    velocity: Optional[np.ndarray] = None # (3,)

class SpatialRelation(Enum):
    ON_TOP_OF = "on_top_of"
    UNDER = "under"
    INSIDE = "inside"
    NEXT_TO = "next_to"
    IN_FRONT_OF = "in_front_of"
    BEHIND = "behind"

@dataclass
class SceneGraphEdge:
    source_id: str
    target_id: str
    relation: SpatialRelation
    distance: float
    confidence: float

@dataclass
class SceneGraph:
    nodes: Dict[str, SpatialNode] = field(default_factory=dict)
    edges: List[SceneGraphEdge] = field(default_factory=list)
    
    def add_node(self, node: SpatialNode):
        self.nodes[node.node_id] = node
        
    def add_edge(self, edge: SceneGraphEdge):
        self.edges.append(edge)

class OccupancyGrid:
    """Probabilistic 3D Voxel Grid."""
    def __init__(self, resolution: float = 0.05, bounds: Tuple[float, float, float] = (10.0, 10.0, 5.0)):
        self.resolution = resolution
        self.bounds = bounds
        self.grid_shape = (
            int(bounds[0] * 2 / resolution),
            int(bounds[1] * 2 / resolution),
            int(bounds[2] / resolution)
        )
        # Using log-odds for occupancy
        self.log_odds = np.zeros(self.grid_shape, dtype=np.float32)
        
        self.l_occ = 0.85
        self.l_free = -0.4
        self.l_min = -2.0
        self.l_max = 3.5

    def update_from_points(self, points: np.ndarray, origin: np.ndarray):
        """Raytrace from origin to points to update free/occupied space. (Simplified)"""
        # Convert points to grid indices
        # In a real implementation, this would use Bresenham's 3D or ray casting
        for pt in points:
            idx = self._point_to_idx(pt)
            if self._in_bounds(idx):
                self.log_odds[idx] += self.l_occ
                self.log_odds[idx] = min(self.log_odds[idx], self.l_max)
                
    def _point_to_idx(self, pt: np.ndarray) -> Tuple[int, int, int]:
        x = int((pt[0] + self.bounds[0]) / self.resolution)
        y = int((pt[1] + self.bounds[1]) / self.resolution)
        z = int(pt[2] / self.resolution)
        return (x, y, z)
        
    def _in_bounds(self, idx: Tuple[int, int, int]) -> bool:
        return (0 <= idx[0] < self.grid_shape[0] and 
                0 <= idx[1] < self.grid_shape[1] and 
                0 <= idx[2] < self.grid_shape[2])

class SpatialReasoningEngine:
    def __init__(self):
        self.distance_threshold = 1.5 # meters
        
    def extract_relationships(self, nodes: Dict[str, SpatialNode]) -> List[SceneGraphEdge]:
        edges = []
        node_list = list(nodes.values())
        
        for i in range(len(node_list)):
            for j in range(i + 1, len(node_list)):
                n1, n2 = node_list[i], node_list[j]
                
                delta = n1.pose.translation - n2.pose.translation
                dist = np.linalg.norm(delta)
                
                if dist > self.distance_threshold:
                    continue
                    
                # Basic geometric heuristics for relations
                dz = delta[2]
                
                # If n1 is significantly higher than n2
                if dz > 0.2 and abs(delta[0]) < 0.3 and abs(delta[1]) < 0.3:
                    edges.append(SceneGraphEdge(n1.node_id, n2.node_id, SpatialRelation.ON_TOP_OF, dist, 0.8))
                elif dz < -0.2 and abs(delta[0]) < 0.3 and abs(delta[1]) < 0.3:
                    edges.append(SceneGraphEdge(n1.node_id, n2.node_id, SpatialRelation.UNDER, dist, 0.8))
                else:
                    edges.append(SceneGraphEdge(n1.node_id, n2.node_id, SpatialRelation.NEXT_TO, dist, 0.5))
                    
        return edges

class SpatialPerceptionAgent:
    """
    H11-SPATIAL Agent
    Maintains 3D scene graphs and occupancy maps from spatial inputs.
    """
    def __init__(self):
        self.occupancy_grid = OccupancyGrid(resolution=0.1)
        self.scene_graph = SceneGraph()
        self.reasoner = SpatialReasoningEngine()
        self.frame_tracker = {}
        
    def process_spatial_update(self, 
                             point_cloud: np.ndarray, 
                             sensor_pose: Pose3D,
                             detected_objects: List[SpatialNode]) -> SceneGraph:
        """
        Integrates new spatial data into the global allocentric map.
        """
        # 1. Update Occupancy Grid
        # Transform points from egocentric to allocentric
        sensor_mat = sensor_pose.to_matrix()
        # Homogenous coords
        pc_h = np.hstack((point_cloud, np.ones((point_cloud.shape[0], 1))))
        pc_global = (sensor_mat @ pc_h.T).T[:, :3]
        
        self.occupancy_grid.update_from_points(pc_global, sensor_pose.translation)
        
        # 2. Update Scene Graph Nodes
        for obj in detected_objects:
            # Simple identity tracking based on ID (real impl uses Kalman/SORT)
            self.scene_graph.add_node(obj)
            
        # 3. Re-evaluate Spatial Relationships
        new_edges = self.reasoner.extract_relationships(self.scene_graph.nodes)
        self.scene_graph.edges = new_edges
        
        return self.scene_graph

    def get_spatial_context(self) -> Dict:
        return {
            "node_count": len(self.scene_graph.nodes),
            "edge_count": len(self.scene_graph.edges),
            "grid_size": self.occupancy_grid.grid_shape,
            "relationships": [
                f"{e.source_id} is {e.relation.value} {e.target_id}" 
                for e in self.scene_graph.edges[:10]
            ]
        }
