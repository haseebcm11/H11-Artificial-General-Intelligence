> **Layer 1** · Medicine & Health Sciences · `H11-REHABILITATIO`

## Purpose
The H11-REHABILITATIO agent translates raw biomechanical and neuromuscular signals into actionable recovery plans. It evaluates motor deficits (post-stroke, post-surgery, or musculoskeletal injury) and quantifies recovery trajectories by analyzing gait symmetry, joint moments, and muscular activation patterns.

## Technical Deep-Dive
The agent utilizes Inverse Kinematics and Inverse Dynamics to calculate internal joint moments and powers from external motion capture data and ground reaction forces. 
For muscular analysis, it processes raw surface Electromyography (sEMG) data. It employs time-frequency analysis (e.g., Short-Time Fourier Transform) to track the median frequency (MDF) of the EMG signal. A downward shift in MDF is a highly reliable biomarker for localized muscle fatigue, allowing the agent to dynamically terminate therapy sets before compensatory, detrimental movement patterns emerge.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `mocap_markers` | `TimeSeries` | X, Y, Z coords of anatomical landmarks |
| `force_plates` | `TimeSeries` | Ground reaction forces (GRF) |
| `semg_signals` | `Dict[str, TimeSeries]` | Raw electrical activity per muscle group |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `kinematics` | `Dict[str, float]` | Flexion/extension angles, joint torques |
| `fatigue_state` | `Dict[str, float]` | Spectral shift indicators per muscle |

### State Schema
Tracks the patient's Range of Motion (ROM) progress across sessions and stores baseline symmetrical benchmarks.

## Dependencies
### Upstream (depends on)
* H11-CHIRURGIA: For structural constraints (e.g., hip replacement dislocation precautions).
* H11-NEUROLOGIA: For baseline spasticity/tone profiles.
### Downstream (feeds into)
* H11-SPORTMEDICINA: Transitions patients from rehab to high-performance return-to-play.

## Failure Modes
1. **Marker Occlusion/Swapping:** Motion capture cameras lose sight of a marker, causing the IK solver to flip a knee joint backwards mathematically.
2. **Crosstalk Interference:** sEMG sensors picking up ECG signals or adjacent muscle firing, creating false fatigue readings.
3. **Improper Anthropometric Scaling:** Using default segment masses instead of patient-specific ones, skewing all torque calculations.

## Performance Characteristics
Real-time feedback requires processing 120Hz mocap and 1000Hz EMG data with less than 50ms latency to provide immediate auditory or visual biofeedback to the patient.

## Research References
1. Winter, D. A. (2009). "Biomechanics and Motor Control of Human Movement." *John Wiley & Sons*.
2. De Luca, C. J. (1984). "Myoelectrical manifestations of localized muscular fatigue in humans." *CRC Critical Reviews in Biomedical Engineering*.

## Implementation Notes
EMG signals must first be band-pass filtered (20-450 Hz) and then full-wave rectified before extracting linear envelopes via low-pass filtering (typically ~6 Hz Butterworth filter).
