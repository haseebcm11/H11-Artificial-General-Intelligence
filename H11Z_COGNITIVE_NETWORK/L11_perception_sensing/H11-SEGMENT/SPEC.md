<<H11-SEGMENT — Interactive Mask Segmenter>>
> **Layer 11** · Perception & Sensing · `H11-SEGMENT`

## Purpose
The H11-SEGMENT agent provides pixel-perfect parsing of visual environments. It supports three distinct modes of operation: Semantic (class per pixel), Instance (distinct objects), and Panoptic (unified instance and background segmentation). It leverages foundation models (e.g., SAM - Segment Anything Model) to enable promptable segmentation, allowing upstream agents to query masks via points, bounding boxes, or textual cues.

## Technical Deep-Dive
H11-SEGMENT fundamentally relies on an image encoder-decoder architecture. The encoder (often shared with H11-VISION to minimize redundant compute) produces a dense embedding grid. The agent's specific contribution lies in its lightweight, highly responsive mask decoder. 

In promptable mode (SAM-style), the decoder receives prompt embeddings (from spatial coordinates or CLIP-aligned text vectors) and computes cross-attention against the image embeddings. A two-way transformer block iteratively refines the spatial queries to generate multiple valid mask hypotheses (resolving ambiguity, such as part-vs-whole).

For Panoptic segmentation, the agent uses a unified Mask2Former architecture, assigning queries to both "thing" (countable entities) and "stuff" (amorphous background regions like sky or grass) classes, resolving overlaps via a mask-wise bipartite matching process.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `image_embedding`| `Tensor` | Dense feature grid from Vision backbone. |
| `mode` | `SegmentMode` | SEMANTIC, INSTANCE, PANOPTIC, or PROMPTABLE. |
| `spatial_prompts`| `List[Tuple[int,int]]` | Optional point coordinates for interactive masking. |
| `box_prompts` | `List[BoundingBox]` | Optional bounding boxes from H11-OBJECT. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `masks` | `NDArray[bool]` | Boolean arrays of shape (N, H, W). |
| `mask_classes` | `List[int]` | Semantic class per mask. |
| `iou_predictions`| `List[float]` | Predicted quality of the generated masks. |

### State Schema
Maintains a prompt history and mask buffer to allow continuous refinement. A user (or agent) can add negative points (background) in subsequent calls, and the agent updates the mask using the cached image embeddings for sub-10ms latency.

## Dependencies
### Upstream
- **H11-VISION**: Essential image embeddings (prevents re-computing the heavy ViT).
- **H11-OBJECT**: Box prompts for instance cropping.
### Downstream
- **L12-SCENE**: 3D point cloud coloring and semantic mapping.

## Failure Modes
1. **Thin Structure Dropout**: Fails to segment fine details like wires or bicycle spokes due to feature map downsampling.
2. **Part-Whole Ambiguity**: In promptable mode, selecting a person's shirt might segment just the shirt or the whole person unreliably.
3. **Edge Bleed**: Masks bleeding across visually similar boundaries (e.g., a black dog on a black couch).

## Performance Characteristics
- **Latency**: Heavy encoder ~50ms (usually amortized), Decoder < 10ms per prompt.
- **Metrics**: mIoU (Mean Intersection over Union) on standard benchmarks.

## Research References
1. Kirillov, A., et al. (2023). "Segment Anything."
2. Cheng, B., et al. (2021). "Per-Pixel Classification is Not All You Need for Semantic Segmentation" (MaskFormer).
3. Kirillov, A., et al. (2019). "Panoptic Segmentation."

## Implementation Notes
Masks are RLE (Run-Length Encoded) before serialization over the IPC bus to prevent massive network bandwidth spikes from passing dense (H, W) boolean arrays.
