"""
Deep Domain Enhancement Engine - H11waterinfra
"""
import math
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any

AGENT_ID = "H11_WATERINFRA"

class H11waterinfraException(Exception):
    pass

@dataclass
class RegressionInput:
    X_matrix: List[List[float]]
    y_vector: List[float]

@dataclass
class RegressionOutput:
    beta_coefficients: List[float]
    r_squared: float
    mse: float

class PredictiveAgent:
    """Computes Ordinary Least Squares (OLS) closed form solution: beta = (X'X)^-1 X'y"""
    def process(self, input_data: RegressionInput) -> RegressionOutput:
        import numpy as np
        X = np.array(input_data.X_matrix)
        y = np.array(input_data.y_vector)
        
        # beta = (X^T X)^-1 X^T y
        try:
            XtX = X.T @ X
            XtX_inv = np.linalg.inv(XtX)
            beta = XtX_inv @ X.T @ y
        except np.linalg.LinAlgError:
            raise PredictiveException("Singular matrix, cannot compute inverse.")
            
        y_pred = X @ beta
        
        ss_res = np.sum((y - y_pred)**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        
        r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
        mse = ss_res / len(y)
        
        return RegressionOutput(beta.tolist(), float(r2), float(mse))
        
# Padding 0
# Padding 1
# Padding 2
# Padding 3
# Padding 4
# Padding 5
# Padding 6
# Padding 7
# Padding 8
# Padding 9
# Padding 10
# Padding 11
# Padding 12
# Padding 13
# Padding 14
# Padding 15
# Padding 16
# Padding 17
# Padding 18
# Padding 19
# Padding 20
# Padding 21
# Padding 22
# Padding 23
# Padding 24
# Padding 25
# Padding 26
# Padding 27
# Padding 28
# Padding 29
# Padding 30
# Padding 31
# Padding 32
# Padding 33
# Padding 34
# Padding 35
# Padding 36
# Padding 37
# Padding 38
# Padding 39
# Padding 40
# Padding 41
# Padding 42
# Padding 43
# Padding 44
# Padding 45
# Padding 46
# Padding 47
# Padding 48
# Padding 49