"""
H11-HASH: Locality Sensitive Hashing (LSH) using Random Projection for Cosine Similarity.
"""
from dataclasses import dataclass
from typing import List, Dict
import math
import random

AGENT_ID = "H11-HASH"

@dataclass
class HashInput:
    vectors: List[List[float]]
    num_planes: int
    seed: int

@dataclass
class HashOutput:
    hash_tables: Dict[str, List[int]]
    hyperplanes: List[List[float]]

class H11HashAgent:
    def process(self, data: HashInput) -> HashOutput:
        random.seed(data.seed)
        if not data.vectors:
            return HashOutput({}, [])
            
        D = len(data.vectors[0])
        planes = []
        
        for _ in range(data.num_planes):
            # Generate random hyperplane normal vector
            plane = [random.gauss(0, 1) for _ in range(D)]
            planes.append(plane)
            
        hash_tables = {}
        
        for idx, vec in enumerate(data.vectors):
            hash_val = 0
            for p_idx, plane in enumerate(planes):
                dot_prod = sum(vec[i] * plane[i] for i in range(D))
                if dot_prod >= 0:
                    hash_val |= (1 << p_idx)
                    
            hash_str = format(hash_val, f'0{data.num_planes}b')
            if hash_str not in hash_tables:
                hash_tables[hash_str] = []
            hash_tables[hash_str].append(idx)
            
        return HashOutput(
            hash_tables=hash_tables,
            hyperplanes=planes
        )
