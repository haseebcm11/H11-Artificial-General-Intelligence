<<H11-OBJECT — Spatial Object Detector>>
> **Layer 11** · Perception & Sensing · `H11-OBJECT`

## Purpose
The H11-OBJECT agent is dedicated to identifying, localizing, and classifying discrete entities within visual space. Consuming feature pyramids from H11-VISION, it predicts bounding boxes and class probabilities with high fidelity. It is crucial for scene parsing, interactive navigation, and tracking dynamic targets across temporal frames.

## Technical Deep-Dive
H11-OBJECT dynamically switches between anchor-based architectures (like Faster R-CNN) for high-accuracy analysis and anchor-free, single-shot mechanisms (like YOLOv8 or DETR) for real-time latency-bound processing. 

For transformer-based detection (DETR paradigms), it utilizes bipartite matching via the Hungarian Algorithm to assign predicted boxes to ground truth, completely eliminating the need for heuristic-driven Non-Maximum Suppression (NMS). However, when operating in convolutional modes, it relies on batched NMS (or Soft-NMS) with dynamically tuned IoU thresholds to discard redundant proposals.

The agent computes confidence scores by merging objectness priors with conditional class probabilities. It also implements an ROI Align module for feature pooling, ensuring pixel-accurate bounding box regression despite feature map quantization errors.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `feature_pyramid` | `Dict[str, Tensor]` | Multi-scale tensors (P3-P5) from H11-VISION. |
| `confidence_thresh`| `float` | Minimum score to consider an object valid. |
| `iou_thresh` | `float` | Threshold for NMS filtering. |
| `mode` | `DetectionMode` | REALTIME (YOLO) vs HIGH_ACCURACY (DETR). |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `boxes` | `List[BoundingBox]` | XYXY coordinates of detected objects. |
| `classes` | `List[int]` | Class IDs mapped to a semantic ontology. |
| `scores` | `List[float]` | Detection confidence (0.0 to 1.0). |

### State Schema
Maintains a transient tracking cache for SORT (Simple Online and Realtime Tracking), linking bounding boxes between contiguous frames via Kalman filters to provide consistent object IDs over time.

## Dependencies
### Upstream
- **H11-VISION**: Multi-scale visual feature maps.
### Downstream
- **L12-SCENE**: Spatial layout parsing.
- **H11-SEGMENT**: Instance mask cropping.

## Failure Modes
1. **Dense Crowd Overlap**: NMS aggressively suppressing valid but heavily occluded objects.
2. **Scale Variance Collapse**: Failure to detect ultra-small objects (e.g., distant signs) if P2 feature maps are stripped.
3. **Ghosting**: Phantom boxes predicted on artifacts or shadows in low-light scenarios.

## Performance Characteristics
- **Latency**: < 20ms in REALTIME mode, ~80ms in HIGH_ACCURACY mode.
- **Metrics**: Evaluated using mAP@0.5:0.95.

## Research References
1. Carion, N., et al. (2020). "End-to-End Object Detection with Transformers."
2. Redmon, J., & Farhadi, A. (2018). "YOLOv3: An Incremental Improvement."
3. Ren, S., et al. (2015). "Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks."

## Implementation Notes
Leverages highly optimized CUDA kernels for NMS and anchor generation to prevent CPU bottlenecks.
