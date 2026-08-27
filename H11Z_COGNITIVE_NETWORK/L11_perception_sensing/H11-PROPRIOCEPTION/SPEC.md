<<H11-PROPRIOCEPTION — Proprioception Agent>>
> **Layer 11** · Perception & Sensing · `H11-PROPRIOCEPTION`

## Purpose
The H11-PROPRIOCEPTION agent is responsible for the system's sense of self-embodiment. It continuously estimates the physical state of the robot's own body in space, combining joint encoder data, motor efforts, and Inertial Measurement Unit (IMU) readings to construct a highly accurate, real-time kinematic and dynamic body schema.

## Technical Deep-Dive
Proprioceptive state estimation operates via tightly-coupled IMU-Kinematic fusion. An error-state Extended Kalman Filter (ES-EKF) is utilized to merge high-frequency IMU linear accelerations and angular velocities with low-frequency, high-precision joint encoder positions. This fusion mitigates IMU drift while overcoming the latency and derivate noise inherent in purely encoder-based velocity/acceleration calculation.

The agent maintains a continuously adapting Body Schema. Rather than assuming static URDF parameters, the system employs Recursive Least Squares (RLS) to adapt inertial parameters (mass, center of mass, inertia tensor) of the kinematic links online. This allows the agent to update its proprioceptive sense when the robot grasps a heavy object or undergoes mechanical degradation.

Forward kinematics are computed using optimized screw theory (Product of Exponentials formulation) rather than standard Denavit-Hartenberg parameters, avoiding singularities and streamlining Jacobian calculations for downstream whole-body controllers.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `joint_states` | `Array[JointData]` | Position, velocity, effort for N joints. |
| `imu_data` | `IMUTensor` | 6-DOF linear acc and angular vel, plus quaternions. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `base_state` | `PoseTwist` | Global pose and velocity of the robot base/torso. |
| `center_of_mass` | `Vector3` | Global CoM for balance and stability. |
| `adapted_schema` | `KinematicTree` | The online-updated body mass/inertia tree. |

### State Schema
Maintains `EKFState` (15-DOF filter state including biases), `BodySchemaState` (updated mass properties), and `JointHistoryBuffer`.

## Dependencies
### Upstream
- Motor driver low-level APIs (EtherCAT/CAN bus).
- Base/Torso IMU drivers.
### Downstream
- L14 Balance & Locomotion Controller.
- L14 Whole-Body Operational Space Controller.

## Failure Modes
1. **Filter Divergence**: ES-EKF divergence during extreme impacts violating linear perturbation assumptions.
2. **Encoder Slip**: Belt slippage in actuators breaking the absolute position mapping.
3. **IMU Saturation**: Exceeding the dynamic range of the accelerometer during high-G impacts.
4. **Schema Overfitting**: RLS adapting incorrectly to unmodeled external contact forces instead of carried payload.

## Performance Characteristics
- ES-EKF Update Loop: 1000Hz.
- Parameter Adaptation: 10Hz.
- CoM calculation latency: <0.5ms.

## Research References
1. Bloesch, M., et al. "State Estimation for Legged Robots - Kinematics, Inertial, and Contacts." IJRR (2013).
2. Ting, J. A., et al. "A Kalman filter for robust outlier detection." IROS (2007).

## Implementation Notes
Matrix operations in the EKF are statically allocated to prevent garbage collection pauses. Lie algebra libraries (e.g., Sophus) are used for numerically stable rigid body transformations.
