# H11-SUPERCONDUCTOR Agent Specification

## 1. System Overview
The H11-SUPERCONDUCTOR agent models low-temperature physics, Type-II superconductor vortex pinning, critical current density ($J_c$) optimization, and cryogenic cooling loop integrations.

## 2. Core Architecture
- **BCS Theory Calculator**: Predicts $T_c$ (Critical Temperature) based on Bardeen-Cooper-Schrieffer or McMillan equations.
- **Magnetic Flux Simulator**: Models Meissner effect and London penetration depths.
- **Cryostat Designer**: Computes thermal loads, helium boil-off rates, and pulse-tube refrigerator capacities.
- **Material Synthesizer**: Predicts optimal stoichiometry for YBCO, BSCCO, and newly theorized hydride superconductors.

## 3. Interfaces
- `calculate_critical_temperature(dos: float, debye_freq: float, electron_phonon_coupling: float) -> float`
- `simulate_vortex_lattice(b_field_tesla: float, temp_k: float) -> VortexLatticeData`
- `design_cryocooler(heat_load_w: float, target_temp_k: float) -> CryoSystemConfig`

## 4. Performance Metrics
- **$T_c$ Prediction Error**: Mean Absolute Error (MAE) < 2.5K for known cuprates.
- **Magnetic Simulation Resolution**: Sub-nanometer vortex core resolving.
- **Thermal Load Computation**: Follows standard NIST cryogenics property databases accurately.

## 5. Security & Compliance
- Compliance with pressurized gas safety regulations (ASME Boiler and Pressure Vessel Code).
- High magnetic field exposure limits modeled per WHO/ICNIRP guidelines.
