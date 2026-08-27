> **Layer 2** · Machine Learning · `H11-EXPLAINABLE`

## Purpose

H11-EXPLAINABLE (XAI) bridges the gap between complex neural representations and human/symbolic reasoning. As the substrate relies on deep learning and billion-parameter models, the "black box" nature of these systems poses unacceptable risks for critical decision-making. This agent decomposes, visualizes, and mathematically justifies the outputs of other machine learning agents.

It operates post-hoc (analyzing already trained models) and inherently (designing models that are interpretable by construction). When a medical diagnostic model proposes a treatment, or a financial model rejects a transaction, EXPLAINABLE generates the semantic evidence chain proving *why* the decision was made.

## Technical Deep-Dive

The agent utilizes a suite of attribution and perturbation techniques. For global interpretability, it constructs surrogate models (e.g., shallow decision trees) that approximate the deep network's manifold. For local interpretability, it employs SHAP (Shapley Additive exPlanations) and LIME (Local Interpretable Model-agnostic Explanations).

In deep visual models, it generates saliency maps using Grad-CAM, Integrated Gradients, or SmoothGrad to highlight the exact pixels influencing a classification. In NLP models, it analyzes attention heads (Attention Rollout) and performs causal interventions (Knockoff generation, Counterfactual testing) to determine true causal reliance versus spurious correlation.

More advanced capabilities include Mechanistic Interpretability—mapping specific neurons or circuits within a Transformer to human-understandable concepts (e.g., finding the "plurality neuron" or the "induction head").

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| model_artifact | str | URI to the model to explain |
| input_data | Tensor | The specific data point(s) causing the decision |
| prediction_output| Tensor | The output to explain |
| explanation_type | XAIType | LOCAL_SHAP, GRAD_CAM, COUNTERFACTUAL, MECHANISTIC |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| feature_attributions| Dict[str, float] | Importance scores for input features |
| saliency_map | Optional[str] | URI to visual overlay mask |
| counterfactuals | List[Tensor] | Minimum perturbations to flip the decision |
| text_justification| str | Human-readable explanation text |

### State Schema
- `concept_activation_vectors`: Cached TCAVs (Testing with Concept Activation Vectors) for known concepts.
- `explanation_cache`: Memoized SHAP values for frequent inputs.

## Dependencies

### Upstream (depends on)
- H11-DEEPLEARNING: Provides the model weights, architectures, and gradients.
- H11-MACHINA-DISCENS: Provides classical models for surrogate construction.

### Downstream (feeds into)
- H11-FAIRNESS: Uses feature attributions to detect reliance on protected attributes.
- H11-ROBUSTA: Uses counterfactuals to identify brittle decision boundaries.

## Failure Modes
- `ExplanationFaithfulnessFailure`: The generated explanation (e.g., via LIME) does not actually reflect the model's true internal logic (the surrogate model is unfaithful).
- `GradientShattering`: In very deep networks with ReLUs, gradient-based explanations become noisy and meaningless.
- `SpuriousConceptAlignment`: TCAV incorrectly aligns a learned concept with a human concept due to confounding variables in the probing dataset.

## Performance Characteristics
- Latency: High. Exact SHAP calculation is NP-hard; relies on sampling approximations.
- Compute: Gradient-based attributions require multiple backward passes.

## Research References
- Lundberg, S. M., & Lee, Su-In. (2017). *A Unified Approach to Interpreting Model Predictions (SHAP)*.
- Selvaraju, R. R., et al. (2017). *Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization*.

## Implementation Notes
Requires deep access to computational graphs to insert hooks for intermediate activations and gradients.
