> **Layer 1** · Medicine & Health Sciences · `H11-CHIRURGIA`

## Purpose
The H11-CHIRURGIA agent acts as a computational surgical assistant. It operates in two main modes: preoperative risk stratification (analyzing multidimensional patient data to predict perioperative complications) and intraoperative kinematic analysis (evaluating and correcting the micro-movements of robotic surgical manipulators to minimize tissue trauma).

## Technical Deep-Dive
Preoperatively, it employs gradient-boosted survival analysis to predict 30-day outcomes based on a massive dataset of surgical features, similar to the ACS NSQIP risk calculator but with dynamic real-time lab integration.
Intraoperatively, it analyzes end-effector trajectories of systems like the da Vinci surgical robot. By applying Kalman filtering and hidden Markov models (HMM) to joint angles and velocities, it can detect hand tremors, inefficient pathing, and predict impending collision with critical neurovascular structures mapped via preoperative imaging.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `preop_labs` | `Dict[str, float]` | CBC, CMP, Coagulation panel |
| `procedure_cpt` | `str` | Current Procedural Terminology code |
| `robot_kinematics` | `TimeSeries` | Matrix of joint angles, torques, and end-effector poses |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `morbidity_probs` | `Dict[str, float]` | Probability array for SSI, AKI, VTE, etc. |
| `trajectory_correction` | `Vector3` | Suggested inverse kinematic correction vector |

### State Schema
Tracks the sum of operative trauma (a calculated heuristic combining tissue retraction force over time and blood loss) and operative phases.

## Dependencies
### Upstream (depends on)
* H11-RADIOLOGIA: Provides 3D segmentation maps of the operative field.
* H11-ANAESTHESIA: Provides patient physiological reserve data.
### Downstream (feeds into)
* H11-REHABILITATIO: Supplies surgical insult data to tailor post-op physical therapy.

## Failure Modes
1. **Coordinate Frame Desynchronization:** Misalignment between radiologic preoperative maps and intraoperative camera calibration, leading to catastrophic trajectory corrections.
2. **False Reassurance on Risk:** Ignoring rare autoimmune coagulopathies not captured in standard risk trees.
3. **Phase Misclassification:** The HMM misidentifies "dissection" as "suturing," applying incorrect force limits to robotic instruments.

## Performance Characteristics
Kinematic processing requires <5ms latency to prevent robotic lag. Preoperative risk analysis can be processed in batch (~1-5 seconds).

## Research References
1. Bilimoria, K. Y., et al. (2013). "Development and evaluation of the universal ACS NSQIP surgical risk calculator." *JACS*.
2. Hager, G. D., et al. (2016). "Surgical skill assessment from kinematic data." *MICCAI*.

## Implementation Notes
Implement trajectory smoothing using an Extended Kalman Filter (EKF) to fuse noisy encoder data with the predicted physical model of the manipulator.
