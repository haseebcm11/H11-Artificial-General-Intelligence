> **Layer 2** · Machine Learning · `H11-METALEARNING`

## Purpose

H11-METALEARNING is the substrate's "learning to learn" engine. While DEEPLEARNING and MACHINA-DISCENS focus on solving specific tasks, METALEARNING optimizes the algorithms, learning rates, architectures, and optimization strategies used across the entire system. It extracts meta-knowledge from previous training runs to radically accelerate future convergence.

This agent is critical for few-shot learning and system-level self-improvement. By modeling the loss surfaces and training dynamics of hundreds of models, it can predict the optimal hyperparameters and initialization schemes for novel tasks without requiring expensive grid searches or Bayesian optimization trials from scratch.

## Technical Deep-Dive

The agent implements Model-Agnostic Meta-Learning (MAML) to find optimal parameter initializations that can be adapted to new tasks with just one or two gradient steps. It operates an inner-loop (task-specific adaptation) and an outer-loop (meta-objective optimization).

Beyond MAML, it utilizes recurrent meta-learners (e.g., RL2, LSTMs acting as optimizers) that ingest gradients and output parameter updates, effectively replacing standard optimizers like Adam or SGD with a learned neural optimizer tailored to the substrate's specific workload distribution.

It also maintains an active "Task Embedding Space" using prototypical networks. When a new dataset arrives, it computes a task representation and matches it against the embedding space to retrieve the most suitable training curriculum and architecture.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| task_batch | List[TaskSpec] | Set of diverse tasks for the outer loop |
| meta_objective | LossFunction | The metric to optimize (e.g., few-shot accuracy) |
| inner_lr | float | Learning rate for the task-specific update |
| outer_optimizer| str | Optimizer for the meta-parameters |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| meta_parameters | str | URI to the optimized initialization weights |
| learned_optimizer| str | URI to the neural optimizer network |
| task_embeddings | Dict[str, Vector] | Latent representations of the tasks |
| meta_convergence | float | Final meta-loss |

### State Schema
- `task_manifold`: Vector database mapping task properties to optimal hyperparameters.
- `meta_gradients`: Accumulated outer-loop gradients.

## Dependencies

### Upstream (depends on)
- H11-DEEPLEARNING: Provides the base networks and computes inner-loop gradients.
- H11-TRANSFERLEARNING: Provides base models for zero-shot evaluations.

### Downstream (feeds into)
- H11-MACHINA-DISCENS: Replaces its Bayesian HP search with learned initializations.
- H11-GENERATIVA: Provides fast-adaptation initializations for generative prompts.

## Failure Modes
- `MetaOverfitting`: The outer loop overfits to the meta-training tasks and fails to generalize to novel tasks.
- `GradientDegradationAnomaly`: Second-order derivatives (Hessian approximations in MAML) become numerically unstable (NaN).
- `TaskImbalanceCollapse`: The meta-learner ignores difficult tasks in the batch to minimize loss on easy tasks.

## Performance Characteristics
- Compute Intensity: Extremely high. MAML requires computing gradients of gradients (Hessian vector products).
- Inference/Adaptation: Extremely fast (1-5 gradient steps on novel data).

## Research References
- Finn, C., et al. (2017). *Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks*.
- Andrychowicz, M., et al. (2016). *Learning to learn by gradient descent by gradient descent*.

## Implementation Notes
Requires deep integration with auto-differentiation frameworks (e.g., JAX, PyTorch functorch) to efficiently compute higher-order derivatives.
