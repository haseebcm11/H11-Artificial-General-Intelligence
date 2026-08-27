> **Layer 16** · Transportation & Mobility · `H11-DRONE`

## Purpose
H11-DRONE manages the flight dynamics, swarming logic, and low-altitude airspace integration for multi-rotor and VTOL UAVs. It specifically handles high-frequency ESC (Electronic Speed Controller) commands, attitude estimation (EKF), and collision avoidance in cluttered urban environments.

## Technical Deep-Dive
The agent utilizes a cascaded PID controller architecture (rate, attitude, position, velocity) for precise hover and trajectory tracking. It incorporates sensor fusion using an Error-State Kalman Filter (ESKF) merging IMU, GPS, and optical flow. The swarming algorithm is based on artificial potential fields.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| setpoint | Pose3D | Desired position and yaw |
| imu_data | IMUState | Accel, gyro, mag |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| motor_pwm | List[int] | PWM signals to each ESC |
| state_est | StateEstimate| Fused position/attitude |

### State Schema
- `quad_state`: 12-DOF rigid body state
- `eskf_covariance`: Filter certainty matrix
- `battery_sag`: Voltage drop under load

## Dependencies
### Upstream
- H11-LOGISTICA (for last-mile delivery tasks)

## Failure Modes
- Prop wash / vortex ring state settling
- GPS denial/multipath in urban canyons

## Research References
- Mahony, R., et al. (2012). Nonlinear Complementary Filters on the Special Orthogonal Group.
- Mellinger, D., & Kumar, V. (2011). Minimum snap trajectory generation and control for quadrotors.
