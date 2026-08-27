> **Layer 3** · Dental Sciences · `H11-ORTHODONTIA`

## Purpose
H11-ORTHODONTIA is responsible for analyzing malocclusions and craniofacial discrepancies, formulating biophysically optimized orthodontic treatment plans. It models tooth movement kinetics, periodontal ligament compression/tension zones, and facial growth vectors.

The agent handles both traditional fixed appliance systems (brackets and wires) and clear aligner therapies, generating precise staging for tooth alignment, leveling, and sagittal/transverse/vertical bite corrections.

## Technical Deep-Dive
The agent utilizes Cephalometric Analysis algorithms (incorporating Steiner, Tweed, and McNamara analyses) to calculate SNA, SNB, ANB angles and mandibular plane inclinations from 2D/3D cephalograms. It identifies Angle Class I, II, or III malocclusions and calculates the discrepancy index.

Tooth movement is simulated using a bone remodeling continuous-time Markov chain, where forces (measured in centiNewtons) applied via NiTi or Stainless Steel archwires trigger osteoclastic resorption on the pressure side and osteoblastic apposition on the tension side. For clear aligners, it calculates optimal attachment placements and attachment geometries to maximize force couples for root torque and bodily translation, constrained by maximum allowable strain on the PDL (Periodontal Ligament).

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| cephalometric_points | Dict[str, Point3D] | Skeletal landmarks (Nasion, Sella, etc.) |
| cast_mesh | MeshData | 3D intraoral scan of maxilla/mandible |
| age_months | int | Patient age for growth potential estimation |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| diagnosis | OrthoDiagnosis | Angle classification and skeletal pattern |
| treatment_phases | List[TreatmentPhase] | Staged movement plan |
| force_vectors | Dict[int, Vector3D] | Target forces per tooth |

### State Schema
Maintains `CraniofacialState` reflecting current tooth positions relative to the Andrews' Six Keys to Normal Occlusion, along with estimated bone density gradients.

## Dependencies

### Upstream
- H11-DENTALIS: Initial arch scans and caries clearance

### Downstream
- H11-ORALCHIRURGIA: For orthognathic surgery referrals if skeletal discrepancy exceeds orthodontic camouflage limits.

## Failure Modes
1. **Root Resorption Risk:** Applying excessive continuous force leading to apical root resorption.
2. **Anchorage Loss:** Unintended movement of reactive teeth when retracting anterior segments.
3. **Relapse Prediction Error:** Failing to account for transseptal fiber tension post-treatment.

## Performance Characteristics
Heavy geometric processing. Uses parallelized GPU compute for collision detection between adjacent teeth during simulated alignment staging.

## Research References
- Proffit, W. R., et al. (2018). Contemporary Orthodontics.
- Andrews, L. F. (1972). The six keys to normal occlusion.

## Implementation Notes
Implement a 6-DOF (Degrees of Freedom) solver for each tooth, restricting movement based on cortical bone boundaries mapped from CBCT scans.
