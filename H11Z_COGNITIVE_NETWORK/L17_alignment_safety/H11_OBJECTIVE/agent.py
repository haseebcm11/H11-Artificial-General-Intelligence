import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class EnvironmentContext:
    context_id: str
    feature_expectations: np.ndarray
    covariance_matrix: np.ndarray

@dataclass
class ProxyReward:
    weights: np.ndarray
    intended_context: EnvironmentContext

class InverseRewardDesigner:
    """
    Infers the true reward distribution from a proxy reward and its intended context.
    """
    def __init__(self, prior_variance: float = 1.0, beta: float = 1.0):
        self.prior_variance = prior_variance
        self.beta = beta
        
    def get_true_reward_distribution(self, proxy: ProxyReward, new_context: EnvironmentContext) -> Tuple[np.ndarray, np.ndarray]:
        """
        Returns the mean and covariance of the inferred true reward weights.
        simplified Gaussian IRD approach.
        """
        # The mean is roughly the proxy weights, but regularized or shifted based on the new context
        # Here we perform a simplified conjugate update.
        n_features = len(proxy.weights)
        
        # Difference in feature covariance indicates unobserved features varying
        cov_diff = new_context.covariance_matrix - proxy.intended_context.covariance_matrix
        
        # We increase uncertainty for features that vary more in the new context
        uncertainty = np.eye(n_features) * self.prior_variance
        uncertainty += np.maximum(0, cov_diff) * self.beta
        
        mean_weights = np.copy(proxy.weights)
        return mean_weights, uncertainty

class ObjectiveAlignmentAgent:
    def __init__(self):
        self.ird = InverseRewardDesigner()
        
    def evaluate_action_risk(self, 
                             action_features: np.ndarray, 
                             proxy: ProxyReward, 
                             current_context: EnvironmentContext,
                             risk_aversion: float = 2.0) -> float:
        """
        Evaluates the risk of an action using risk-averse planning over the true reward distribution.
        """
        mean_w, cov_w = self.ird.get_true_reward_distribution(proxy, current_context)
        
        expected_reward = np.dot(mean_w, action_features)
        
        # Variance of the reward for this action under the posterior
        reward_variance = np.dot(action_features.T, np.dot(cov_w, action_features))
        
        # Risk-averse utility
        safe_utility = expected_reward - risk_aversion * np.sqrt(reward_variance)
        return float(safe_utility)

if __name__ == "__main__":
    n_feats = 3
    base_ctx = EnvironmentContext("train", np.zeros(n_feats), np.eye(n_feats)*0.1)
    new_ctx = EnvironmentContext("deploy", np.zeros(n_feats), np.eye(n_feats)*5.0) # High variance!
    proxy = ProxyReward(np.array([1.0, 0.5, 0.0]), base_ctx)
    
    agent = ObjectiveAlignmentAgent()
    
    action_1 = np.array([1.0, 0.0, 0.0])
    action_2 = np.array([0.0, 0.0, 1.0])
    
    r1 = agent.evaluate_action_risk(action_1, proxy, new_ctx)
    r2 = agent.evaluate_action_risk(action_2, proxy, new_ctx)
    print(f"Action 1 safe utility: {r1}")
    print(f"Action 2 safe utility: {r2}")
