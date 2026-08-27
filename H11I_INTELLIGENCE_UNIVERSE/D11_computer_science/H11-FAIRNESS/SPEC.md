> **Layer 2** · Machine Learning · `H11-FAIRNESS`

## Purpose

H11-FAIRNESS ensures that the cognitive substrate operates equitably across diverse demographic groups and subpopulations. While ML models naturally optimize for average global accuracy, they often achieve this by exploiting spurious correlations that disadvantage minority groups. This agent audits models, detects disparate impact, and applies mathematical interventions to enforce fairness constraints.

In an AGI context, this agent acts as the ethical governor. Before a model (e.g., resource allocation, hiring screening, facial recognition) is deployed, FAIRNESS ensures its predictions satisfy strict definitions of fairness, such as Demographic Parity, Equalized Odds, or Counterfactual Fairness.

## Technical Deep-Dive

The agent calculates fairness metrics across specified sensitive attributes (e.g., race, gender, age). It operates at three stages of the ML pipeline:
1. **Pre-processing:** Reweighting the training data, applying SMOTE to minority classes, or learning fair representations where sensitive attributes are mathematically independent of the latent space (e.g., using Maximum Mean Discrepancy penalties).
2. **In-processing:** Adding fairness regularization terms to the loss function during training (Adversarial Debiasing).
3. **Post-processing:** Adjusting the decision thresholds dynamically for different groups to equalize True Positive Rates (TPR) and False Positive Rates (FPR).

It utilizes Causal Graphs to evaluate Counterfactual Fairness—ensuring that a decision would remain the same if the sensitive attribute were flipped, holding all other causal ancestors constant.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| model_predictions | Tensor | Outputs of the model |
| sensitive_attributes| Tensor | Protected class labels |
| ground_truth | Tensor | True labels |
| fairness_metric | FairnessDef | EQUALIZED_ODDS, DEMOGRAPHIC_PARITY |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| disparity_scores | Dict[str, float] | Gap between groups for TPR/FPR |
| mitigation_weights| Optional[Tensor] | Data reweighting vector |
| adjusted_thresholds| Optional[Dict] | Post-processing threshold per group |
| certification | bool | Does it pass the required threshold? |

### State Schema
- `audit_history`: Record of disparate impact scores for deployed models.
- `causal_graphs`: Inferred causal relationships between features and sensitive attributes.

## Dependencies

### Upstream (depends on)
- H11-EXPLAINABLE: Uses feature attributions to see if sensitive attributes directly drive the prediction.
- H11-MACHINA-DISCENS: Audits classical ML pipelines.

### Downstream (feeds into)
- H11-SRE: Blocks deployment if the model fails fairness certification.

## Failure Modes
- `ImpossibilityTheoremCollision`: User requests both Calibration and Equalized Odds simultaneously when base rates differ (mathematically impossible).
- `ProxyVariableLeakage`: The model does not use the sensitive attribute explicitly, but reconstructs it perfectly from proxy variables (e.g., zip code).
- `IntersectionalityCombinatorics`: Computing fairness metrics across the cross-product of many sensitive attributes leads to data sparsity and high variance.

## Performance Characteristics
- Latency: Very low for post-processing; high for in-processing adversarial debiasing.
- Data Requirements: Requires explicit access to sensitive attributes during auditing, which may conflict with privacy constraints.

## Research References
- Hardt, M., et al. (2016). *Equality of Opportunity in Supervised Learning*.
- Kusner, M. J., et al. (2017). *Counterfactual Fairness*.

## Implementation Notes
Includes an explicit impossibility-theorem checker to prevent optimizing for mutually exclusive fairness metrics.
