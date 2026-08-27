> **Layer 1** · Medicine & Health Sciences · `H11-CARDIOLOGIA`

## Purpose
The H11-CARDIOLOGIA agent manages the computational modeling of the cardiovascular system, encompassing electrophysiology, hemodynamics, and myocardial mechanics. It provides high-fidelity simulations of the heart's electrical conduction and mechanical pumping function to diagnose arrhythmias, ischemic events, and structural heart diseases.

It acts as the primary analytical engine for ECG interpretations, echocardiographic fluid dynamics, and vascular compliance models, supporting both acute care (e.g., myocardial infarction) and chronic management (e.g., heart failure).

## Technical Deep-Dive
The electrophysiological component employs the Aliev-Panfilov or monodomain reaction-diffusion equations to simulate the propagation of action potentials across the atrial and ventricular myocardium. It accounts for ion channel dynamics (Na+, K+, Ca2+) to predict re-entrant arrhythmias and QT prolongation in response to pharmacological inputs.

Hemodynamics are modeled using a lumped-parameter (Windkessel) model coupled with finite element analysis (FEA) of the left ventricular wall stress. This dual approach allows the agent to evaluate ejection fraction, end-diastolic pressure-volume relationships (EDPVR), and transvalvular pressure gradients with exceptional accuracy.

Vascular modeling incorporates Navier-Stokes equations for non-Newtonian blood flow in major arteries, calculating endothelial shear stress (ESS) to predict atherosclerotic plaque progression and rupture vulnerability in coronary vessels.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `ecg_leads` | `Matrix[12, T]` | 12-lead electrocardiogram time series |
| `echo_params` | `EchoMetrics` | Strain rates, ejection fraction, valve areas |
| `blood_pressure` | `ArterialWaveform` | Continuous invasive or non-invasive BP waveform |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `arrhythmia_map` | `3DActivationMap` | Spatiotemporal map of cardiac depolarization |
| `pv_loop` | `PressureVolumeLoop` | Reconstructed LV pressure-volume relationship |
| `plaque_vulnerability` | `StressTensor` | ESS and plaque structural stress |

### State Schema
Maintains `CardiacHemodynamicState` tracking chronic remodeling metrics (e.g., LV mass index) and electrophysiological substrate changes (e.g., fibrosis burden).

## Dependencies
### Upstream (depends on)
- `H11-HEMATOLOGIA`: For blood viscosity and coagulability impacting hemodynamics.
- `H11-ENDOCRINOLOGIA`: For RAAS axis and catecholamine influences on vascular tone.
### Downstream (feeds into)
- `H11-PNEUMOLOGIA`: For cardiopulmonary interactions (cor pulmonale, pulmonary edema).
- `H11-NEUROLOGIA`: For stroke risk stratification in atrial fibrillation.

## Failure Modes
1. **Mesh Tangling:** FEA divergence during excessive systolic deformation in severe hypertrophic cardiomyopathy simulations.
2. **Action Potential Instability:** Numerical instability in stiff ion channel ODEs leading to artificial fibrillation patterns.
3. **Boundary Condition Errors:** Incorrect assumptions in coronary outflow boundaries causing reversed flow artifacts.

## Performance Characteristics
- Solves 1D Windkessel models in <10ms.
- Full 3D electrophysiology simulation over 1 cardiac cycle (~800ms) computes in ~2.5s.

## Research References
1. *Patient-Specific Modeling of Cardiac Electrophysiology*, IEEE Transactions on Biomedical Engineering.
2. *Computational Fluid Dynamics in Coronary Artery Disease*, Biomechanics and Modeling in Mechanobiology.

## Implementation Notes
Utilize GPU acceleration (CUDA/OpenCL) for the 3D monodomain reaction-diffusion solver. Implement adaptive time-stepping for the action potential upstroke to ensure numerical stability.
