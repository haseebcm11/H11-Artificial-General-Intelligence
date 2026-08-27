# H11-CONSTITUTION (Constitutional AI)

## Overview
H11-CONSTITUTION governs the self-correction and critique phase of the agent's internal monologue. It provides an explicit declarative constitution containing principles that the model uses to critique and revise its own outputs prior to finalization.

## Architecture
- **Principle Registry**: A version-controlled, hierarchical registry of constitutional principles.
- **Critique Generator**: Evaluates a draft response against the principles, generating a natural language critique.
- **Revision Engine**: Applies the critique to modify the draft into a compliant final state.

## Interfaces
- `get_active_principles(context: Domain) -> List[Principle]`
- `critique(draft: str, principles: List[Principle]) -> Critique`
- `revise(draft: str, critique: Critique) -> RevisedOutput`
