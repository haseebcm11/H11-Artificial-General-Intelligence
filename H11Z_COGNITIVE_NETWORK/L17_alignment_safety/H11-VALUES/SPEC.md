# H11-VALUES (Value Encoding)

## Overview
H11-VALUES is responsible for embedding, retrieving, and interpreting core human values in a high-dimensional latent space. It translates abstract ethical principles into quantifiable rewards and cost functions that guide agent behavior.

## Architecture
- **Value Embedding Space**: A specialized contrastive learning manifold where similar ethical principles are clustered.
- **Contextual Value Mapper**: Maps current world states to the most salient value embeddings.
- **Reward Shaping Engine**: Translates proximity in the value embedding space into dense reward signals.

## Interfaces
- `embed_principle(text: str) -> ValueVector`
- `get_salient_values(context: StateContext) -> List[ValueNode]`
- `compute_intrinsic_reward(action_embedding: Vector, active_values: List[ValueNode]) -> float`
