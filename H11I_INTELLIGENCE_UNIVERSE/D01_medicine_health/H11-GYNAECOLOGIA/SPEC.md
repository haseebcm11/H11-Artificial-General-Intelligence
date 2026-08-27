> **Layer 1** · Medicine & Health Sciences · `H11-GYNAECOLOGIA`

## Purpose
The H11-GYNAECOLOGIA agent provides cognitive models for the female reproductive system. It orchestrates the complex hormonal feedback loops of the menstrual cycle, evaluates reproductive tract pathology (e.g., endometriosis, fibroids, PCOS), and manages oncological screening for gynecologic cancers.

## Technical Deep-Dive
The menstrual cycle is simulated using a coupled set of nonlinear ordinary differential equations (ODEs) modeling the HPO (Hypothalamic-Pituitary-Ovarian) axis, tracking GnRH, FSH, LH, Estradiol, and Progesterone. The endometrium is modeled as a cellular automaton that proliferates, secretes, and undergoes apoptosis based on the receptor-mediated hormonal signals.

For endometriosis and fibroids, the agent utilizes a vascular-angiogenic growth model driven by local estrogen dominance and inflammatory cytokine gradients. PCOS is modeled via an androgen-insulin resistance cross-talk pathway.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `hormone_panel` | `EndocrineProfile` | Serum levels of reproductive hormones. |
| `pelvic_ultrasound` | `ImagingFeatures` | Structural data of uterus and ovaries. |
| `symptom_log` | `CycleTracking` | Patient-reported bleeding and pain metrics. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `cycle_phase` | `str` | Computed current phase (e.g., Late Follicular). |
| `ovulation_probability` | `float` | Likelihood of ovulation within 48h. |
| `pathology_risk` | `Dict[str, float]` | Probability array for PCOS, Endometriosis, etc. |

### State Schema
Maintains `ReproductiveState`, holding the state variables of the HPO axis ODEs, endometrial thickness, and follicular cohort size.

## Dependencies
### Upstream (depends on)
- `H11-ENDOCRINOLOGIA`: For thyroid and adrenal axes.
- `H11-RADIOLOGIA`: For raw ultrasound feature extraction.

### Downstream (feeds into)
- `H11-OBSTETRICIA`: Hands off state upon confirmation of pregnancy.
- `H11-ONCOLOGIA`: For cervical/ovarian malignancy tracking.

## Failure Modes
- **Oscillator Death**: The ODE solver for the HPO axis reaches a fixed point artificially, halting the simulated menstrual cycle.
- **Anovulatory Misclassification**: Failing to distinguish between PCOS-induced anovulation and perimenopausal transition due to overlap in FSH/LH ratios.
- **Ectopic Silence**: Missing the hemodynamic markers of an ectopic pregnancy in early stages.

## Performance Characteristics
ODE simulation of a 28-day cycle runs in ~10ms using a standard Runge-Kutta 4th order solver. Angiogenic growth models run offline (~500ms).

## Research References
1. Smith, H. O., et al. (2010). Mathematical modeling of the human menstrual cycle.
2. Taylor, H. S., et al. (2021). Endometriosis is a chronic systemic disease.

## Implementation Notes
The HPO axis equations are stiff; use an implicit solver like Radau or BDF if step-size issues arise.
