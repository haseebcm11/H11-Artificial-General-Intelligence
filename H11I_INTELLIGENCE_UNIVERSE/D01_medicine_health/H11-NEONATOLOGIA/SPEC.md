> **Layer 1** · Medicine & Health Sciences · `H11-NEONATOLOGIA`

## Purpose
The `H11-NEONATOLOGIA` agent models the physiological, developmental, and pathophysiological dynamics of neonates from birth through the post-neonatal transition (up to 44 weeks postmenstrual age). It specializes in extremely low birth weight (ELBW, <1000g), very low birth weight (VLBW, <1500g), late preterm, and critically ill term infants.

The agent computes vital neonatal scoring indices (APGAR, Silverman-Andersen, SNAPPE-II), models respiratory mechanics in Neonatal Respiratory Distress Syndrome (RDS) and Bronchopulmonary Dysplasia (BPD), evaluates hyperbilirubinemia trajectories against Bhutani/AAP nomograms, tracks Glucose Infusion Rates (GIR) and parentero-enteral fluid-electrolyte transitions, predicts Early-Onset Sepsis (EOS) risk, and guides neuroprotective strategies such as therapeutic hypothermia in Hypoxic-Ischemic Encephalopathy (HIE).

## Technical Deep-Dive

### 1. Cardiopulmonary Transition & Surfactant Kinetics
At birth, the neonatal lung transitions from liquid-filled alveoli to air breathing. The agent models the alveolar surface tension via the Laplace relationship $P = 2\gamma / r$, simulating dipalmitoylphosphatidylcholine (DPPC) surfactant dynamics. In surfactant deficiency (RDS), alveolar collapse and intrapulmonary shunting are simulated using a two-compartment ventilation-perfusion ($V_A/Q$) model. Oxygenation Index (OI) is computed as:
$$\text{OI} = \frac{\text{MAP} \times \text{FiO}_2 \times 100}{\text{PaO}_2}$$
Guiding decisions on exogenous surfactant instillation (e.g., poractant alfa, calfactant), non-invasive CPAP, synchronized intermittent mandatory ventilation (SIMV), and inhaled Nitric Oxide (iNO) for Persistent Pulmonary Hypertension of the Newborn (PPHN).

### 2. Bilirubin Kinetics & Phototherapy Thresholds
Unconjugated bilirubin clearance is modeled via UDP-glucuronosyltransferase 1A1 (UGT1A1) maturation kinetics, enterohepatic circulation, and albumin-binding capacity. The agent implements the American Academy of Pediatrics (AAP) 2022 guidelines and hour-specific Bhutani nomograms to generate real-time phototherapy and exchange transfusion recommendations categorized by neurotoxicity risk factors (e.g., hemolytic disease, gestational age < 38 weeks, sepsis, hypoalbuminemia).

### 3. Fluid Balance, GIR & Metabolic Homeostasis
Insensible water loss (IWL) is computed factoring in gestational age, birth weight, radiant warmers, phototherapy, and humidified incubator settings. The Glucose Infusion Rate is calculated via:
$$\text{GIR} \, (\text{mg/kg/min}) = \frac{\text{Dextrose Conc} \, (\%) \times \text{Infusion Rate} \, (\text{mL/hr}) \times 0.167}{\text{Weight} \, (\text{kg})}$$
Enabling real-time titration to prevent neonatal hypoglycemia (<45 mg/dL) and hyperglycemia-induced osmotic diuresis.

### 4. Perinatal Infection & Sepsis Risk Stratification
The agent implements the Kaiser Permanente Neonatal Early-Onset Sepsis (EOS) multivariate predictive model. It integrates maternal intrapartum temperature, rupture of membranes (ROM) duration, maternal Group B Streptococcus (GBS) colonization, intrapartum antibiotic prophylaxis (IAP), and the neonate's clinical examination to output sepsis risk per 1,000 live births and recommended action tiers.

### 5. Hypoxic-Ischemic Encephalopathy (HIE) & Neuroprotection
For term and near-term neonates ($\ge 35$ weeks) with perinatal asphyxia (cord pH $< 7.00$, base deficit $\ge 16$ mmol/L, APGAR $\le 5$ at 10 min, or ongoing resuscitation), the agent evaluates Sarnat staging (mild, moderate, severe) and amplitude-integrated EEG (aEEG) background patterns to determine eligibility for therapeutic whole-body hypothermia ($33.5^\circ\text{C} \pm 0.5^\circ\text{C}$ for 72 hours) within the critical 6-hour therapeutic window.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `gestational_age_weeks` | `float` | Gestational age at birth in weeks (e.g., 28.4) |
| `birth_weight_grams` | `float` | Birth weight in grams |
| `chronological_age_hours`| `float` | Postnatal age in hours |
| `apgar_scores` | `Dict[str, int]` | APGAR scores at 1, 5, and 10 minutes |
| `respiratory_metrics` | `SilvermanScoreInput` | Silverman-Andersen retraction and grunting metrics |
| `blood_gas` | `ArterialBloodGas` | pH, PaO2, PaCO2, Base Excess, Lactate |
| `bilirubin_panel` | `BilirubinAssessmentInput`| Total and direct serum bilirubin, hour of life, risk tier |
| `maternal_perinatal_data`| `MaternalPerinatalData` | GBS status, ROM hours, maternal fever, IAP |
| `hemodynamic_pda_echo` | `PDAEchoAssessment` | Ductal diameter, shunt direction, LA/Ao ratio |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `apgar_evaluation` | `APGARResult` | Resuscitation trajectory and neurodevelopmental risk flag |
| `respiratory_plan` | `RespiratoryDistressAssessment`| RDS severity, OI, surfactant eligibility, ventilator settings |
| `phototherapy_decision` | `BilirubinNomogramDecision`| Phototherapy/exchange transfusion urgency, hours to threshold |
| `fluid_metabolic_plan` | `FluidPlan` | Total fluids (mL/kg/day), GIR (mg/kg/min), electrolyte targets |
| `eos_sepsis_stratification`| `EOSRiskAssessment` | Posterior sepsis probability, blood culture/antibiotic recommendation |
| `hie_cooling_protocol` | `TherapeuticHypothermiaProtocol`| Target core temp, cooling phase, rewarming rate, aEEG targets |
| `nec_stage_assessment` | `NECStagingResult` | Modified Bell's staging, NPO duration, surgical consult alert |

### State Schema
Maintains `NeonatalPatientState`, encapsulating postmenstrual age (PMA), daily weights, caloric/protein intake, ventilator dependence days, phototherapy cumulative hours, brain cooling phase, and modified Bell's enterocolitis staging.

## Dependencies

### Upstream (depends on)
- `H11-GYNAECOLOGIA` / `H11-OBSTETRICIA`: For maternal prenatal records, gestational dating, Doppler flows, and labor dynamics.
- `H11-GENETICA-MED`: For screening congenital anomalies, inborn errors of metabolism, and chromosomal syndromes.
- `H11-IMMUNOLOGIA`: For maternal-fetal alloimmunization (Rh/ABO incompatibility) and neonatal innate immunity profiling.
- `H11-BACTERIOLOGIA`: For blood/CSF bacterial culture identification and antibiograms (GBS, E. coli, Listeria).

### Downstream (feeds into)
- `H11-PNEUMOLOGIA`: For long-term chronic lung disease / bronchopulmonary dysplasia (BPD) management.
- `H11-NEUROLOGIA`: For developmental follow-up, cerebral palsy risk modeling, and post-HIE neuroimaging (MRI).
- `H11-CARDIOLOGIA`: For persistent PDA closure hemodynamics, congenital heart defects, and persistent PPHN.
- `H11-NUTRITIO`: For post-discharge growth curves (Fenton/Intergrowth-21st), human milk fortification, and micronutrients.

## Failure Modes
1. **Phototherapy Threshold Miscalculation**: Rapid hemolytic rise in bilirubin outpacing static 12-hour testing intervals.
2. **Delayed Therapeutic Hypothermia Window**: Failing to initiate neuroprotective cooling prior to the 6-hour post-birth window closure.
3. **Over-Oxygenation in Preterm Retinopathy (ROP)**: Excessive PaO2/SpO2 fluctuations triggering hyperoxic retinal vascular obliteration and subsequent VEGF-driven neovascularization.
4. **Fluid Overload in PDA**: High fluid administration exacerbating left-to-right ductal shunting, pulmonary edema, and increasing NEC risk.

## Performance Characteristics
- High-priority APGAR & Resuscitation triage latency: < 5ms.
- Sepsis multivariate calculation & AAP 2022 Bhutani plot evaluation: < 15ms.
- Multi-compartment neonatal lung & surfactant kinetic simulation: < 100ms.

## Research References
1. AAP Subcommittee on Hyperbilirubinemia (2022). *Clinical Practice Guideline Revision: Management of Hyperbilirubinemia in the Newborn Infant 35 or More Weeks of Gestation*. Pediatrics, 150(3):e2022058859.
2. Puopolo, K. M., et al. (2018). *Management of Neonates Born at $\ge 35$ Weeks’ Gestation with Suspected or Proven Early-Onset Sepsis*. Pediatrics, 142(6):e20182894.
3. Sweet, D. G., et al. (2023). *European Consensus Guidelines on the Management of Respiratory Distress Syndrome: 2022 Update*. Neonatology, 120(1):3–23.
4. Shankaran, S., et al. (2005). *Whole-Body Hypothermia for Neonates with Hypoxic-Ischemic Encephalopathy*. N Engl J Med, 353(15):1574–1584.

## Implementation Notes
- All drug dosing and fluid calculators MUST strictly validate postmenstrual age (PMA) and current weight in grams/kilograms.
- Bilirubin risk thresholds interpolate spline curves from the updated 2022 AAP neurotoxicity risk tables.
- Hypothermia protocols implement precise rewarmed ramps ($\le 0.5^\circ\text{C}/\text{hr}$) to prevent sudden systemic hypotension and rebound seizures.
