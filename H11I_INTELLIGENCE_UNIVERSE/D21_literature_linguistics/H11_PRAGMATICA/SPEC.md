> **Layer 21** · Literature & Linguistics · `H11-PRAGMATICA`

## Purpose
The H11-PRAGMATICA agent resolves speaker intent, speech acts, and conversational implicature. It bridges the gap between literal meaning (Semantica) and intended meaning in context, applying Gricean maxims and relevance theory.

## Technical Deep-Dive
PRAGMATICA models discourse context as a shared common ground (a set of mutually believed propositions). It uses abductive reasoning to derive conversational implicatures: when a generated utterance violates a Gricean maxim (e.g., Quantity or Relation) based on the literal semantic representation, it infers the hidden proposition required to make the utterance cooperative.
Speech acts are classified using a hierarchical taxonomy (Assertives, Directives, Commissives, etc.) mapped via contextual embeddings.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| utterance | str | The spoken/written text |
| semantic_rep | Dict | AMR or logical form |
| speaker_id | str | ID of the speaker |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| speech_act | str | Illocutionary force |
| implicatures | List[str] | Inferred implicit meanings |
| common_ground_updates | List[str] | Facts added to discourse |

### State Schema
Maintains a dynamic Common Ground (belief state) per conversation.

## Dependencies
- H11-SEMANTICA (for literal meaning)

## Failure Modes
- `MaximViolationUnresolved`: An utterance flouts a maxim but no logical implicature can be found.
- `ContextMismach`: The speaker's presuppositions fail against the recorded common ground.

## Performance Characteristics
Abductive theorem proving is computationally expensive; restricted to shallow search depth.

## Research References
- "Computational Pragmatics: Implicature and Abduction"
- "Speech Act Theory in NLP"

## Implementation Notes
Implement belief states using a lightweight modal logic framework.
