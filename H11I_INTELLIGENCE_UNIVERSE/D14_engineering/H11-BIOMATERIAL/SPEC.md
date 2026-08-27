# H11-BIOMATERIAL Agent Specification

## 1. System Overview
The H11-BIOMATERIAL agent is dedicated to tissue engineering, biocompatibility simulation, scaffold degradation modeling, and implant surface interactions.

## 2. Core Architecture
- **Biocompatibility Grader**: Analyzes ISO 10993 cytotoxicity and sensitization profiles for new polymers and alloys.
- **Degradation Kinetics Simulator**: Models hydrolytic and enzymatic degradation of bioresorbable polymers (e.g., PLGA, PCL).
- **Surface Topology Optimizer**: Recommends micro-topographical structures to promote or inhibit osteointegration and cellular adhesion.
- **Rheology Engine**: Models fluid dynamics of hydrogel bioinks used in 3D bioprinting.

## 3. Interfaces
- `simulate_degradation(polymer_type: str, molecular_weight: float, environment_ph: float) -> DegradationCurve`
- `assess_cytotoxicity(chemical_composition: dict) -> ISO10993Score`
- `optimize_bioink_rheology(shear_rate: float, temperature: float) -> ViscosityProfile`

## 4. Performance Metrics
- **Degradation Prediction**: Accurately matches in-vitro half-life within 5%.
- **Biocompatibility Accuracy**: Matches known FDA MAF database toxicity scores with 99% precision.
- **Rheological Precision**: Evaluates non-Newtonian behavior of complex bioinks in <10 seconds.

## 5. Security & Compliance
- Adheres strictly to ISO 10993 (Biological evaluation of medical devices).
- PII and PHI data sanitization when handling patient-specific implant modeling data.
