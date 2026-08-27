# H11-SEMICONDUCTOR Agent Specification

## 1. System Overview
The H11-SEMICONDUCTOR agent focuses on automating microarchitecture design rules, photolithography optimization, doping profile simulations, and yield prediction models.

## 2. Core Architecture
- **Lithography Simulator**: Simulates optical proximity correction (OPC) and dose margins.
- **TCAD Interface**: Bridges to technology computer-aided design tools for semiconductor device physics.
- **Yield Predictor**: Machine learning model that predicts die yield based on defect densities and layout density.
- **Process Flow Engine**: Organizes standard CMOS steps (Deposition, Photo, Etch, Implantation, Anneal, CMP).

## 3. Interfaces
- `simulate_doping_profile(energy_kev: float, dose: float) -> DopingProfile`
- `optimize_opc_mask(layout_gds: bytes) -> bytes`
- `predict_wafer_yield(defect_density_per_cm2: float, die_area_cm2: float) -> YieldReport`

## 4. Performance Metrics
- **OPC Convergence Time**: <1 hour per reticle field.
- **Yield Accuracy**: Predicts within 3% of actual fabrication yield.
- **Resolution Limit**: Supports multi-patterning down to 2nm node geometries.

## 5. Security & Compliance
- Strict intellectual property controls on GDSII file handling.
- ITAR compliance module for sensitive radiation-hardened designs.
