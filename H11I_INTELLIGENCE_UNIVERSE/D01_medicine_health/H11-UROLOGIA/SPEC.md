> **Layer 1** · Medicine & Health Sciences · `H11-UROLOGIA`

## Purpose
The H11-UROLOGIA agent manages the modeling of the male and female urinary tracts, as well as the male reproductive system. It focuses on renal fluid dynamics (in conjunction with Nephrology), urodynamics of the bladder, prostate pathologies, and urolithiasis (kidney stone) precipitation kinetics.

## Technical Deep-Dive
Urodynamics are modeled using a compliant spherical reservoir model (Laplace's Law) coupled with urethral hydrodynamic resistance (modified Bernoulli equation for distensible tubes) to simulate micturition curves. 
Prostatic hyperplasia (BPH) is modeled spatially, assessing the impingement of transition zone volume on the prostatic urethra. 
Urolithiasis is simulated using chemical thermodynamic engines to track supersaturation of calcium oxalate, uric acid, and struvite based on urinary pH, volume, and solute concentrations.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `uroflowmetry` | `FlowCurve` | Flow rate over time during micturition. |
| `urinalysis` | `UrinalysisPanel` | Chemical and microscopic urine properties. |
| `prostate_volume` | `float` | Estimated volume in cc (from TRUS or MRI). |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `stone_risk_index` | `Dict[str, float]` | Supersaturation risks for various stone types. |
| `bladder_outlet_obstruction` | `float` | Probability/severity of BOO. |
| `bph_progression` | `float` | Projected growth rate of adenoma. |

### State Schema
Maintains `UrologicalState`, logging detrusor muscle tone, residual urine volumes, and cumulative solute loads.

## Dependencies
### Upstream (depends on)
- `H11-NEPHROLOGIA`: For GFR and primary urine composition.
- `H11-NEUROLOGIA`: For autonomic innervation of the detrusor and sphincter.

### Downstream (feeds into)
- `H11-INFECTIOLOGIA`: For UTI risk derived from urinary stasis.

## Failure Modes
- **Sphincter Dyssynergia Misclassification**: Confusing neurogenic sphincter spasm with mechanical prostatic obstruction.
- **Supersaturation Hallucination**: Incorrectly predicting stone formation due to ignoring urinary inhibitors like citrate.
- **Detrusor Fatigue Error**: Failing to model the myogenic failure of the bladder over years of high-pressure voiding.

## Performance Characteristics
Urodynamic flow curve fitting solves in ~20ms. Thermodynamic saturation modeling requires complex iterative root-finding, taking ~150ms per urine sample.

## Research References
1. Griffiths, D. J. (1980). Urodynamics: The mechanics and hydrodynamics of the lower urinary tract.
2. Finlayson, B. (1977). Calcium stones: some physical and clinical aspects.

## Implementation Notes
Implement the urinary stone saturation using a robust equilibrium solver (similar to EQUIL2 algorithms). Use non-linear least squares for fitting the flow curves to the urethral resistance model.
