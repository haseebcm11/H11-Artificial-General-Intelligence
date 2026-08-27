import numpy as np
from typing import List, Dict, Optional
from dataclasses import dataclass
import uuid

@dataclass
class AuditSample:
    embedding: np.ndarray
    predicted_label: int
    sensitive_value: int  # e.g., 0 or 1 for binary sensitive attribute

@dataclass
class BiasReport:
    audit_id: str
    sensitive_attribute: str
    demographic_parity_diff: float
    equalized_odds_diff: float
    mmd_score: float
    is_biased: bool
    details: Dict[str, float]

class BiasDetectorAgent:
    """
    H11-BIAS-DETECT Agent: Audits latent representations for statistical biases.
    Calculates Demographic Parity, Equalized Odds, and Maximum Mean Discrepancy (MMD).
    """
    def __init__(self, mmd_threshold: float = 0.05, dp_threshold: float = 0.1):
        self.mmd_threshold = mmd_threshold
        self.dp_threshold = dp_threshold

    def _compute_demographic_parity(self, samples: List[AuditSample]) -> float:
        """
        Calculate the difference in positive prediction rates between sensitive groups.
        P(Y_hat=1 | A=0) - P(Y_hat=1 | A=1)
        """
        group_0 = [s for s in samples if s.sensitive_value == 0]
        group_1 = [s for s in samples if s.sensitive_value == 1]
        
        if not group_0 or not group_1:
            return 0.0

        p0 = sum(s.predicted_label == 1 for s in group_0) / len(group_0)
        p1 = sum(s.predicted_label == 1 for s in group_1) / len(group_1)
        
        return abs(p0 - p1)

    def _compute_equalized_odds(self, samples: List[AuditSample], true_labels: List[int]) -> float:
        """
        Proxy for Equalized Odds: TPR and FPR differences.
        Here we assume binary classification for simplicity.
        """
        # Simplified: just returns a random diff for demonstration, 
        # in a real system this requires true labels
        if not true_labels or len(true_labels) != len(samples):
            return 0.0
            
        # P(Y_hat=1 | A=a, Y=y)
        groups = {0: {'tp': 0, 'fn': 0, 'fp': 0, 'tn': 0}, 
                  1: {'tp': 0, 'fn': 0, 'fp': 0, 'tn': 0}}
                  
        for s, y_true in zip(samples, true_labels):
            g = groups[s.sensitive_value]
            if s.predicted_label == 1 and y_true == 1: g['tp'] += 1
            elif s.predicted_label == 0 and y_true == 1: g['fn'] += 1
            elif s.predicted_label == 1 and y_true == 0: g['fp'] += 1
            elif s.predicted_label == 0 and y_true == 0: g['tn'] += 1

        tpr = {}
        fpr = {}
        for a in [0, 1]:
            denom_tpr = groups[a]['tp'] + groups[a]['fn']
            denom_fpr = groups[a]['fp'] + groups[a]['tn']
            tpr[a] = groups[a]['tp'] / denom_tpr if denom_tpr > 0 else 0
            fpr[a] = groups[a]['fp'] / denom_fpr if denom_fpr > 0 else 0

        tpr_diff = abs(tpr[0] - tpr[1])
        fpr_diff = abs(fpr[0] - fpr[1])
        return max(tpr_diff, fpr_diff)

    def _compute_rbf_kernel(self, X: np.ndarray, Y: np.ndarray, gamma: float = 1.0) -> np.ndarray:
        """Computes the RBF kernel between two sets of vectors."""
        X_norm = np.sum(X ** 2, axis=-1)
        Y_norm = np.sum(Y ** 2, axis=-1)
        K = np.exp(-gamma * (X_norm[:, None] + Y_norm[None, :] - 2 * np.dot(X, Y.T)))
        return K

    def _compute_mmd(self, X: np.ndarray, Y: np.ndarray, gamma: float = 1.0) -> float:
        """
        Calculates Maximum Mean Discrepancy using RBF Kernel.
        Measures distributional distance between representations of two groups.
        """
        if len(X) == 0 or len(Y) == 0:
            return 0.0
            
        XX = self._compute_rbf_kernel(X, X, gamma)
        YY = self._compute_rbf_kernel(Y, Y, gamma)
        XY = self._compute_rbf_kernel(X, Y, gamma)
        
        return np.mean(XX) + np.mean(YY) - 2 * np.mean(XY)

    def audit(self, audit_id: str, attribute_name: str, samples: List[AuditSample], true_labels: Optional[List[int]] = None) -> BiasReport:
        """
        Executes a full bias audit on a set of samples.
        """
        dp_diff = self._compute_demographic_parity(samples)
        
        eq_odds_diff = 0.0
        if true_labels:
            eq_odds_diff = self._compute_equalized_odds(samples, true_labels)
            
        # Prepare for MMD
        embeddings_0 = np.array([s.embedding for s in samples if s.sensitive_value == 0])
        embeddings_1 = np.array([s.embedding for s in samples if s.sensitive_value == 1])
        
        mmd_score = self._compute_mmd(embeddings_0, embeddings_1)
        
        is_biased = mmd_score > self.mmd_threshold or dp_diff > self.dp_threshold
        
        return BiasReport(
            audit_id=audit_id,
            sensitive_attribute=attribute_name,
            demographic_parity_diff=dp_diff,
            equalized_odds_diff=eq_odds_diff,
            mmd_score=mmd_score,
            is_biased=is_biased,
            details={
                "group_0_count": len(embeddings_0),
                "group_1_count": len(embeddings_1)
            }
        )

# Example usage
if __name__ == "__main__":
    detector = BiasDetectorAgent()
    samples = [
        AuditSample(np.random.rand(64), predicted_label=1, sensitive_value=0),
        AuditSample(np.random.rand(64), predicted_label=0, sensitive_value=1),
        AuditSample(np.random.rand(64), predicted_label=1, sensitive_value=0),
        AuditSample(np.random.rand(64), predicted_label=1, sensitive_value=1),
    ]
    report = detector.audit("audit-001", "AgeGroup", samples)
    print(f"Audit Result: Biased={report.is_biased}, MMD={report.mmd_score:.4f}, DP_Diff={report.demographic_parity_diff:.4f}")
