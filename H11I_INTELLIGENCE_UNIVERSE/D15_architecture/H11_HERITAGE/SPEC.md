> **Layer 15** · Architecture & Construction · `H11-HERITAGE`

## Purpose
H11-HERITAGE handles the preservation, restoration, and adaptive reuse of historical structures. It processes point cloud data from LiDAR scans to reconstruct accurate as-built models and diagnoses material degradation (e.g., masonry efflorescence, timber rot).

## Technical Deep-Dive
Uses RANSAC (Random Sample Consensus) algorithms to fit geometric primitives to noisy 3D point cloud data. Employs deep learning (CNNs) on thermographic and photogrammetry datasets to identify micro-cracks and structural spalling in heritage masonry.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| point_cloud | PointCloud | Terrestrial laser scan |
| photos | List[Image] | Photogrammetry data |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| as_built_bim | IFCModel | Reconstructed model |
| defect_map | Mesh | Annotated degradation |

### State Schema
- `scan_registration_error`: Float
- `preservation_status`: String

## Dependencies
- **Downstream**: H11-BIM

## Failure Modes
- Occlusions in point cloud leading to missing structural topology
- False positives in degradation detection

## Implementation Notes
Focuses heavily on point cloud processing and non-destructive testing (NDT) data fusion.
