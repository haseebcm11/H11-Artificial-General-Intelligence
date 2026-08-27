# H11-REFLECTION Specification

## Overview
H11-REFLECTION provides the cognitive capacity for self-assessment, error detection, and iterative refinement. It implements concepts from the Reflexion framework, allowing agents to evaluate their own generated outputs, identify flaws, and generate critiques that guide self-correction.

## Core Capabilities
- **Output Evaluation**: Grading or classifying the quality of a given response or reasoning chain.
- **Error Detection**: Identifying logical fallacies, factual errors, or formatting issues in generated text.
- **Critique Generation**: Producing targeted verbal reinforcement (critiques) detailing why an output failed and how to improve it.
- **Iterative Refinement**: Managing the loop of Generation -> Evaluation -> Critique -> Generation.

## Architecture
- `SelfEvaluator`: Assesses a trajectory or output against expected constraints.
- `CritiqueGenerator`: Formulates natural language feedback based on identified errors.
- `ReflexionMemory`: Stores past failed trajectories and their critiques to prevent repeated mistakes in future iterations.
