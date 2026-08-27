import math
import logging
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("H11-ABSTRACTION")

@dataclass
class Exemplar:
    id: str
    features: Dict[str, float]

@dataclass
class Prototype:
    id: str
    members: List[str]
    mean_features: Dict[str, float]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "members": self.members,
            "mean_features": self.mean_features
        }

class AbstractionEngine:
    """
    Implements a simple K-Means based conceptual clustering to extract prototypes
    from numeric feature vectors, acting as a flat abstraction layer.
    """
    def __init__(self, exemplars: List[Exemplar], k: int = 2):
        self.exemplars = exemplars
        self.k = min(k, len(exemplars))
        self.feature_keys = self._get_all_features()

    def _get_all_features(self) -> List[str]:
        keys = set()
        for ex in self.exemplars:
            keys.update(ex.features.keys())
        return list(keys)

    def _distance(self, f1: Dict[str, float], f2: Dict[str, float]) -> float:
        dist = 0.0
        for k in self.feature_keys:
            v1 = f1.get(k, 0.0)
            v2 = f2.get(k, 0.0)
            dist += (v1 - v2) ** 2
        return math.sqrt(dist)

    def _compute_centroid(self, cluster: List[Exemplar]) -> Dict[str, float]:
        if not cluster:
            return {}
        centroid = {}
        n = len(cluster)
        for k in self.feature_keys:
            centroid[k] = sum(ex.features.get(k, 0.0) for ex in cluster) / n
        return centroid

    def extract_prototypes(self, max_iters: int = 100) -> List[Prototype]:
        if not self.exemplars:
            return []
            
        # 1. Initialize centroids (random pick, deterministic for simplicity here: first k)
        centroids = [dict(self.exemplars[i].features) for i in range(self.k)]
        
        clusters: List[List[Exemplar]] = [[] for _ in range(self.k)]
        
        for _ in range(max_iters):
            # Assignment step
            new_clusters = [[] for _ in range(self.k)]
            for ex in self.exemplars:
                dists = [self._distance(ex.features, c) for c in centroids]
                best_idx = dists.index(min(dists))
                new_clusters[best_idx].append(ex)
                
            # Check convergence
            if [len(c) for c in clusters] == [len(c) for c in new_clusters]:
                # Weak convergence check based on cluster sizes
                break
            clusters = new_clusters
            
            # Update step
            centroids = [self._compute_centroid(c) if c else centroids[i] for i, c in enumerate(clusters)]
            
        # Format output
        prototypes = []
        for i, (c_list, centroid) in enumerate(zip(clusters, centroids)):
            if not c_list:
                continue
            prototypes.append(Prototype(
                id=f"Concept_Proto_{i}",
                members=[ex.id for ex in c_list],
                mean_features=centroid
            ))
            
        return prototypes

def run_abstraction_agent(input_data: Dict[str, Any]) -> Dict[str, Any]:
    raw_ex = input_data.get("exemplars", [])
    k = input_data.get("target_clusters", 2)
    
    exemplars = [Exemplar(e["id"], e["features"]) for e in raw_ex]
    
    engine = AbstractionEngine(exemplars, k)
    prototypes = engine.extract_prototypes()
    
    return {
        "prototypes": [p.to_dict() for p in prototypes]
    }

if __name__ == "__main__":
    sample_input = {
        "target_clusters": 2,
        "exemplars": [
            {"id": "dog1", "features": {"size": 0.5, "fur": 1.0, "barks": 1.0}},
            {"id": "dog2", "features": {"size": 0.6, "fur": 0.9, "barks": 1.0}},
            {"id": "cat1", "features": {"size": 0.2, "fur": 0.8, "barks": 0.0}},
            {"id": "cat2", "features": {"size": 0.1, "fur": 1.0, "barks": 0.0}}
        ]
    }
    result = run_abstraction_agent(sample_input)
    print(json.dumps(result, indent=2))
