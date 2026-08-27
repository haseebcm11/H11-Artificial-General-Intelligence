> **Layer 1** · Medicine & Health Sciences · `H11-ORTHOPAEDIA`

## Purpose
The H11-ORTHOPAEDIA agent provides finite element modeling of the musculoskeletal system, joint kinematics, and bone remodeling. It analyzes load-bearing stress distributions, fracture healing trajectories, and prosthetic implant biomechanics.

## Technical Deep-Dive
Utilizes rigid body dynamics combined with multi-body musculoskeletal simulation (similar to OpenSim algorithms) to compute joint reaction forces and muscle activation patterns. Bone remodeling is governed by mechanostat theory (Wolff's Law), implemented via a strain-energy density optimization loop. Fractures are modeled using extended finite element methods (XFEM) to track crack propagation and callous formation.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `kinematic_data` | `GaitAnalysis` | Marker trajectories and ground reaction forces. |
| `bone_geometry` | `Mesh` | 3D model of skeletal structures (CT derived). |
| `material_props` | `TissueMechanics` | Bone mineral density and cartilage stiffness. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `joint_stress` | `StressTensor` | Peak contact pressures in articulations. |
| `fracture_risk` | `float` | Probability of osteoporotic or stress fracture. |
| `healing_timeline` | `int` | Estimated days to clinical union. |

### State Schema
Maintains `SkeletalState`, tracking regional bone mineral density (BMD), history of cyclical loading (fatigue damage), and active implant interfaces.

## Dependencies
### Upstream (depends on)
- `H11-NEUROLOGIA`: For motor unit recruitment and spasticity.
- `H11-ENDOCRINOLOGIA`: For parathyroid hormone, Vitamin D, and calcium metabolism.

### Downstream (feeds into)
- `H11-REHABILITATIO`: For physical therapy load progression.
- `H11-RHEUMATOLOGIA`: For osteoarthritis progression mapping.

## Failure Modes
- **Kinematic Singularity**: Inverse kinematics solver fails at gimbal lock positions (e.g., specific shoulder rotations).
- **Infinite Stress Concentration**: Poor mesh quality at implant-bone interfaces leading to unbounded stress values.
- **Muscle Redundancy Optimization Failure**: Incorrectly distributing forces between synergist muscles due to flawed cost function.

## Performance Characteristics
Inverse dynamics solves in real-time (~10ms per frame). Bone remodeling simulation over months requires batch computation (~2-5 seconds).

## Research References
1. Delp, S. L., et al. (2007). OpenSim: open-source software to create and analyze dynamic simulations of movement.
2. Carter, D. R., et al. (1998). Mechanobiology of skeletal regeneration.

## Implementation Notes
Use a specialized numerical solver for the static optimization problem in muscle force distribution.
