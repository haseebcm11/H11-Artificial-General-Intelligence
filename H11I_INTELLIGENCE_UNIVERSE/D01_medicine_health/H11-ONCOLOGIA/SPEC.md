> **Layer 1** · Medicine & Health Sciences · `H11-ONCOLOGIA`

## Purpose
The H11-ONCOLOGIA agent serves as the core intelligence substrate for clinical and translational oncology. It models oncogenesis, tumor microenvironmental evolution, genomic driver landscapes, anatomical and prognostic TNM staging (AJCC/UICC 8th Edition), Gompertzian tumor growth kinetics under selective therapeutic pressures (Norton-Simon hypothesis), RECIST 1.1 longitudinal response tracking, subclonal heterogeneity, synthetic lethality vulnerabilities (e.g., homologous recombination deficiency / PARP inhibition, MSI-H / anti-PD-1 axis), and algorithmic Virtual Tumor Board (VTB) multi-modality regimen stratification.

## Technical Deep-Dive
Cancer progression is modeled as a multi-scale dynamic system integrating molecular genomics, spatial tumor growth kinetics, and evolutionary clonal selection:
1. **Mathematical Tumor Kinetics**: Implements Gompertzian growth kinetics:
   $$\frac{dV(t)}{dt} = \alpha V(t) \ln\left(\frac{K}{V(t)}\right) - \kappa(D, t) V(t)$$
   where $K$ represents carrying capacity, $\alpha$ is intrinsic proliferation rate, and $\kappa(D, t)$ represents dose-dense cytoreductive kill rate modeled via the Norton-Simon hypothesis.
2. **AJCC 8th Edition Staging & Biomarker Integration**: Evaluates anatomical primary tumor invasion ($T_0-T_4$), regional lymph node involvement ($N_0-N_3$), and distant metastasis ($M_0-M_1$), integrated with tumor-specific biological modifiers (histological grade $G_1-G_4$, hormone receptor status ER/PR/HER2, Ki-67, PSA/Gleason grade groups, HPV/p16 status, and microsatellite instability).
3. **RECIST 1.1 Automated Analytics**: Tracks sum of longest diameters (SLD) of baseline target lesions, adjusts for pathological lymph nodes (short axis $\ge 15\text{ mm}$ target, $\ge 10\text{ mm}$ non-target), detects progressive nadir elevations ($\ge 20\%$ increase and $\ge 5\text{ mm}$ absolute increase) or partial regression ($\ge 30\%$ decrease), and integrates non-target/new lesion metrics for objective response classification (CR, PR, SD, PD).
4. **Clonal Evolution & Resistance Trajectories**: Simulates subclone branching processes with shifting variant allele frequencies (VAF), anticipating targeted therapy secondary resistance gates (e.g., EGFR T790M/C797S under osimertinib, KRAS G12C switch mutations, ESR1 ligand-binding domain mutations).
5. **Precision Oncology Stratification**: Maps genomic alterations across AMP/ASCO/CAP Tiers I–IV, evaluating oncogene addictions, tumor mutational burden (TMB $\ge 10\text{ mut/Mb}$), homologous recombination repair deficiency (HRD), and actionable fusions (NTRK, ALK, ROS1, RET).

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `cancer_type` | `CancerType` | Primary anatomical cancer classification (e.g., NSCLC, BREAST, COLORECTAL, MELANOMA) |
| `tnm_raw` | `TNMDescriptor` | Clinical/pathological T, N, M descriptors, grade, and site-specific biomarker flags |
| `genomic_variants` | `List[GenomicVariant]` | Curated somatically identified variants with VAF, Tiering, and drug sensitivities |
| `serial_lesions` | `List[LesionMeasurement]` | Longitudinal target/non-target lesion caliper measurements across imaging timepoints |
| `treatment_history` | `List[TreatmentRegimen]` | Historical systemic, surgical, and radiation treatments with prior response nadirs |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `staging_result` | `TNMStageResult` | AJCC 8th Ed anatomical stage, prognostic stage group, and risk classification |
| `recist_assessment` | `RECISTEvaluation` | Quantitative SLD change, nadir delta, and overall RECIST 1.1 response category |
| `kinetic_projection` | `Dict[str, Any]` | Gompertzian volumetric trajectory over 30/60/180 days under candidate therapies |
| `stratified_regimens` | `List[TreatmentRegimen]` | Ranked therapeutic options with clinical evidence tier, predicted PFS, and rationale |
| `vtb_consensus` | `Dict[str, Any]` | Multidisciplinary Virtual Tumor Board synthesis, biomarker insights, and monitoring plan |

### State Schema
Maintains `OncologyPatientState`, an evolving longitudinal case record containing:
- Baseline disease topography and histopathology
- Serial imaging caliper measurements & target lesion SLD histories
- Clonal subpopulation architecture with historical and emergent VAF profiles
- Cumulative line-of-therapy regimens and toxicity profiles

## Dependencies
### Upstream (depends on)
- `H11-PATHOLOGIA`: Histopathology grades, architectural atypia, immunohistochemical stains.
- `H11-GENETICA-MED`: Germline cancer susceptibility variants (BRCA1/2, Lynch mismatch genes, TP53 Li-Fraumeni).
- `H11-PHARMACOGENOMICA`: DPYD, UGT1A1, TPMT, and CYP2D6 metabolizer status for chemotherapy dosing.
- `H11-RADIOLOGIA`: Volumetric lesion segmentations and RECIST caliper coordinates from CT/MRI/PET-CT.

### Downstream (feeds into)
- `H11-IMMUNOTHERAPIA`: Tumor mutational burden, neoantigen density, and PD-L1 TPS/CPS for biologic design.
- `H11-CHIRURGIA`: Resectability assessments, margin status requirements, and neoadjuvant downstaging targets.
- `H11-NUCLEARIS-MED`: Theranostic target selection (e.g., PSMA-PET/Lu-177, DOTATATE-PET/Lu-177).
- `H11-PALLIATIVA`: Symptom burden trajectories, performance status decline, and supportive care triggers.

## Failure Modes
1. **Pseudoprogression Confounding**: Transient immune infiltrate swelling mimicking progressive disease on RECIST 1.1 before delayed regression; mitigated via iRECIST/imRECIST criteria integration.
2. **Subclonal Sampling Bias**: Tissue biopsy missing spatially distant resistant subclones; mitigated by ctDNA liquid biopsy VAF tracking.
3. **Non-Standard Staging Violations**: Applying epithelial TNM criteria to hematologic, pediatric, or CNS malignancies; mitigated by strict site validation guards.

## Performance Characteristics
- **Compute Intensity**: Moderate-High. Gompertzian numerical ODE integration executes in $<5\text{ ms}$; multi-agent tumor board combinatorial stratification executes in $<50\text{ ms}$.
- **Memory Footprint**: Low-Moderate ($\sim 16-64\text{ MB}$ per longitudinal case state including dense serial lesion geometries).

## Research References
- Amin MB, et al. *The Eighth Edition AJCC Cancer Staging Manual: Continuing to build a bridge from a population-based to a more "personalized" approach to cancer staging.* CA Cancer J Clin. 2017.
- Eisenhauer EA, et al. *New response evaluation criteria in solid tumours: Revised RECIST guideline (version 1.1).* Eur J Cancer. 2009.
- Hanahan D. *Hallmarks of Cancer: New Dimensions.* Cancer Discovery. 2022.
- Norton L, Simon R. *Tumor size, sensitivity to therapy, and design of treatment schedules.* Cancer Treat Rep. 1977.

## Implementation Notes
Employs pure Python scientific primitives and NumPy-accelerated trajectory integrations. Implements explicit exception hierarchies (`InvalidStagingInputError`, `RECISTCalculationError`) and strict dataclass type safety for all inter-agent protocol exchanges.
