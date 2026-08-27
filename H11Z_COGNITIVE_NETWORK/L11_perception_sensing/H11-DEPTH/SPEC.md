<<H11-DEPTH — Depth Perception>>
> **Layer 11** · Perception & Sensing · `H11-DEPTH`

## Purpose
The H11-DEPTH agent translates 2D visual inputs into 2.5D/3D depth representations. It provides the crucial missing dimension (Z-axis) to flat RGB images, enabling the system to understand occlusion, scale, and distance. It acts as a specialized preprocessing and feature-extraction module whose outputs directly feed into H11-SPATIAL and H11-VISION.

Whether dealing with single-camera (monocular) streams, stereo pairs, or active depth sensors (LiDAR, Structured Light), this agent normalizes the data into a unified, high-confidence depth map and dense point cloud.

## Technical Deep-Dive
H11-DEPTH implements a hybrid approach to depth estimation. For monocular RGB inputs, it relies on zero-shot scale-invariant depth models (like MiDaS or Depth Anything) based on Vision Transformers (ViTs). These models extract relative depth extremely well but lack absolute scale.

To recover absolute scale, the agent fuses monocular predictions with sparse metric data. This metric data can come from Odometry/SLAM scale estimates, stereo disparity maps (using Semi-Global Matching or RAFT-Stereo), or sparse LiDAR returns. 

The agent runs a **Depth Completion Pipeline**, which takes a dense relative depth map and sparse metric points, formulating an energy minimization problem (or using a lightweight CNN like CSPN - Convolutional Spatial Propagation Network) to output a dense, metric depth map. It also computes a `DepthConfidenceMap`, flagging regions where estimation is uncertain (e.g., reflective surfaces, transparent objects, or textureless walls).

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `rgb_image` | `np.ndarray` | Primary visual input (HxWx3). |
| `intrinsics`| `CameraIntrinsics`| Focal length and principal point. |
| `stereo_pair`| `Optional[np.ndarray]` | Right camera image, if available. |
| `sparse_depth`| `Optional[np.ndarray]`| From LiDAR or active sensors. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `depth_map` | `np.ndarray` | Metric depth map (HxW, float32). |
| `confidence`| `np.ndarray` | Confidence per pixel (HxW, [0,1]). |
| `point_cloud`| `np.ndarray` | Unprojected Nx3 points in camera frame. |

### State Schema
Stateless on a per-frame basis, though it maintains an `IntrinsicsCache` and `TemporalConsistencyBuffer` (using recurrent hidden states like ConvLSTM) to prevent depth flickering across video frames.

## Dependencies
### Upstream
- `H11-VISION`: Provides synchronized RGB frames.
### Downstream
- `H11-SPATIAL`: Consumes the point cloud to build the 3D scene.
- `H12-MOTOR-PLANNING`: Uses depth directly for immediate reactive collision avoidance (e.g., stopping before hitting a wall).

## Failure Modes
1. **Scale Ambiguity**: In pure monocular mode, the absolute scale is a guess; a toy car looks like a real car without context.
2. **Reflective/Transparent Surfaces**: Mirrors, windows, and water confuse both active sensors (LiDAR) and passive visual models.
3. **Temporal Flickering**: Without temporal smoothing, pixel depth can oscillate rapidly, causing downstream spatial maps to blur.
4. **Stereo Occlusion**: Regions visible to the left camera but occluded in the right camera result in undefined disparities.
5. **Textureless Regions**: Blank walls foil traditional stereo matching (though deep models handle this better).

## Performance Characteristics
- **Latency**: ~15-25ms per frame on a modern GPU (TensorRT optimized).
- **Resolution**: Typically operates at 384x512 or 512x512 internally, upsampling to native resolution.

## Research References
1. Ranftl, R., et al. (2020). *Towards Robust Monocular Depth Estimation: Mixing Datasets for Zero-shot Cross-dataset Transfer* (MiDaS). PAMI.
2. Yang, L., et al. (2024). *Depth Anything: Unleashing the Power of Large-Scale Unlabeled Data*. CVPR.
3. Cheng, X., et al. (2018). *Depth Estimation via Affinity Learned with Convolutional Spatial Propagation Network*. ECCV.

## Implementation Notes
The depth maps must be aligned strictly to the optical center defined in the `CameraIntrinsics`. Sub-pixel interpolation is required when upsampling the model outputs to match the high-resolution RGB frames.
