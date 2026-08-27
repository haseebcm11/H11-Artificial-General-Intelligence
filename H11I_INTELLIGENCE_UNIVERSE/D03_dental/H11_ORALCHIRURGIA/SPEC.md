> **Layer 3** · Dental Sciences · `H11-ORALCHIRURGIA`

## Purpose
H11-ORALCHIRURGIA is the surgical intervention node, managing exodontia (tooth extractions), implantology, orthognathic surgery, and management of maxillofacial pathologies. It operates in environments where bone manipulation, nerve avoidance, and soft tissue flap design are critical.

This agent handles spatial collision detection between surgical instruments (drills, elevators) and vital anatomical structures such as the Inferior Alveolar Nerve (IAN) and the Maxillary Sinus. It generates surgical guides and prescribes pharmacological protocols for post-operative pain and infection management.

## Technical Deep-Dive
The agent processes volumetric DICOM data to isolate the IAN canal and sinus floor via convolutional neural networks (CNN) segmentation. For implant planning, it calculates Hounsfield Units (HU) to evaluate bone density (D1 to D4), selecting appropriate implant macro-geometry (taper, thread pitch) to maximize primary stability (insertion torque > 35 Ncm).

During simulated orthognathic surgery (e.g., Le Fort I osteotomy, Bilateral Sagittal Split Osteotomy), it employs biomechanical soft-tissue morphing algorithms to predict post-operative facial aesthetics based on skeletal movements. It calculates stress vectors on the Temporomandibular Joint (TMJ) capsule to avoid post-surgical condylar resorption.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| cbct_dicom | VoxelGrid | 3D radiological volume |
| surgical_goal | SurgicalObjective | E.g., Implant Placement, Extraction |
| medical_history | MedHistory | Bleeding disorders, medications |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| surgical_plan | SurgicalProtocol | Flap design, osteotomy steps |
| surgical_guide | MeshData | 3D printable stent for guided surgery |
| risk_assessment | Dict[str, float] | Probabilities of paresthesia, sinus perf. |

### State Schema
Maintains `SurgicalFieldState` tracking active bleeding rates, anesthesia efficacy (nerve block duration), and current osteotomy depth relative to vital structures.

## Dependencies

### Upstream
- H11-DENTALIS: Initial referral for un-restorable teeth.
- H11-ORTHODONTIA: Pre-surgical orthodontic alignment data.
- H11-PERIODONTIA: Ridge preservation requirements.

### Downstream
- H11-PROSTHODONTIA: Position of placed implants for prosthesis design.

## Failure Modes
1. **Nerve Injury:** Drill trajectory intersects the IAN canal leading to permanent paresthesia.
2. **Sinus Perforation:** Penetration of the Schneiderian membrane during maxillary implant placement without planned sinus lift.
3. **Osteonecrosis:** Excessive heat generation during drilling (>47 degrees C) causing bone death and implant failure.

## Performance Characteristics
High computational demand for volumetric rendering and real-time collision detection during virtual surgery simulation.

## Research References
- Misch, C. E. (2014). Contemporary Implant Dentistry.
- Hounsfield, G. N. (1980). Computed medical imaging.

## Implementation Notes
Implement a ray-casting boundary condition algorithm to simulate heat dissipation during the bone drilling sequence, adjusting coolant flow parameters dynamically.
