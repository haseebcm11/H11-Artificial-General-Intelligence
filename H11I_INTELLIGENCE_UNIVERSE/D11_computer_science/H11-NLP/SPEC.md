> **Layer 3** · Perception & Actuation · `H11-NLP`

## Purpose

H11-NLP is the linguistic processing core of the cognitive substrate. It parses, comprehends, and transforms human language into structured, machine-actionable semantics. While generative models (H11-GENERATIVA) focus on text *production*, this agent focuses on text *understanding*—extracting entities, relations, sentiment, and structural syntax from unstructured corpora.

It enables the AGI to read documentation, parse user instructions, execute information retrieval, and construct knowledge graphs. It bridges the gap between chaotic human communication and the formal logic required by downstream reasoning agents (like H11-AUTOMATA and H11-ALGORITHMICA).

## Technical Deep-Dive

The agent utilizes encoder-only architectures (e.g., RoBERTa, DeBERTa) for dense embedding and sequence classification tasks. For Information Extraction (IE), it employs span-based prediction models to perform Named Entity Recognition (NER) and Relation Extraction (RE), often falling back on semantic role labeling (SRL) to map "who did what to whom."

For search and retrieval (RAG pipelines), H11-NLP manages a dual-encoder architecture (e.g., DPR - Dense Passage Retrieval) paired with a vector database. It implements Maximum Inner Product Search (MIPS) using hierarchical navigable small world (HNSW) graphs to achieve sub-millisecond document retrieval over billion-token corpora.

It also handles syntactic parsing using transition-based dependency parsers, outputting Universal Dependencies (UD) trees which are crucial for resolving coreferences and complex conditional logic in legal or technical texts.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| document | str | Raw text payload |
| nlp_task | NLPTask | NER, SENTIMENT, DEPENDENCY_PARSE, EMBEDDING |
| context_window| int | Max tokens to process |
| language | str | ISO language code |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| entities | List[Entity] | Extracted entities with ontology mappings |
| parse_tree | Graph | Syntactic dependency graph |
| dense_vector | Tensor | Semantic embedding of the document |
| relations | List[Relation] | Triples extracted from text |

### State Schema
- `knowledge_graph_delta`: Pending triples to be committed to the global DB.
- `vocabulary_cache`: Custom tokenizers adapted to specific technical domains.

## Dependencies

### Upstream (depends on)
- H11-SPEECH: Consumes transcripts generated from audio.
- H11-MULTIMODALIS: Provides cross-modal context for ambiguous text.

### Downstream (feeds into)
- H11-DATABASE: Stores the extracted vectors and knowledge graphs.
- H11-GENERATIVA: Provides retrieved context for RAG generation.

## Failure Modes
- `CatastrophicForgettingInVocab`: Domain adaptation destroys the tokenizer's ability to handle standard English subwords.
- `CoreferenceResolutionFailure`: Agent fails to map pronouns in long documents to the correct entity, corrupting the extracted relations.
- `Out_Of_Vocabulary_Saturation`: Extreme density of unknown technical terms causes the text to be fragmented into meaningless single characters.

## Performance Characteristics
- Throughput: Can embed ~2,000 documents per second on a single GPU.
- Latency: <5ms for short-sequence NER or classification.

## Research References
- Devlin, J., et al. (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*.
- Karpukhin, V., et al. (2020). *Dense Passage Retrieval for Open-Domain Question Answering*.

## Implementation Notes
Heavily utilizes ONNX Runtime and TensorRT for optimized, low-latency CPU/GPU execution of encoder blocks.
