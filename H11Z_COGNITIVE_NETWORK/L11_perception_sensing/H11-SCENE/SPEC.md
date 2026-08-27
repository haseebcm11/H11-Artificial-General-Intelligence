<<H11-SCENE — Scene Understanding Agent>>
> **Layer 11** · Perception & Sensing · `H11-SCENE`

## Purpose
The H11-SCENE agent extracts high-level semantic meaning from holistic visual environments. Moving beyond object detection, it interprets relationships, contexts, and spatial arrangements to construct symbolic scene graphs and natural language descriptions. 

This agent provides the cognitive substrate with a grounded understanding of "where things are," "what is happening globally," and "how objects interact," which is fundamental for complex reasoning, question answering, and contextual awareness.

## Technical Deep-Dive
H11-SCENE relies on a Vision-Language foundation model architecture. For structural understanding, it employs a Scene Graph Generation (SGG) pipeline utilizing a transformer-based object relation extractor (e.g., RelTR). This model jointly detects objects and predicates (e.g., *person-riding-bike*, *cup-on-table*), outputting a directed graph of semantic triplets.

For holistic semantic interpretation, it utilizes a large multi-modal model (LMM) aligned via contrastive learning (similar to CLIP) coupled with a generative decoder (like BLIP-2 or LLaVA). This allows the agent to perform Visual Question Answering (VQA), dense captioning, and referring expression comprehension. The image is encoded via a ViT (Vision Transformer) into dense patch embeddings, which are then queried by a Q-Former mechanism to extract context-specific visual tokens that interface directly with the LLM backend.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `image` | `NDArray` | High-resolution scene image (RGB). |
| `task_query` | `SceneQuery` | Dataclass specifying requested task (Graph, VQA, Captioning). |
| `text_prompt` | `Optional[str]` | Text prompt for VQA or referring expressions. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `scene_graph` | `SceneGraph` | Graph structure with Object Nodes and Edge Predicates. |
| `caption` | `Optional[str]` | Natural language description of the scene. |
| `vqa_answer` | `Optional[str]` | Textual answer to the provided visual question. |
| `grounded_boxes`| `List[BBox]` | Bounding boxes corresponding to specific text phrases. |

### State Schema
Stateless by default for single-image queries, but can maintain a `ContextBuffer` for sequential video scene reasoning, aggregating scene graphs across time to filter out transient noise and build a stable environmental map.

## Dependencies
### Upstream
- `H11-CAMERA`: Source visual input.
- `H10-LLM`: (Optional) Can offload complex generative tasks to the central language model layer.

### Downstream
- `H12-NAV`: Uses scene graphs for semantic path planning.
- `H14-EXEC`: Uses referring expression comprehension to interact with specific objects.

## Failure Modes
1. **Hallucination**: Generative models predicting plausible but non-existent objects based on language priors. Recovery: Strict grounding constraints leveraging object detection confidence.
2. **Predicate Ambiguity**: Hard-to-define relationships (e.g., "near", "behind") depending on camera angle. Recovery: Outputting probabilistic relation edges rather than deterministic ones.
3. **Clutter Degradation**: Performance drop in highly cluttered scenes (e.g., messy room) due to O(N^2) relation space. Recovery: Top-K relation pruning based on object saliency.

## Performance Characteristics
- **Scene Graph Generation**: ~100ms per frame.
- **VQA / Captioning**: ~300-800ms depending on sequence length and model scale.

## Research References
1. Cong, Y., et al. (2022). RelTR: Relation Transformer for Scene Graph Generation. IEEE TPAMI.
2. Li, J., et al. (2023). BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models. ICML.
3. Krishna, R., et al. (2017). Visual Genome: Connecting Language and Vision Using Crowdsourced Dense Image Annotations. IJCV.

## Implementation Notes
Graph representations use NetworkX compatible data structures. To handle the O(N^2) relation space efficiently, we employ spatial heuristics to mask out impossible relations (e.g., objects 50 meters apart) before passing through the heavy transformer layers.
