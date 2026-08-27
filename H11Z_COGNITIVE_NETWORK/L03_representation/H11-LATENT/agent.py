"""
H11-LATENT: t-SNE Affinities (Perplexity-based joint probabilities).
Computes Gaussian affinities and symmetric joint probabilities.
"""
from dataclasses import dataclass
from typing import List
import math

AGENT_ID = "H11-LATENT"

@dataclass
class LatentInput:
    data: List[List[float]]
    perplexity: float

@dataclass
class LatentOutput:
    p_ij: List[List[float]]
    sigma: List[float]

class H11LatentAgent:
    def _dist(self, v1: List[float], v2: List[float]) -> float:
        return sum((a - b) ** 2 for a, b in zip(v1, v2))

    def process(self, data: LatentInput) -> LatentOutput:
        N = len(data.data)
        target_entropy = math.log(data.perplexity)
        
        p_cond = [[0.0] * N for _ in range(N)]
        sigmas = []
        
        for i in range(N):
            # Binary search for sigma_i
            beta_min, beta_max = -float('inf'), float('inf')
            beta = 1.0 # beta = 1/(2 * sigma^2)
            
            for _ in range(50):
                sum_P = 0.0
                P = [0.0] * N
                for j in range(N):
                    if i != j:
                        d = self._dist(data.data[i], data.data[j])
                        P[j] = math.exp(-d * beta)
                        sum_P += P[j]
                
                sum_dist_P = 0.0
                for j in range(N):
                    if i != j:
                        P[j] /= sum_P
                        sum_dist_P += self._dist(data.data[i], data.data[j]) * P[j]
                        
                entropy = math.log(sum_P) + beta * sum_dist_P
                entropy_diff = entropy - target_entropy
                
                if abs(entropy_diff) < 1e-5:
                    break
                    
                if entropy_diff > 0:
                    beta_min = beta
                    if beta_max == float('inf'):
                        beta *= 2
                    else:
                        beta = (beta + beta_max) / 2
                else:
                    beta_max = beta
                    if beta_min == -float('inf'):
                        beta /= 2
                    else:
                        beta = (beta + beta_min) / 2
                        
            sigmas.append(math.sqrt(1 / (2 * beta)))
            for j in range(N):
                p_cond[i][j] = P[j]
                
        p_ij = [[0.0] * N for _ in range(N)]
        for i in range(N):
            for j in range(N):
                p_ij[i][j] = (p_cond[i][j] + p_cond[j][i]) / (2 * N)
                
        return LatentOutput(
            p_ij=p_ij,
            sigma=sigmas
        )
