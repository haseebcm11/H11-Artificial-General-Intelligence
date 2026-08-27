import math
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

@dataclass
class PKParameters:
    volume_of_distribution: float  # Vd in L
    clearance: float               # Cl in L/hr
    absorption_rate: float         # ka in 1/hr
    bioavailability: float         # F (0 to 1)
    
@dataclass
class DosingRegimen:
    route: str                     # "IV" or "PO"
    dose_mg: float
    interval_hr: float = 0.0       # 0 means single dose
    num_doses: int = 1

class PKODESolver:
    """Numerical solver for compartmental models using RK4."""
    
    def __init__(self, step_size: float = 0.1):
        self.dt = step_size
        
    def rk4_step(self, t: float, y: List[float], f: callable) -> List[float]:
        k1 = f(t, y)
        k2 = f(t + self.dt/2, [y[i] + self.dt/2 * k1[i] for i in range(len(y))])
        k3 = f(t + self.dt/2, [y[i] + self.dt/2 * k2[i] for i in range(len(y))])
        k4 = f(t + self.dt, [y[i] + self.dt * k3[i] for i in range(len(y))])
        
        return [y[i] + (self.dt/6.0) * (k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) for i in range(len(y))]

class PharmacokineticsAgent:
    def __init__(self):
        self.solver = PKODESolver(step_size=0.1)
        
    def simulate_1compartment(self, params: PKParameters, regimen: DosingRegimen, sim_hours: float) -> Dict:
        """
        Simulates a 1-compartment model with first order absorption and elimination.
        State vector y:
        y[0] = Amount of drug at absorption site (GI tract)
        y[1] = Amount of drug in central compartment (Plasma)
        """
        elimination_rate = params.clearance / params.volume_of_distribution # ke
        
        def derivatives(t, y):
            dy = [0.0, 0.0]
            # y[0] is GI depot, y[1] is Plasma
            absorption = params.absorption_rate * y[0]
            elimination = elimination_rate * y[1]
            
            dy[0] = -absorption
            dy[1] = absorption - elimination
            return dy

        times = []
        plasma_concentrations = []
        
        y = [0.0, 0.0]
        current_dose = 0
        next_dose_time = 0.0
        
        t = 0.0
        while t <= sim_hours:
            # Check for dosing event
            if current_dose < regimen.num_doses and t >= next_dose_time:
                if regimen.route == "PO":
                    y[0] += regimen.dose_mg * params.bioavailability
                elif regimen.route == "IV":
                    y[1] += regimen.dose_mg # IV assumes 100% F, directly into central comp
                
                current_dose += 1
                next_dose_time += regimen.interval_hr if regimen.interval_hr > 0 else float('inf')
                
            times.append(t)
            plasma_concentrations.append(y[1] / params.volume_of_distribution)
            
            y = self.solver.rk4_step(t, y, derivatives)
            t += self.solver.dt
            
        return self._calculate_metrics(times, plasma_concentrations, elimination_rate)
        
    def _calculate_metrics(self, times: List[float], concs: List[float], ke: float) -> Dict:
        cmax = max(concs)
        tmax = times[concs.index(cmax)]
        half_life = 0.693 / ke if ke > 0 else float('inf')
        
        # Calculate AUC using trapezoidal rule
        auc = 0.0
        for i in range(1, len(times)):
            dt = times[i] - times[i-1]
            auc += (concs[i] + concs[i-1]) / 2.0 * dt
            
        return {
            "Cmax_mg_L": round(cmax, 4),
            "Tmax_hr": round(tmax, 2),
            "Half_life_hr": round(half_life, 2),
            "AUC_hr_mg_L": round(auc, 4),
            "times": [round(t, 2) for t in times[::10]], # downsample for output
            "concentrations": [round(c, 4) for c in concs[::10]]
        }

if __name__ == "__main__":
    agent = PharmacokineticsAgent()
    params = PKParameters(volume_of_distribution=50.0, clearance=5.0, absorption_rate=1.2, bioavailability=0.8)
    regimen = DosingRegimen(route="PO", dose_mg=500.0, interval_hr=12.0, num_doses=3)
    
    results = agent.simulate_1compartment(params, regimen, sim_hours=48.0)
    print(f"Cmax: {results['Cmax_mg_L']}, Tmax: {results['Tmax_hr']}, AUC: {results['AUC_hr_mg_L']}")
