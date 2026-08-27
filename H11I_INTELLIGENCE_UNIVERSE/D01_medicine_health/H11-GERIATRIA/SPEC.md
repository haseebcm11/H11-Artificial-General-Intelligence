> **Layer 1** · Medicine & Health Sciences · `H11-GERIATRIA`

## Purpose
The `H11-GERIATRIA` agent provides computational modeling, multidimensional risk assessment, and clinical decision support for aging biology, frailty syndromes, and multimorbidity management in older adults. It operationalizes the Comprehensive Geriatric Assessment (CGA) paradigm into an automated, quantitative reasoning engine capable of deciphering the complex interdependencies between functional decline, cognitive vulnerability, polypharmacy interactions, sarcopenia, and acute geriatric syndromes (e.g., delirium, falls).

By integrating phenotypic frailty models, deficit accumulation indices, pharmacogeriatric safety algorithms (Beers 2023 / STOPP/START v3), and intrinsic capacity trajectories (WHO ICOPE framework), `H11-GERIATRIA` optimizes care plans, prevents iatrogenic harm, and supports goal-concordant care across the continuum from healthy aging to advanced frailty and palliative transition.

## Technical Deep-Dive

### 1. Multidimensional Comprehensive Geriatric Assessment (CGA)
The agent executes automated multidimensional scoring spanning six core domains:
- **Functional Status:** Basic Activities of Daily Living (ADLs, Katz Index 0–6) and Instrumental Activities of Daily Living (IADLs, Lawton-Brody Index 0–8), tracking independence transitions and caregiver dependency.
- **Cognitive & Neuropsychiatric:** Cognitive reserve scoring (MMSE, MoCA, Mini-Cog) combined with affective mood screening via the Geriatric Depression Scale (GDS-15/30).
- **Nutritional & Metabolic:** Mini Nutritional Assessment (MNA) with BMI adjustment and unintended weight loss velocity tracking.
- **Mobility & Gait Biomechanics:** Timed Up and Go (TUG), Berg Balance Scale, and 4-meter gait velocity kinetics.
- **Polypharmacy & Anticholinergic Load:** Anticholinergic Cognitive Burden (ACB) scaling and drug-disease interaction filtering.
- **Socio-Environmental:** Caregiver burden, home safety vulnerabilities, and social isolation vulnerability scoring.

### 2. Dual Frailty Quantification (Phenotypic vs. Deficit Accumulation)
`H11-GERIATRIA` implements two complementary, mathematically distinct frailty paradigms:
1. **Fried Frailty Phenotype (Cardiovascular Health Study):** Evaluates 5 physical biomarkers (unintentional weight loss $\ge 5\%$, self-reported exhaustion, low physical activity energy expenditure, slowed 4m walking speed adjusted for sex/height, and weakened dynamometric grip strength adjusted for sex/BMI). Scores classify patients into *Robust* (0 criteria), *Pre-frail* (1–2 criteria), or *Frail* ($\ge 3$ criteria).
2. **Rockwood Frailty Index (Deficit Accumulation Model):** Computes a continuous frailty ratio:
   $$\text{FI} = \frac{\sum_{i=1}^{N} d_i}{N}$$
   across $\ge 30$ multi-system clinical, laboratory, cognitive, and functional deficits. The agent tracks non-linear mortality acceleration when $\text{FI} > 0.25$ and identifies the physiological saturation limit near $\text{FI} \approx 0.67$.

### 3. Sarcopenia & Musculoskeletal Staging (EWGSOP2)
Implements the European Working Group on Sarcopenia in Older People (EWGSOP2) consensus criteria:
- **Probable Sarcopenia:** Low muscle strength (Isometric handgrip strength $< 27\text{ kg}$ in men, $< 16\text{ kg}$ in women, or 5-times chair stand test $> 15\text{ s}$).
- **Confirmed Sarcopenia:** Documented low muscle quantity/quality via Appendicular Skeletal Muscle Mass (ASMM $< 20\text{ kg}$ or $< 7.0\text{ kg/m}^2$ for men; $< 15\text{ kg}$ or $< 5.5\text{ kg/m}^2$ for women via DEXA/BIA).
- **Severe Sarcopenia:** Confirmed sarcopenia accompanied by compromised physical performance (Gait speed $\le 0.8\text{ m/s}$ or 400m walk failure).

### 4. Pharmacogeriatrics, Deprescribing, and Anticholinergic Cognitive Burden
Older adults exhibit altered pharmacokinetics (reduced GFR, lower hepatic CYP450 clearance, decreased total body water, increased adipose distribution volume) and pharmacodynamics (increased sensitivity to CNS depressants and anticholinergics). The agent incorporates:
- **Beers Criteria (2023 AGS update):** Real-time interception of potentially inappropriate medications (PIMs), including sedatives, high-risk NSAIDs, tertiary TCAs, sliding-scale insulin, and long-acting sulfonylureas.
- **STOPP/START Criteria v3:** Systematic rules for deprescribing overtreatment and initiating evidence-based undertreatment (e.g., bone protection in chronic corticosteroid therapy, SGLT2i/GLP1-RA in frailty-adjusted diabetes targets).
- **Anticholinergic Burden Calculator:** Cumulative score summation ($0$ to $\ge 3$) correlating directly with delirium risk, fall probability, and cognitive decline acceleration.

### 5. Delirium Stratification (CAM / 4AT Engine)
Detects acute encephalopathy and delirium phenotypes (hyperactive, hypoactive, mixed) using the Confusion Assessment Method (CAM) algorithm:
$$\text{Delirium} = \text{Feature 1 (Acute Onset \& Fluctuating)} \land \text{Feature 2 (Inattention)} \land [\text{Feature 3 (Disorganized Thinking)} \lor \text{Feature 4 (Altered Consciousness)}]$$
The agent specifically monitors for masked hypoactive delirium, often misattributed to depression or dementia progression.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `patient_id` | `str` | Unique subject identifier |
| `age` | `int` | Chronological age in years |
| `sex` | `Sex` | Biological sex (`MALE`, `FEMALE`) |
| `adl_metrics` | `ADLMetrics` | Katz Basic ADL score breakdown (0–6) |
| `iadl_metrics` | `IADLMetrics` | Lawton-Brody Instrumental ADL scores (0–8) |
| `cognitive_scores` | `Dict[str, float]` | MMSE (0–30), MoCA (0–30), GDS-15 (0–15) |
| `physical_performance`| `PhenotypeMetrics` | Grip strength (kg), gait speed (m/s), TUG (s), weight loss |
| `medications` | `List[Medication]` | Full active drug regimen with dosages and anticholinergic weights |
| `deficits_list` | `List[DeficitItem]`| Binary/graded deficit checklist for Rockwood Frailty Index |
| `renal_function` | `float` | Estimated GFR (mL/min/1.73m²) |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `cga_report` | `CGAReport` | Synthesized multi-domain assessment with deficit scores |
| `frailty_status` | `FrailtyStatus` | `ROBUST`, `PRE_FRAIL`, or `FRAIL` phenotype |
| `frailty_index` | `float` | Continuous Rockwood Index ($0.00 - 1.00$) |
| `sarcopenia_stage` | `SarcopeniaStage` | EWGSOP2 classification (`NONE`, `PROBABLE`, `CONFIRMED`, `SEVERE`) |
| `delirium_status` | `DeliriumAssessment`| CAM/4AT delirium evaluation and risk breakdown |
| `deprescribing_plan` | `DeprescribingRecommendation` | Identified PIMs, anticholinergic score, and tapering advice |
| `falls_risk` | `FallsRiskStratification` | Multi-factorial fall risk tier and targeted interventions |

### State Schema
Maintains `GeriatricPatientState` capturing longitudinal functional trajectories, historical CGA evaluations, chronic geriatric syndromes, and real-time anticholinergic drug exposure.

## Dependencies

### Upstream (depends on)
- `H11-FARMACOLOGIA`: For raw pharmacokinetic parameters, half-life modifications, and drug interaction databases.
- `H11-NEUROLOGIA`: For differentiating underlying neurodegenerative dementias (Alzheimer's, Lewy Body, FTD) from delirium.
- `H11-ENDOCRINOLOGIA`: For frailty-adjusted glycemic targets, thyroid balance, and sarcopenia-related endocrine decline.
- `H11-NUTRITIO`: For micronutrient deficiencies, protein intake targets, and cachexia/sarcopenia dietary optimization.

### Downstream (feeds into)
- `H11-PALLIATIVA`: Supplies frailty progression milestones and prognostication data for palliative transitions.
- `H11-REHABILITATIO`: Delivers target physical therapy, balance training, and functional restorative goals.
- `H11-CARDIOLOGIA`: Provides frailty-adjusted blood pressure goals and anticoagulation risk-benefit trade-offs in AFib.
- `H11-ORTHOPAEDIA`: Feeds bone fragility metrics and pre-operative peri-surgical risk stratification for fracture prevention.

## Failure Modes
1. **Atypical Presentation Masking:** Failure to detect systemic infection, myocardial infarction, or acute abdomen due to absence of fever, leukocytosis, or classic pain responses in frail elders.
2. **Hypoactive Delirium Under-detection:** Misclassifying quiet, lethargic hypoactive delirium states as baseline dementia or depressive withdrawal.
3. **Deprescribing Withdrawal & Rebound Shocks:** Abrupt cessation of long-term benzodiazepines, beta-blockers, or PPIs causing rebound insomnia, tachycardia, or severe dyspepsia rather than phased tapering.
4. **Deficit Saturation Artifacts:** Distortion in Rockwood FI calculation when duplicate or non-independent clinical symptoms are over-counted in the deficit denominator.
5. **Sarcopenic Obesity Concealment:** Missing profound muscle mass depletion in overweight/obese patients where high adiposity masks low skeletal muscle index.

## Performance Characteristics
- Multi-domain CGA synthesis and rule-matching executed in $< 15\text{ ms}$.
- Complete Beers/STOPP/START polypharmacy matrix cross-referenced across 50+ medications in $< 8\text{ ms}$.
- Deterministic frailty scoring with reproducible trajectory extrapolation over longitudinal horizons.

## Research References
1. Fried, L. P., et al. (2001). *Frailty in older adults: evidence for a phenotype*. The Journals of Gerontology Series A, 56(3), M146–M157.
2. Rockwood, K., & Mitnitski, A. (2007). *Frailty in relation to the accumulation of deficits*. Clinics in Geriatric Medicine, 23(3), 505–516.
3. Cruz-Jentoft, A. J., et al. (2019). *Sarcopenia: revised European consensus on definition and diagnosis (EWGSOP2)*. Age and Ageing, 48(1), 16–31.
4. American Geriatrics Society (2023). *American Geriatrics Society 2023 updated AGS Beers Criteria® for potentially inappropriate medication use in older adults*. Journal of the American Geriatrics Society, 71(7), 2052–2081.
5. O’Mahony, D., et al. (2023). *STOPP/START criteria for potentially inappropriate prescribing in older people: version 3*. European Geriatric Medicine, 14(4), 625–632.

## Implementation Notes
Implements vector-based deficit aggregation, validated threshold lookups for sarcopenia metrics, and rule engines for geriatric prescribing safety. All asynchronous state mutations preserve thread safety across multi-patient cohort queries.
