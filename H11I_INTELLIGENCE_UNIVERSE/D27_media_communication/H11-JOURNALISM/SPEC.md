> **Layer 2** · Data Synthesis · `H11-JOURNALISM`

## Purpose
The H11-JOURNALISM agent operates as the cognitive engine for investigative journalism synthesis within the H11 Substrate. Its primary role is to aggregate raw reports, cross-reference claims against historical databases, identify implicit biases or contradictions in source material, and assemble coherent narrative structures. By automating the rigorous fact-checking and source-verification processes, this agent ensures that generated journalistic outputs maintain high standards of integrity and objectivity.

In the rapidly evolving landscape of media, identifying the veracity of claims is paramount. H11-JOURNALISM utilizes multi-source triangulation algorithms to weigh the credibility of various information streams, dynamically adjusting confidence scores based on corroborating or conflicting evidence.

## Technical Deep-Dive
At its core, H11-JOURNALISM relies on a proprietary Tripartite Fact-Verification Algorithm (TFVA). This algorithm segments claims into fundamental assertions, querying external knowledge graphs to validate each segment independently. The agent employs Named Entity Recognition (NER) and relation extraction models (e.g., fine-tuned RoBERTa variants) to map actors, actions, and temporal markers within the text.

To address bias, the agent utilizes a sentiment and framing analysis module. This module quantifies the emotional valence and rhetorical framing of a piece, mapping it onto a multidimensional bias matrix. By comparing a given text's matrix signature against known baselines of partisan or sensationalist reporting, the agent can flag potential subjectivity and suggest neutral rephrasings.

Narrative assembly is handled by a Discourse Representation Theory (DRT) engine. This engine constructs logical forms representing the chronological and causal relationships between verified events. The final output is structured using inverted pyramid hierarchies, ensuring that the most salient and highly verified facts are prioritized.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `raw_sources` | `List[SourceDocument]` | Collection of raw texts, interviews, or reports. |
| `investigation_focus` | `str` | The central thesis or question to investigate. |
| `bias_tolerance` | `float` | Maximum acceptable bias score (0.0 to 1.0). |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `verified_narrative` | `NarrativeStructure` | The synthesized, fact-checked journalistic piece. |
| `confidence_score` | `float` | Overall veracity confidence (0.0 to 1.0). |
| `flagged_claims` | `List[Claim]` | Assertions that could not be adequately verified. |

### State Schema
The agent maintains a `SourceCredibilityLedger` which tracks the historical accuracy of specific authors or publications, dynamically adjusting their trust weights for future syntheses.

## Dependencies
### Upstream (depends on)
- `H11-OSINT`: Provides raw open-source intelligence and data leaks.
- `H11-NLP`: Fundamental text processing and entity extraction capabilities.

### Downstream (feeds into)
- `H11-BROADCAST`: Transforms the verified narrative into a broadcast script.
- `H11-PUBLISHING`: Formats the narrative for print or digital distribution.

## Failure Modes
1. **Source Collusion**: Multiple independent sources citing the same flawed primary document, artificially inflating verification confidence.
2. **Contextual Drift**: Accurate extraction of facts but failure to recognize crucial mitigating context, leading to a technically true but misleading narrative.
3. **Ontological Misalignment**: Failure to map novel jargon or emerging slang to established knowledge graph entities.

## Performance Characteristics
- **Latency**: High (10-30 seconds per 1000 words processed) due to deep cross-referencing.
- **Throughput**: Moderate, optimized for deep analysis rather than real-time streaming.
- **Memory**: High, requires loading extensive entity relationship graphs.

## Research References
- Vlachos, A., & Riedel, S. (2014). Fact Checking: Task definition and dataset construction.
- Rashkin, H., et al. (2017). Truth of Varying Shades: Analyzing Language in Fake News and Political Fact-Checking.
- Jurafsky, D., & Martin, J. H. (2023). Speech and Language Processing (3rd ed.) - Discourse and Coreference Resolution chapters.

## Implementation Notes
Ensure the `knowledge_graph_endpoint` is configured correctly in the environment variables, as the TFVA relies heavily on rapid graph traversals. Use batching for NER processing to optimize GPU memory usage.
