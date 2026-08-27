# H11-SELFREFINE: Self-Refinement Agent Specification

## Abstract
The H11-SELFREFINE agent is responsible for iterative output improvement. It utilizes contrastive self-refinement and chain-of-thought introspection to independently evaluate its own preliminary outputs and rewrite them to meet stringent quality constraints.

## Core Mechanisms
1. **Multi-turn Introspection**: Operates on a generation-evaluation-refinement loop. It generates a draft, formally evaluates it against multidimensional criteria, and produces a specialized revision plan.
2. **Contrastive Decoding / Prompting**: Employs contrastive methods by explicitly analyzing *why* a previous iteration failed (the negative anchor) and formulating how the next iteration will succeed (the positive anchor).
3. **Delta Application**: Instead of wholesale rewriting for minor issues, the agent can apply structural deltas (e.g., AST transformations for code, semantic diffs for text) to preserve valid sub-components.

## Interfaces
- **Inputs**: `DraftArtifact` containing the initial content, `ConstraintSet` defining the success criteria, and optional `ExternalFeedback`.
- **Outputs**: `RefinedArtifact`, a detailed `RefinementTrace` logging the changes and rationales across iterations, and a boolean `ConvergenceStatus`.

## Failure Modes & Recovery
- **Infinite Oscillations**: The agent might oscillate between two suboptimal states. A loop-detection hash history prevents this; if oscillation is detected, the agent employs a "temperature spike" or reverts to the best-scoring state and terminates.
- **Over-refinement (Degradation)**: Sometimes refinement removes nuance. The agent tracks a monotonic improvement score; if the score degrades for two consecutive steps, early stopping is triggered.
