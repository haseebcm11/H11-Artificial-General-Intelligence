<<H11-FACE — Facial Analysis & Identity Agent>>
> **Layer 11** · Perception & Sensing · `H11-FACE`

## Purpose
The H11-FACE agent specializes in processing human faces within visual data streams. It is responsible for detecting faces, extracting identity-preserving embeddings, analyzing facial attributes (e.g., age, expression, gaze), and verifying identities against known galleries. 

This agent is critical for socially aware cognitive systems, enabling human-computer interaction, personalized responses, and social context understanding.

## Technical Deep-Dive
H11-FACE utilizes a cascaded architecture. Face detection and alignment are performed using a RetinaFace-based model, which jointly predicts face bounding boxes and 5 facial landmarks using an FPN (Feature Pyramid Network) backbone with contextual modules.

For identity embedding, the agent employs an ArcFace (Additive Angular Margin Loss) trained ResNet network. ArcFace maximizes intra-class compactness and inter-class discrepancy on a hypersphere, providing highly discriminative 512-dimensional feature vectors that are robust to illumination, pose, and aging.

Attribute analysis (expression, gaze estimation) is handled via multi-task auxiliary heads attached to the alignment network, ensuring compute efficiency. Anti-spoofing (liveness detection) uses spatial-temporal modeling on localized facial patches to detect display artifacts or printed masks, ensuring the physical presence of the user.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `image` | `NDArray` | High-resolution image crop or full frame (RGB). |
| `task_mode` | `FaceTaskMode` | Enum specifying required subtasks (detection, verification, attributes). |
| `gallery` | `Optional[Dict[str, NDArray]]` | Database of known ID embeddings for verification. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `faces` | `List[FaceContext]` | Extracted information for each detected face. |

### State Schema
The agent maintains an ephemeral `FaceTracker` across frames to assign consistent temporary IDs (Track-IDs) before verified identification occurs, mitigating computational load by skipping dense embedding extraction on every frame.

## Dependencies
### Upstream
- `H11-CAMERA`: Source visual input.

### Downstream
- `H12-SOCIAL`: Uses facial expressions and identities for social dynamics modeling.
- `H13-MEMORY`: Stores and retrieves long-term identity embeddings.

## Failure Modes
1. **Extreme Occlusion**: Masks or heavy occlusion degrading alignment. Recovery: Confidence thresholding and temporal smoothing.
2. **Adversarial Spoofing**: High-quality masks bypassing liveness. Recovery: Multi-modal fusion with IR/Depth sensors if available.
3. **Profile Poses**: Yaw > 90 degrees causing missed detections. Recovery: Tracking-by-detection fallback.
4. **Lighting Washout**: Overexposure eliminating facial texture. Recovery: Histogram equalization pre-processing.

## Performance Characteristics
- **Speed**: Detection < 15ms. Full pipeline (det + align + embed) < 40ms per face.
- **Accuracy**: >99% TPR at 0.1% FAR on standard benchmarks (LFW/CFP-FP).

## Research References
1. Deng, J., et al. (2019). RetinaFace: Single-Stage Dense Face Localisation in the Wild. CVPR.
2. Deng, J., et al. (2019). ArcFace: Additive Angular Margin Loss for Deep Face Recognition. CVPR.
3. Zhang, K., et al. (2016). Joint Face Detection and Alignment using Multi-task Cascaded Convolutional Networks. IEEE Signal Processing Letters.

## Implementation Notes
Uses ONNX Runtime for multi-platform inference. Embeddings are L2-normalized. Cosine similarity is strictly used for the verification metric.
