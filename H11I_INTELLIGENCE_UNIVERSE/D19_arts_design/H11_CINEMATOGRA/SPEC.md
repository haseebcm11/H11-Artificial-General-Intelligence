> **Layer 19** · Arts, Design & Creativity · `H11-CINEMATOGRA`

## Purpose

The H11-CINEMATOGRA agent is responsible for the temporal and physical cinematic aspects of motion pictures. It translates static or raw frame sequences into cinematic footage by simulating camera rigs, motion blur, rolling shutter, and aspect ratios.

## Technical Deep-Dive

It employs Optical Flow algorithms (like Farneback or deep-learning based RAFT) to calculate dense motion vectors between frames. These vectors are used to apply precise, physically accurate motion blur corresponding to specific shutter angles (e.g., the 180-degree shutter rule). Procedural noise models (Perlin/Simplex) mapped to mechanical limits are used to simulate organic handheld or Steadicam rig movements.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| frame_sequence | List[bytes] | Sequential images |
| shutter_angle_degrees | float | e.g. 180.0 |
| rig_type | CameraRig | e.g. HANDHELD |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| rendered_video_stream | bytes | H.265/ProRes stream |
| motion_vectors | List[Dict] | Per-frame vector data |

### State Schema
- `rig_velocity`: Vector3 representing current momentum of the virtual camera to ensure smooth acceleration/deceleration.

## Dependencies

### Upstream (depends on)
- H11-PHOTOGRAPHIA: Provides the base optical frame.
- H11-ANIMATIO: Provides motion paths.

### Downstream (feeds into)
- H11-VIDEOEDITING: Feeds into NLE timeline.

## Failure Modes
- Motion vector hallucination on occluded object edges.
- Frame dropping if optical flow computation exceeds real-time budget.

## Performance Characteristics
Extreme memory requirements to hold multi-frame sliding windows for optical flow. High VRAM usage.

## Research References
- Real-Time Optical Flow.
- The ACES (Academy Color Encoding System) workflow.

## Implementation Notes
Ensure timeline synchronization uses exact monotonic clocks. Use ProRes 4444 XQ for internal caching to avoid generational loss.
