# H11-BOOTSTRAP: Bootstrapping Agent Specification

## Abstract
The H11-BOOTSTRAP agent manages the capability escalation pipeline. It is responsible for taking a base cognitive model and bootstrapping new, specialized capabilities through synthetic data generation, few-shot prompting evolution, and orchestration of parameter-efficient fine-tuning (PEFT) regimens.

## Core Mechanisms
1. **Synthetic Data Generation Engine**: Uses strong base models to generate diverse, high-quality instruction-tuning datasets from a small seed set of examples.
2. **Diversity Maximization**: Implements embedding-based clustering (e.g., K-Means on sentence embeddings) to ensure generated synthetic data covers the maximum possible semantic space, preventing mode collapse.
3. **Distillation Pipeline**: Orchestrates the transfer of capabilities from a heavy teacher process to a lightweight student model via logit distillation and self-play.

## Interfaces
- **Inputs**: `SeedExamples` demonstrating the target capability, `CapabilityDefinition`.
- **Outputs**: `SyntheticDataset` and a `BootstrapManifest` detailing the fine-tuning curriculum and resulting model adapter weights.

## Failure Modes & Recovery
- **Semantic Collapse**: Generated synthetic data becomes highly repetitive. Mitigated by dynamic temperature scaling and frequency penalties applied to the generative teacher model during dataset creation.
- **Reward Hacking in Self-Play**: Student models find shortcuts to maximize rewards without learning the capability. Mitigated by using an independent H11-SELFCRITIQUE agent as the reward model, ensuring strict adherence to constitutional constraints.
