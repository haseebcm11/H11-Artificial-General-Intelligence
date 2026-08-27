<<H11-SPATIAL — Spatial Perception>>
> **Layer 11** · Perception & Sensing · `H11-SPATIAL`

## Purpose
The H11-SPATIAL agent constructs and maintains a coherent 3D representation of the physical environment. Moving beyond raw pixel arrays or depth maps, this agent interprets spatial semantics: recognizing object volumes, spatial relationships (e.g., "on top of", "inside"), and tracking entities in 3D space over time. 

It grounds the cognitive substrate's understanding of the physical world, enabling downstream agents to perform spatial reasoning, plan navigation, and understand physical interactions. It explicitly handles the translation between egocentric (camera-relative) and allocentric (world-relative) coordinate frames.

## Technical Deep-Dive
H11-SPATIAL leverages point cloud processing, occupancy grids, and 3D scene graph generation. It fuses inputs from multi-view cameras, depth sensors (H11-DEPTH), and odometry.

For static environment modeling, it utilizes Truncated Signed Distance Fields (TSDFs) combined with voxel hashing to incrementally build a dense 3D map of the environment (similar to KinectFusion or VoxelBlox). For dynamic objects, it employs 3D object detection algorithms (such as PointPillars or 3D-RCNN) to extract bounding boxes, orientations (quaternions), and velocities.

The agent explicitly builds a **3D Scene Graph**, where nodes are objects/regions and edges are spatial or semantic relationships. Graph Neural Networks (GNNs) are used to continuously update these relationships based on temporal changes. To handle perspective changes, it employs Spatial Transformer Networks (STNs) and SE(3) pose graph optimization for robust Simultaneous Localization and Mapping (SLAM).

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `point_cloud` | `np.ndarray` | Nx3 array of 3D points. |
| `sensor_pose` | `SE3Transform` | Extrinsic pose of the sensor in world coordinates. |
| `semantic_masks`| `np.ndarray` | 2D/3D segmentation masks from visual streams. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `scene_graph` | `SceneGraph` | Graph of objects and their spatial relationships. |
| `occupancy_grid`| `VoxelGrid` | Probabilistic 3D occupancy map. |
| `spatial_events`| `List[Event]` | Detected changes in spatial arrangements. |

### State Schema
The agent maintains an active `GlobalMap` (a TSDF or Octree), an `EntityTracker` that maintains Kalman filters for moving objects in 3D, and an `AllocentricFrame` definition that anchors the global coordinate system.

## Dependencies
### Upstream
- `H11-DEPTH`: Provides dense depth maps and point clouds.
- `H11-VISION`: Provides 2D bounding boxes, segmentation masks, and visual features.
### Downstream
- `H12-MOTOR-PLANNING`: Relies on the occupancy grid for collision avoidance.
- `H9-REASONING`: Uses the scene graph for physical logic (e.g., "if I push this, it falls").

## Failure Modes
1. **Coordinate Drift**: Accumulation of odometry errors can cause the global map to warp, requiring loop closure corrections.
2. **Dynamic Occlusion**: Moving objects can leave "shadows" in the occupancy grid, which must be systematically ray-traced and cleared.
3. **Reference Frame Confusion**: Improper synchronization between egocentric sensor data and allocentric maps leads to ghosting artifacts.
4. **Symmetric Object Pose Ambiguity**: Objects with rotational symmetry (like a plain mug) can cause unstable quaternion estimates in the scene graph.
5. **Voxel Memory Explosion**: Large environments can exhaust memory if the voxel grid is not properly paged out or managed via octrees.

## Performance Characteristics
- **Latency**: Point cloud integration < 30ms. Scene graph updates < 100ms.
- **Throughput**: Can process 10Hz LiDAR or depth-camera point clouds in real-time.

## Research References
1. Armeni, I., et al. (2019). *3D Scene Graph: A Structure for Unified Semantics, 3D Space, and Camera*. ICCV.
2. Newcombe, R. A., et al. (2011). *KinectFusion: Real-time dense surface mapping and tracking*. ISMAR.
3. Lang, A. H., et al. (2019). *PointPillars: Fast Encoders for Object Detection from Point Clouds*. CVPR.

## Implementation Notes
Implementations must use highly optimized tensor libraries (e.g., PyTorch3D or Open3D) for point cloud operations. Spatial joins and relationship graph edge generation should be bounded by a spatial radius to prevent O(N^2) complexity.
