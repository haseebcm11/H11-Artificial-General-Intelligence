> **Layer 16** · Transportation & Mobility · `H11-AUTONOMOUS`

## Purpose
H11-AUTONOMOUS provides the intelligence stack for Level 4/5 autonomous vehicles. It handles sensor fusion (LiDAR, Radar, Camera), occupancy grid mapping, trajectory planning (Frenet frame generation), and Model Predictive Control (MPC) for vehicle actuation.

## Technical Deep-Dive
The agent utilizes a late-fusion architecture for object detection. Planning is conducted in the Frenet space (s, d coordinates relative to a reference path) to decouple longitudinal and lateral dynamics. A non-linear Model Predictive Controller (NMPC) optimizes the steering and acceleration over a receding horizon while maintaining safety bounds (obstacle avoidance, kinematic limits).

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| point_cloud | PointCloud3D | Raw LiDAR data |
| object_list | List[TrackedObject] | Radar/Camera detected objects |
| route | Route | High-level GPS route |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| trajectory | List[Pose] | Local trajectory |
| actuation | ActuationCommand| Steer, Throttle, Brake |

### State Schema
- `occupancy_grid`: Probabilistic grid map
- `ego_state`: Current localized pose and velocity
- `predicted_actors`: Extrapolated trajectories of others

## Dependencies
### Downstream
- H11-AUTOMOBILIS (sends actuation commands)
- H11-EV (requests torque limits)

## Failure Modes
- Sensor occlusion / False positives
- MPC optimization infeasibility

## Research References
- Thrun, S. (2005). Probabilistic Robotics.
- Werling, M. et al. (2010). Optimal Trajectory Generation for Dynamic Street Scenarios in a Frenet Frame.
