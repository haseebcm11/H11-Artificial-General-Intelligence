# H11-SEDIMENTOLOGIA: Sedimentology & Stratigraphy Agent

## Purpose
The H11-SEDIMENTOLOGIA agent models the processes of erosion, transport, deposition, and diagenesis of sedimentary materials. It interprets stratigraphic sequences to reconstruct basin histories and paleoenvironments, playing a crucial role in sequence stratigraphy and basin analysis.

Operating within the Earth & Environmental Sciences domain, this agent provides quantitative models for sediment transport dynamics and stratigraphic forward modeling to predict facies distribution in sedimentary basins.

## Technical Deep Dive
The architecture integrates fluid dynamics for particle settling and bedload transport equations (e.g., Shields parameter, Exner equation) with sequence stratigraphic principles (accommodation space vs. sediment supply).

**Key capabilities:**
- **Stratigraphic Forward Modeling**: Simulates basin filling over geological time, accounting for eustatic sea-level changes, tectonic subsidence, and variable sediment flux.
- **Facies Analysis**: Interprets sedimentary structures and grain size distributions (e.g., Markov chain analysis of lithofacies transitions) to deduce depositional environments.
- **Sediment Transport Dynamics**: Calculates critical shear stress, settling velocities, and transport rates for various clast sizes in fluvial, aeolian, and marine environments.

**Architecture Contracts:**
Input JSON must include eustatic curves, subsidence rates, or empirical stratigraphic columns (lithology, grain size, bed thickness). Output JSON produces facies architecture predictions, synthetic well logs, or transport thresholds.
Dependencies: Interfaces with H11-PALEONTOLOGIA for biostratigraphic age constraints and paleoenvironmental indicators.
