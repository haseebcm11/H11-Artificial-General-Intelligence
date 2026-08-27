> **Layer 2** · Data Plane & Ingestion · `H11-SYNTHDATA`

## Purpose

The H11-SYNTHDATA agent fundamentally transforms the Cognitive Substrate from a passive consumer of organic data into an active creator of its own training manifold. As high-quality human-generated data becomes scarce (the "data wall"), models must rely on synthetically generated datasets to continue scaling capabilities. This agent orchestrates the programmatic generation of structured, unstructured, and multi-modal data that adheres to strict distribution constraints while maintaining differential privacy.

It acts as a controlled hallucination engine, utilizing techniques like Self-Instruct and Evol-Instruct to iteratively bootstrap instruction-tuning datasets from a small set of seed prompts. Additionally, it serves as a privacy-preserving bridge: when organic data contains highly sensitive PII, this agent trains localized Generative Adversarial Networks (GANs) or Diffusion models to synthesize proxy datasets that match the statistical distribution of the organic data without leaking individual identities.

## Technical Deep-Dive

For Natural Language generation, H11-SYNTHDATA implements an Evol-Instruct pipeline. Given a base instruction, it applies a series of stochastic mutations (e.g., adding constraints, deepening reasoning steps, increasing input complexity) via an ensemble of smaller LLMs. This incrementally builds a curriculum of increasingly difficult training examples. To prevent model collapse (where a model trains purely on its own average outputs and loses tail variance), the agent employs a distribution matching heuristic, rejecting synthetic outputs that fall too close to the centroid of the existing dataset embedding space.

For tabular and structured data, the agent implements a Conditional Tabular GAN (CTGAN) framework. It handles discrete columns via Gumbel-Softmax relaxations and continuous columns via Variational Gaussian Mixture Models (VGM). To ensure privacy, the generator's gradients are clipped and noised using the Differential Privacy Stochastic Gradient Descent (DP-SGD) mechanism. The total privacy budget ($\epsilon$, $\delta$) is strictly accounted for; once the budget is exhausted, the model weights are frozen.

For images, the agent directs Latent Diffusion models, walking the latent space along specific principal components to generate targeted counterfactuals (e.g., generating under-represented classes in a vision dataset to balance the long-tail).

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `seed_data` | `List[DataTuple]` | Organic seed examples to mutate or model. |
| `generation_target` | `int` | Total number of synthetic samples requested. |
| `privacy_budget` | `DPBudget` | Epsilon and Delta constraints for generation. |
| `generator_type` | `GeneratorConfig` | EVOL_INSTRUCT, CTGAN, or LATENT_DIFFUSION. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `synthetic_batch` | `List[DataTuple]` | The generated data payload. |
| `diversity_score` | `float` | Nearest-neighbor distance metric ensuring variety. |
| `epsilon_spent` | `float` | Privacy budget consumed during the run. |

### State Schema
- `evol_mutation_history`: Directed acyclic graph tracking how seed prompts evolved into complex prompts.
- `dp_accountant`: Running tally of the Renyi Differential Privacy budget across all active GANs.
- `rejection_sampler`: Cache of discarded samples used to refine the generator's rejection boundaries.

## Dependencies

### Upstream (depends on)
- `H11-FILTER`: Only highly vetted, clean seed data should be used to prevent generating synthetic toxicity.
- `H11-QUALITY`: Validates the synthetic output distribution against the organic baseline.

### Downstream (feeds into)
- `H11-INGEST`: Synthetic data is looped back into the main pipeline as a first-class citizen.

## Failure Modes
1. **Model Collapse (Ouroboros Effect)**: The generator relies too heavily on high-probability outputs, causing the synthetic dataset to lose all variance and heavily degrade downstream model generalization.
2. **Privacy Leakage**: DP-SGD implementation errors causing the generator to perfectly memorize and emit exact copies of sensitive PII from the seed tabular data.
3. **Evol-Instruct Saturation**: Mutations becoming nonsensical (e.g., adding arbitrary constraints until the prompt is mathematically impossible to solve).
4. **Mode Collapse in CTGAN**: The GAN completely ignoring minority classes in highly imbalanced tabular data.

## Performance Characteristics
- Tabular CTGAN Generation: ~50k rows/sec on GPU.
- Evol-Instruct: Bound by LLM inference limits (~50 tokens/sec/stream).
- DP Accounting: Negligible compute overhead, highly memory-bound during gradient clipping.

## Research References
- Xu, L., et al. (2019). Modeling Tabular data using Conditional GAN.
- Wang, Y., et al. (2022). Self-Instruct: Aligning Language Models with Self-Generated Instructions.
- Abadi, M., et al. (2016). Deep Learning with Differential Privacy.

## Implementation Notes
Implement the DP accountant using the Moments Accountant method or Renyi DP for tighter bounds on $\epsilon$. For Evol-Instruct, utilize a temperature scheduling mechanism: increase temperature linearly as the depth of the mutation tree grows to force the model out of local minima.
