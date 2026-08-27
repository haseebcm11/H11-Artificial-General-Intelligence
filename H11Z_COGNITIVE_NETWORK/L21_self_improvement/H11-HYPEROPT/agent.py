import math
import random
from dataclasses import dataclass
from typing import List, Tuple

AGENT_ID = "H11-HYPEROPT"

@dataclass
class HyperoptInput:
    population_size: int
    mutation_rate: float
    generations: int
    nas_search_space: List[int]

@dataclass
class HyperoptOutput:
    best_architecture: List[int]
    best_fitness: float
    bayesian_expected_improvement: float

class OptimizationException(Exception):
    pass

class HyperoptAgent:
    """
    Implements Bayesian hyperparameter expected improvement, genetic algorithm crossover/mutation,
    and NAS search space evaluation.
    """
    def _fitness(self, genome: List[int]) -> float:
        # Mathematical evaluation representing NAS fitness
        return sum(math.sin(x) + math.cos(x/2.0) for x in genome)
        
    def _crossover(self, p1: List[int], p2: List[int]) -> List[int]:
        c = random.randint(1, len(p1) - 1)
        return p1[:c] + p2[c:]
        
    def _mutate(self, genome: List[int], rate: float, space: List[int]) -> List[int]:
        return [random.choice(space) if random.random() < rate else g for g in genome]

    def _bayesian_ei(self, best_f: float, mu: float, sigma: float) -> float:
        if sigma == 0: return 0.0
        z = (mu - best_f) / sigma
        # Approx CDF
        cdf = 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
        pdf = math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
        return (mu - best_f) * cdf + sigma * pdf

    def process(self, input_data: HyperoptInput) -> HyperoptOutput:
        if not input_data.nas_search_space:
            raise OptimizationException("Empty NAS search space")
            
        population = [[random.choice(input_data.nas_search_space) for _ in range(5)] 
                      for _ in range(input_data.population_size)]
                      
        best_genome = None
        best_f = -float('inf')
        
        for _ in range(input_data.generations):
            fitnesses = [(g, self._fitness(g)) for g in population]
            fitnesses.sort(key=lambda x: x[1], reverse=True)
            
            if fitnesses[0][1] > best_f:
                best_f = fitnesses[0][1]
                best_genome = fitnesses[0][0]
                
            next_gen = [fitnesses[0][0], fitnesses[1][0]]
            while len(next_gen) < input_data.population_size:
                p1 = random.choice(fitnesses[:5])[0]
                p2 = random.choice(fitnesses[:5])[0]
                child = self._crossover(p1, p2)
                child = self._mutate(child, input_data.mutation_rate, input_data.nas_search_space)
                next_gen.append(child)
            population = next_gen
            
        ei = self._bayesian_ei(best_f, best_f + 0.5, 1.2)
        
        return HyperoptOutput(
            best_architecture=best_genome,
            best_fitness=best_f,
            bayesian_expected_improvement=ei
        )
