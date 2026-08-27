# H11-OBSTETRICIA — Obstetrics & Maternal-Fetal Medicine
> **Layer 1** · Medicine & Health Sciences · `H11-OBSTETRICIA`

## Purpose
The `H11-OBSTETRICIA` agent delivers high-fidelity cognitive models for maternal-fetal medicine, prenatal surveillance, intrapartum monitoring, and postpartum care. It models physiological adaptations of gestation, computes gestational age and fetal biometric growth trajectories via Hadlock equations, stratifies hypertensive disorders of pregnancy (gestational hypertension, preeclampsia, HELLP syndrome), interprets intrapartum cardiotocography (NICHD Category I/II/III CTG tracings), assesses labor induction readiness via Bishop scoring, and evaluates postpartum hemorrhage (PPH) risk.

## Technical Deep-Dive
Obstetric physiology is governed by coupled maternal-placental-fetal dynamic systems:
1. **Fetal Biometry & Growth Kinetics**: Estimated Fetal Weight (EFW) is derived from biparietal diameter (BPD), head circumference (HC), abdominal circumference (AC), and femur length (FL) using 4-parameter Hadlock regression models ($log_{10} EFW = 1.3596 - 0.00386(AC)(FL) + 0.0064(HC) + 0.00061(BPD)(AC) + 0.0424(AC) + 0.174(FL)$). Percentiles are indexed against gestational age based on WHO and INTERGROWTH-21st fetal growth standards to detect Fetal Growth Restriction (FGR, <10th percentile; severe <3rd percentile) and Large for Gestational Age (LGA, >90th percentile).
2. **Cardiotocography (CTG) & Fetal Oxygenation**: Real-time fetal heart rate (FHR) signals and uterine activity (TOCO) are decomposed into baseline FHR (110–160 bpm), baseline variability (absent, minimal <5 bpm, moderate 6–25 bpm, marked >25 bpm), episodic/periodic accelerations, and decelerations (early/head compression, late/uteroplacental insufficiency, variable/cord compression, prolonged). The agent implements the 3-tier NICHD/ACOG/FIGO intrapartum categorization algorithm.
3. **Preeclampsia & Endothelial Dysfunction Risk Engine**: Incorporates mean arterial pressure (MAP), uterine artery Doppler pulsatility index (UtA-PI), maternal serum biomarkers (soluble fms-like tyrosine kinase-1 to placental growth factor ratio, $sFlt\text{-}1/PlGF$), proteinuria ($mg/24h$ or protein/creatinine ratio $\ge 0.3$), and liver transaminases/platelet kinetics to predict early-onset (<34 weeks) vs. late-onset preeclampsia and impending eclamptic or HELLP decompensation.
4. **Labor Dynamics & Induction Readiness**: Evaluates the modified Bishop score (cervical dilation, effacement, station, consistency, position) and models uterine contraction frequency and Montevideo units (MVU) to guide oxytocin titration and predict vaginal delivery success.
5. **Postpartum Hemorrhage (PPH) & 4T Assessment**: Stratifies obstetric hemorrhage risk across the "4Ts" (Tone/uterine atony, Tissue/retained placenta or accreta spectrum, Trauma/lacerations, Thrombin/coagulopathy) and monitors cumulative blood loss against shock index ($SI = HR / SBP \ge 0.9$).

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `gestational_profile` | `GestationalProfile` | LMP, dating ultrasound CRL/EDD, parity, gravidity, chronologic gestational age. |
| `fetal_biometry` | `FetalBiometry` | BPD, HC, AC, FL, Amniotic Fluid Index (AFI) or Maximum Vertical Pocket (MVP). |
| `ctg_features` | `CTGFeatures` | Baseline FHR, baseline variability, presence of accelerations, deceleration types, contraction frequency. |
| `maternal_vitals_biomarkers` | `MaternalVitalsBiomarkers` | Blood pressure (SBP/DBP), MAP, sFlt-1/PlGF ratio, 24h urine protein, platelets, AST/ALT, LDH. |
| `cervical_assessment` | `CervicalAssessment` | Dilation (cm), effacement (%), station (-3 to +3), cervical consistency, cervical position. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `gestational_age_days` | `int` | Refined gestational age in days and weeks. |
| `estimated_fetal_weight_g` | `float` | Hadlock calculated EFW in grams. |
| `growth_percentile` | `float` | Gestational age-matched fetal growth percentile. |
| `fgr_status` | `str` | Normal, FGR, Severe FGR, or LGA. |
| `ctg_category` | `str` | NICHD Category I (Normal), Category II (Indeterminate), or Category III (Abnormal). |
| `preeclampsia_risk` | `PreeclampsiaRiskResult` | Risk probability, classification, and angiogenic biomarker interpretation. |
| `bishop_score` | `int` | Modified Bishop score (0–13) and induction recommendation. |
| `pph_risk_tier` | `str` | Low, Medium, High, or Active Hemorrhage Alert. |

### State Schema
Maintains `ObstetricState`, tracking serial fundal heights, serial EFW percentiles across trimesters, umbilical/uterine artery Doppler waveform trends, maternal blood pressure trajectory, and labor progression curve (Friedman / Zhang partogram).

## Dependencies
### Upstream (depends on)
- `H11-GYNAECOLOGIA`: Pre-conception ovarian status, uterine anomalies (septate/bicornuate uterus, fibroids).
- `H11-RADIOLOGIA`: Ultrasound biometry metrics, placental location/grading, Doppler velocimetry (UtA, UA, MCA).
- `H11-GENETICA-MED`: Non-invasive prenatal testing (NIPT cfDNA), chorionic villus sampling (CVS), amniocentesis karyotype/microarray results.
- `H11-ENDOCRINOLOGIA`: Pre-existing or gestational diabetes mellitus (GDM) insulin regulation, maternal thyroid status.
- `H11-CARDIOLOGIA`: Maternal cardiovascular reserve, gestational hemodilution, peripartum cardiomyopathy screening.

### Downstream (feeds into)
- `H11-NEONATOLOGIA`: Transition of care at birth, delivery record, APGAR projection, cord blood pH, gestational maturity handoff.
- `H11-ANAESTHESIA`: Obstetric anesthesia planning (neuraxial analgesia eligibility, airway edema risk, preeclampsia coagulopathy checks).
- `H11-CHIRURGIA`: Operative vaginal delivery and Cesarean section readiness, placenta accreta spectrum surgical planning.
- `H11-HEMATOLOGIA`: Management of maternal alloimmunization (Rh immunoglobulin dosing), gestational thrombocytopenia, DIC/PPH massive transfusion protocols.

## Failure Modes
- **Pseudonormalized CTG**: Misinterpreting absent variability with sinusoidal rhythm as benign baseline without identifying acute severe fetal anemia or severe hypoxia.
- **Biometry Discordance in Multiple Gestations**: Overlooking selective fetal growth restriction (sFGR) or Twin-to-Twin Transfusion Syndrome (TTTS) due to averaging biometric indices.
- **Atypical Preeclampsia Underdiagnosis**: Over-relying on hypertension alone and missing normotensive preeclampsia with acute liver injury or thrombocytopenia (HELLP syndrome).
- **Concealed Placental Abruption**: Failing to detect uterine hypertonus and fetal bradycardia when external vaginal bleeding is absent.

## Performance Characteristics
- Hadlock EFW and growth curve percentile evaluation: $<2\text{ ms}$.
- NICHD 3-tier CTG algorithmic classification: $<5\text{ ms}$.
- Multi-variate preeclampsia risk scoring and angiogenic ratio evaluation: $<10\text{ ms}$.
- Full antenatal/intrapartum multi-modal panel analysis: $<25\text{ ms}$.

## Research References
1. Hadlock, F. P., et al. (1985). Estimation of fetal weight with the use of head, body, and femur measurements—a prospective study. *Am J Obstet Gynecol*, 151(3), 333-337.
2. Macones, G. A., et al. (2008). The 2008 National Institute of Child Health and Human Development workshop report on electronic fetal monitoring: update on definitions, interpretation, and guidelines. *Obstet Gynecol*, 112(3), 661-666.
3. Zeisler, H., et al. (2016). Predictive Value of the sFlt-1:PlGF Ratio in Women with Suspected Preeclampsia. *N Engl J Med*, 374(1), 13-22.
4. American College of Obstetricians and Gynecologists (ACOG). (2020). Gestational Hypertension and Preeclampsia: ACOG Practice Bulletin No. 222. *Obstet Gynecol*, 135(6), e237-e260.
5. Zhang, J., et al. (2010). Contemporary patterns of spontaneous labor with normal neonatal outcomes. *Obstet Gynecol*, 116(6), 1281-1287.

## Implementation Notes
Use strict boundary validation for gestational ages (valid range: 4 to 43 completed weeks). Hadlock logarithmic formulas must clamp negative or zero biometric parameters to prevent domain errors. CTG classification conforms directly to NICHD / ACOG standardized category definitions.
