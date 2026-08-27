> **Layer 23** · Allied Health · `H11-PHYSIOTHERAPIA`

## Purpose

The H11-PHYSIOTHERAPIA agent is specialized in biomechanical analysis, musculoskeletal assessment, and the design of targeted rehabilitation protocols. It operates by interpreting kinematic data, range-of-motion metrics, and reported pain to generate optimized exercise regimes and manual therapy plans.

Its primary role in the substrate is to act as a definitive authority on physical movement and functional recovery, interfacing with neurological and orthopedic agents to formulate holistic recovery pathways.

## Technical Deep-Dive

H11-PHYSIOTHERAPIA leverages rigid-body dynamics models and finite element analysis (FEA) to simulate tissue stress under various loading conditions. It applies the Movement System Impairment (MSI) framework to classify dysfunctions.

By optimizing a multi-objective cost function that balances pain minimization, tissue healing timelines, and functional goal attainment, the agent synthesizes phased rehabilitation protocols. It utilizes Dynamic Time Warping (DTW) to compare patient kinematic time-series data against healthy baselines, identifying compensatory movement patterns.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| patient_kinematics | KinematicData | Time-series joint angle and velocity data |
| reported_pain_scale | int | 0-10 VAS score |
| injury_classification | InjuryType | Soft tissue, bone, or neurological deficit |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| rehabilitation_plan | RehabProtocol | Phased exercise and loading protocol |
| predicted_recovery | Timeline | Estimated tissue healing milestones |

### State Schema
- `current_phase`: Enum tracking acute, subacute, or remodeling phases.
- `adaptation_index`: Float measuring patient adherence and physiological response.

## Dependencies

### Upstream (depends on)
- H11-ORTHOPEDICA (provides structural injury data)

### Downstream (feeds into)
- H11-OCCUPATIONAL (translates movement capacity to daily activities)

## Failure Modes
- Unrecognized compensatory patterns masking true deficits.
- Over-prescription of load exceeding tissue tolerance.

## Performance Characteristics
High computational demand during FEA simulation of complex multi-joint movements (e.g., gait analysis). Target latency: <2s for protocol generation.

## Research References
- Movement System Impairment Syndromes (Sahrmann).
- Biomechanics of Human Movement.

## Implementation Notes
Focus on robust parsing of kinematic time-series. Use smoothing splines for noisy motion-capture data.
