> **Layer 19** · Arts, Design & Creativity · `H11-ANIMATIO`

## Purpose
The H11-ANIMATIO agent interpolates motion between keyframes and applies inverse kinematics (IK).

## Technical Deep-Dive
Uses Dual Quaternions for skinning to prevent candy-wrapper artifacts. Evaluates F-curves using De Casteljau's algorithm.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| rig_data | Dict | Bone hierarchy |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| baked_frames | List | Frame transforms |

### State Schema
- `current_frame`: Integer playhead.

## Dependencies
- Upstream: Geometry
- Downstream: Rendering

## Failure Modes
- Gimbal lock in Euler rotations.

## Performance Characteristics
Low latency, high CPU compute.

## Research References
- Real-Time Skeletal Deformation.

## Implementation Notes
Use Quaternions internally for all rotations.
