# H11-SELFCRITIQUE: Self-Critique Agent Specification

## Abstract
The H11-SELFCRITIQUE agent provides rigorous, multi-dimensional evaluation of system artifacts (code, reasoning traces, decisions). Unlike H11-SELFREFINE which focuses on modifying the output, SELFCRITIQUE acts as a read-only constitutional auditor, identifying logical fallacies, alignment breaches, and factual inaccuracies using dynamic rubrics.

## Core Mechanisms
1. **Constitutional Parsing**: Dynamically loads and interprets constitutional principles or specific rubrics, converting them into a computable checklist.
2. **Adversarial Probing**: Actively attempts to find edge cases or adversarial interpretations of the artifact to test its robustness.
3. **Multi-Dimensional Scoring**: Evaluates the artifact across orthogonal dimensions (e.g., Factuality, Coherence, Safety, Efficiency) yielding a continuous tensor of scores rather than a binary pass/fail.

## Interfaces
- **Inputs**: `ArtifactToCritique`, `EvaluationRubric`, `ContextualGrounding` (optional knowledge base for fact-checking).
- **Outputs**: `CritiqueReport` detailing a `ScoreTensor`, specific `ViolationSpans` (pointing to exact lines or tokens), and `CorrectiveSuggestions`.

## Failure Modes & Recovery
- **Overly Pedantic Critiques**: The agent may fixate on trivial stylistic issues. Mitigated by applying a severity weighting matrix; low-severity issues below a threshold are filtered from the final report.
- **Hallucinated Violations**: The critique agent might invent rules. Recovery involves a secondary verification step where the agent must explicitly quote the rubric rule and the violating artifact span.
