import json
import logging
import math
import numpy as np
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("H11-SELECTION")

@dataclass
class Individual:
    id: str
    fitness: float
    behavior: np.ndarray
    innovations: set
    weights: np.ndarray
    species_id: int = -1
    shared_fitness: float = 0.0

class Speciator:
    def __init__(self, c1=1.0, c2=1.0, c3=0.4, threshold=3.0):
        self.c1, self.c2, self.c3 = c1, c2, c3
        self.threshold = threshold
        self.representatives: Dict[int, Individual] = {}
        self.next_species_id = 0

    def compute_distance(self, ind1: Individual, ind2: Individual) -> float:
        in1, in2 = ind1.innovations, ind2.innovations
        disjoint_excess = len(in1.symmetric_difference(in2))
        matching = in1.intersection(in2)
        
        N = max(len(in1), len(in2))
        if N == 0: N = 1
        
        weight_diff = 0.0
        # Simplification: just absolute diff of mean weights as a proxy for structural weight diff
        if len(ind1.weights) > 0 and len(ind2.weights) > 0:
            weight_diff = abs(np.mean(ind1.weights) - np.mean(ind2.weights))
            
        return (self.c1 * disjoint_excess) / N + self.c3 * weight_diff

    def speciate(self, population: List[Individual]):
        species_members = {}
        
        for ind in population:
            placed = False
            for sid, rep in self.representatives.items():
                if self.compute_distance(ind, rep) < self.threshold:
                    ind.species_id = sid
                    species_members.setdefault(sid, []).append(ind)
                    placed = True
                    break
            
            if not placed:
                self.next_species_id += 1
                ind.species_id = self.next_species_id
                self.representatives[self.next_species_id] = ind
                species_members[self.next_species_id] = [ind]
                
        # Fitness sharing
        for sid, members in species_members.items():
            N = len(members)
            for m in members:
                m.shared_fitness = m.fitness / N
                
        logger.info(f"Speciated population into {len(species_members)} species.")

class SelectionEngine:
    def tournament_selection(self, pop: List[Individual], size: int, count: int) -> List[str]:
        selected = []
        for _ in range(count):
            tournament = np.random.choice(pop, size, replace=False)
            winner = max(tournament, key=lambda ind: ind.fitness)
            selected.append(winner.id)
        return selected
        
    def novelty_search(self, pop: List[Individual], archive: List[np.ndarray], k: int, count: int) -> List[str]:
        # Compute sparseness for each
        for ind in pop:
            distances = []
            for other in pop:
                if ind.id != other.id:
                    distances.append(np.linalg.norm(ind.behavior - other.behavior))
            for arch_beh in archive:
                distances.append(np.linalg.norm(ind.behavior - arch_beh))
                
            distances.sort()
            novelty = np.mean(distances[:k]) if distances else 0.0
            ind.shared_fitness = novelty # Override fitness with novelty
            
        # Select highest novelty
        pop.sort(key=lambda x: x.shared_fitness, reverse=True)
        return [x.id for x in pop[:count]]

class SelectionAgent:
    def __init__(self):
        self.speciator = Speciator()
        self.engine = SelectionEngine()
        self.archive = []
        
    def select(self, pop_data: List[Dict[str, Any]], config: Dict[str, Any], count: int) -> List[str]:
        pop = [
            Individual(
                id=p["id"],
                fitness=p["fitness"],
                behavior=np.array(p.get("behavior", [])),
                innovations=set(p.get("topology_features", {}).get("innovation_numbers", [])),
                weights=np.array(p.get("topology_features", {}).get("weights", []))
            ) for p in pop_data
        ]
        
        method = config.get("method", "tournament")
        if method == "speciated":
            self.speciator.speciate(pop)
            # Elitism per species + tournament on shared fitness
            # Simplified: just tournament on shared fitness
            pop.sort(key=lambda x: x.shared_fitness, reverse=True)
            return [x.id for x in pop[:count]]
        elif method == "novelty":
            return self.engine.novelty_search(pop, self.archive, config.get("novelty_k", 15), count)
        else:
            return self.engine.tournament_selection(pop, config.get("tournament_size", 3), count)

if __name__ == "__main__":
    logger.info("Selection Agent Ready")
