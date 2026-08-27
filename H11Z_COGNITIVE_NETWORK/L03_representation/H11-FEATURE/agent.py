"""
H11-FEATURE: Dimensionality reduction via PCA (Eigenvalue computation for covariance matrix).
"""
from dataclasses import dataclass
from typing import List
import math

AGENT_ID = "H11-FEATURE"

@dataclass
class FeatureInput:
    data: List[List[float]]
    n_components: int

@dataclass
class FeatureOutput:
    principal_components: List[List[float]]
    eigenvalues: List[float]
    explained_variance_ratio: List[float]

class H11FeatureAgent:
    def process(self, data: FeatureInput) -> FeatureOutput:
        N = len(data.data)
        D = len(data.data[0])
        
        # Mean centering
        means = [sum(col) / N for col in zip(*data.data)]
        centered = [[row[j] - means[j] for j in range(D)] for row in data.data]
        
        # Covariance matrix
        cov = [[0.0] * D for _ in range(D)]
        for i in range(D):
            for j in range(D):
                cov[i][j] = sum(centered[n][i] * centered[n][j] for n in range(N)) / (N - 1)
                
        # Power iteration for eigenvalues
        components = []
        eigenvals = []
        
        # We need n_components orthogonal eigenvectors
        current_cov = [list(r) for r in cov]
        
        for _ in range(data.n_components):
            v = [1.0] * D
            for _ in range(50):
                v_new = [sum(current_cov[i][j] * v[j] for j in range(D)) for i in range(D)]
                norm = math.sqrt(sum(x*x for x in v_new))
                v = [x/norm for x in v_new]
                
            eigval = sum(v[i] * sum(current_cov[i][j] * v[j] for j in range(D)) for i in range(D))
            eigenvals.append(eigval)
            components.append(v)
            
            # Deflate
            for i in range(D):
                for j in range(D):
                    current_cov[i][j] -= eigval * v[i] * v[j]
                    
        total_var = sum(cov[i][i] for i in range(D))
        ratios = [ev / total_var for ev in eigenvals]
        
        return FeatureOutput(
            principal_components=components,
            eigenvalues=eigenvals,
            explained_variance_ratio=ratios
        )
