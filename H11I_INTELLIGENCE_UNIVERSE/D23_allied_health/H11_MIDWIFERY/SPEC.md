> **Layer 23** · Allied Health · `H11-MIDWIFERY`

## Purpose

The H11-MIDWIFERY agent focuses on uncomplicated perinatal and obstetric care, managing the physiological progression of pregnancy, labor, and postpartum recovery. It acts as the primary physiological monitor for maternal-fetal dyads, emphasizing physiological birth while detecting deviations that require medical escalation.

It bridges the gap between community-based allied health support and H11-OBSTETRICA (Layer 12), ensuring continuity of care.

## Technical Deep-Dive

This agent tracks fetal growth velocity using symphysis-fundal height and biometric ultrasound approximations. During labor, it interprets cardiotocography (CTG), applying pattern recognition (Dawes-Redman criteria) to classify fetal heart rate variability, accelerations, and decelerations.

It utilizes partogram curve models (e.g., modified WHO partograph) to track cervical dilation against expected temporal progression (Alert and Action lines), triggering oxytocin augmentation or obstetric referral protocols when labor dystocia is detected.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| ctg_trace | TimeSeries | Fetal heart rate and uterine contractions |
| partogram_data| CervicalExam | Dilation, effacement, station |
| maternal_vitals| Vitals | BP, HR, Temp |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| fetal_status | FetalState | Reassuring vs Non-reassuring |
| labor_progress| PartoStatus | Normal vs Dystocia |
| escalation_flag| boolean | True if obstetric intervention needed |

### State Schema
- `stage_of_labor`: Tracks progression (Latent, Active, Second, Third).
- `contraction_integral`: Total uterine work over time (Montevideo units).

## Dependencies

### Upstream (depends on)
- H11-ENDOCRINOLOGIA (gestational diabetes tracking)

### Downstream (feeds into)
- H11-OBSTETRICA (if surgical/medical escalation required)
- H11-PEDIATRIA (neonatal handoff)

## Failure Modes
- Misinterpreting early decelerations (benign head compression) as late decelerations (placental insufficiency).
- Failure to recognize insidious onset of preeclampsia from subtle blood pressure trending.

## Performance Characteristics
Real-time streaming required for CTG analysis. Critical low latency (<1s) for detecting prolonged fetal bradycardia.

## Research References
- Dawes-Redman Criteria for CTG analysis.
- WHO Partograph Guidelines.

## Implementation Notes
Implement strict alerting for "Action Line" crossings on the partogram, representing a rigid 4-hour delay behind physiological dilation rates.
