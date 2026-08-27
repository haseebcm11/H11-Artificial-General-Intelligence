> **Layer 23** · Allied Health · `H11-SPEECH`

## Purpose

The H11-SPEECH agent (SpeechPathologyAgent) focuses on communication disorders and swallowing mechanisms (dysphagia). It analyzes acoustic phonetic properties, natural language pragmatics, and videofluoroscopic swallowing study (VFSS) telemetry to diagnose and rehabilitate oropharyngeal deficits.

It bridges the gap between neurology, gastroenterology, and functional communication, ensuring safe deglutition and effective expressive/receptive language.

## Technical Deep-Dive

For dysphagia analysis, the agent employs kinematic analysis of the hyolaryngeal complex using edge-detection algorithms on VFSS imagery. It calculates airway invasion risks using the Penetration-Aspiration Scale (PAS).

For speech and language, it utilizes Mel-frequency cepstral coefficients (MFCCs) and prosodic feature extraction to identify dysarthria, apraxia, or aphasia subtypes. It implements a generative model of linguistic syntax to map lexical retrieval failures to specific neurological lesion topologies.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| acoustic_features | AudioTensor | Extracted voice/speech metrics |
| vfss_kinematics | SwallowingDynamics | Hyoid excursion and timing data |
| language_sample | NLPStruct | Transcribed spontaneous speech |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| dysphagia_diet | DietTexture | Recommended IDDSI level |
| aphasia_classification | AphasiaType | Broca's, Wernicke's, etc. |
| therapy_targets | List[SpeechTarget] | Specific phonetic/linguistic goals |

### State Schema
- `aspiration_risk_profile`: Boolean flag indicating acute risk.
- `lexical_inventory`: Map of successfully retrieved semantic tokens.

## Dependencies

### Upstream (depends on)
- H11-NEURO (brain lesion data)
- H11-ENT (laryngeal structure)

### Downstream (feeds into)
- H11-DIETETICA (for safe diet textures)

## Failure Modes
- Silent aspiration goes undetected due to poor VFSS temporal resolution.
- Misclassification of apraxia vs. aphasia due to overlapping acoustic features.

## Performance Characteristics
High computational load for audio processing (MFCC extraction) and video frame analysis. Requires real-time processing (<100ms) for biofeedback therapy modes.

## Research References
- Penetration-Aspiration Scale (Rosenbek).
- International Diet Standardisation Initiative (IDDSI).
- Boston Diagnostic Aphasia Examination principles.

## Implementation Notes
Implement strict typing around IDDSI levels to prevent catastrophic diet errors. Use Fast Fourier Transforms (FFT) for real-time pitch/formant tracking.
