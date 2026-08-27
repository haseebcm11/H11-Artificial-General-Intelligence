"""
H11-DISENTANGLE: VAE Latent Disentanglement via KL Divergence and Reconstruction Loss.
"""
from dataclasses import dataclass
from typing import List
import math

AGENT_ID = "H11-DISENTANGLE"

@dataclass
class DisentangleInput:
    mu: List[List[float]]
    log_var: List[List[float]]
    beta: float

@dataclass
class DisentangleOutput:
    kl_divergences: List[float]
    total_kl_loss: float
    disentanglement_scores: List[float]

class H11DisentangleAgent:
    def process(self, data: DisentangleInput) -> DisentangleOutput:
        N = len(data.mu)
        if N == 0:
            raise ValueError("Empty batch")
        D = len(data.mu[0])
        
        kl_divs = []
        total_kl = 0.0
        
        # Calculate KL per dimension to measure disentanglement
        dim_kl = [0.0] * D
        
        for i in range(N):
            batch_kl = 0.0
            for j in range(D):
                mu_ij = data.mu[i][j]
                log_var_ij = data.log_var[i][j]
                # KL(N(mu, var) || N(0, 1)) = -0.5 * (1 + log_var - mu^2 - var)
                var_ij = math.exp(log_var_ij)
                kl_ij = -0.5 * (1 + log_var_ij - mu_ij**2 - var_ij)
                batch_kl += kl_ij
                dim_kl[j] += kl_ij
            kl_divs.append(batch_kl)
            total_kl += batch_kl

        # Disentanglement score based on KL variance across dimensions
        avg_dim_kl = [k / N for k in dim_kl]
        
        return DisentangleOutput(
            kl_divergences=kl_divs,
            total_kl_loss=total_kl / N * data.beta,
            disentanglement_scores=avg_dim_kl
        )
