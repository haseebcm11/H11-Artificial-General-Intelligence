> **Layer 1** · Medicine & Health Sciences · `H11-NUCLEARIS-MED`

## Purpose
The H11-NUCLEARIS-MED agent handles the unique physics and kinetics of unsealed radioactive sources used for diagnostics (e.g., PET, SPECT) and targeted radiotherapy (e.g., Lu-177 dotatate, I-131). It tracks radiotracer distribution, calculates absolute standardized uptake values, and predicts tissue-level radiation damage.

## Technical Deep-Dive
Radiotracer behavior is modeled using both physical decay physics ($A(t) = A_0 e^{-\lambda t}$) and biological clearance. To assess true tissue avidity, it calculates the Standardized Uptake Value (SUV), normalizing scanner counts by injected activity and patient distribution volume (using body weight, lean body mass, or body surface area).
For radiotherapeutics, it implements the Medical Internal Radiation Dose (MIRD) formalism. It converts time-activity curves (TACs) from sequential scans into cumulated activity ($\tilde{A}$), then applies target-source S-values to calculate absorbed dose in Gy to both tumors and critical organs-at-risk (like bone marrow or kidneys).

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `isotope` | `str` | e.g., 'F-18', 'Ga-68', 'Lu-177' |
| `injected_activity_MBq` | `float` | MegaBecquerels at calibration time |
| `roi_activity_conc` | `float` | kBq/mL measured in tissue ROI |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `suv_metrics` | `Dict[str, float]` | SUVmax, SUVmean, SUVpeak |
| `dosimetry` | `Dict[str, float]` | Absorbed dose in Gray (Gy) per organ |

### State Schema
Tracks the biological half-lives and physical decay constants for various active tracers in a specific patient over time.

## Dependencies
### Upstream (depends on)
* H11-RADIOLOGIA: Provides the raw segmentation masks (ROIs) from PET/CT data.
### Downstream (feeds into)
* H11-ONCOLOGIA: Tumor SUV changes dictate oncologic treatment response (RECIST/PERCIST criteria).

## Failure Modes
1. **Extravasation Ignorance:** Assuming all injected activity entered the systemic pool when a large portion remained in the injection arm, skewing all SUV calculations downward.
2. **Clock Desynchronization:** A few minutes offset between the injection clock and the scanner clock drastically alters decay corrections for short-lived isotopes (e.g., O-15, half-life 2 mins).
3. **Partial Volume Effect:** Underestimating the activity of very small lymph nodes due to spatial resolution limits of the PET scanner, leading to underdosing in theranostics.

## Performance Characteristics
Computationally lightweight compared to raw image processing. Requires extreme precision (floating point 64) for exponential decay calculations over multiple half-lives.

## Research References
1. Loevinger, R., et al. (1991). "MIRD Primer for Absorbed Dose Calculations." *Society of Nuclear Medicine*.
2. Boellaard, R. (2009). "Standards for PET image acquisition and quantitative data analysis." *Journal of Nuclear Medicine*.

## Implementation Notes
Implement multiple S-value matrices for different patient phantom sizes (adult male, adult female, pediatric) to ensure accurate dosimetry.
