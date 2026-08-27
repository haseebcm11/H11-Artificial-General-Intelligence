import uuid
import math
import random
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from enum import Enum

class EconomicModelType(Enum):
    MARKOV_COHORT = "markov_cohort"
    DECISION_TREE = "decision_tree"
    MICROSIMULATION = "microsimulation"

@dataclass
class HealthState:
    state_id: str
    name: str
    utility_mean: float
    utility_std_err: float
    cost_multiplier: float = 1.0

@dataclass
class TransitionMatrix:
    # State ID to Dict of Destination State ID to Probability
    probabilities: Dict[str, Dict[str, float]]
    
    def validate(self) -> bool:
        for state, transitions in self.probabilities.items():
            total = sum(transitions.values())
            if not math.isclose(total, 1.0, rel_tol=1e-5):
                raise ValueError(f"Transition probabilities for state {state} sum to {total}, expected 1.0")
        return True

@dataclass
class Intervention:
    name: str
    base_cost_per_cycle: float
    transition_matrix: TransitionMatrix
    adverse_event_cost: float = 0.0
    adverse_event_prob: float = 0.0

@dataclass
class ModelParameters:
    time_horizon_cycles: int
    discount_rate_costs: float = 0.03
    discount_rate_outcomes: float = 0.03
    willingness_to_pay_threshold: float = 50000.0
    half_cycle_correction: bool = True

@dataclass
class SimulationResult:
    total_cost: float
    total_qalys: float
    life_years: float

@dataclass
class ICERResult:
    incremental_cost: float
    incremental_qalys: float
    icer: float
    is_cost_effective: bool
    net_monetary_benefit: float

class MarkovCohortModel:
    def __init__(
        self,
        states: List[HealthState],
        intervention: Intervention,
        comparator: Intervention,
        params: ModelParameters
    ):
        self.states = {s.state_id: s for s in states}
        self.intervention = intervention
        self.comparator = comparator
        self.params = params
        self.intervention.transition_matrix.validate()
        self.comparator.transition_matrix.validate()

    def _sample_utility(self, state: HealthState, is_deterministic: bool) -> float:
        if is_deterministic:
            return state.utility_mean
        val = random.gauss(state.utility_mean, state.utility_std_err)
        return max(0.0, min(1.0, val))

    def run_simulation(self, target: Intervention, is_deterministic: bool = True) -> SimulationResult:
        state_ids = list(self.states.keys())
        cohort = {sid: 0.0 for sid in state_ids}
        cohort[state_ids[0]] = 1.0
        
        total_cost = 0.0
        total_qalys = 0.0
        total_life_years = 0.0
        
        for cycle in range(self.params.time_horizon_cycles):
            cycle_cost = 0.0
            cycle_qalys = 0.0
            cycle_ly = 0.0
            
            for sid, proportion in cohort.items():
                if proportion <= 0.0:
                    continue
                state = self.states[sid]
                
                is_dead = 'dead' in state.name.lower()
                
                utility = self._sample_utility(state, is_deterministic)
                
                multiplier = 0.5 if (self.params.half_cycle_correction and (cycle == 0 or cycle == self.params.time_horizon_cycles - 1)) else 1.0
                
                state_cost = (target.base_cost_per_cycle * state.cost_multiplier)
                if random.random() < target.adverse_event_prob:
                    state_cost += target.adverse_event_cost
                
                discount_c = (1 + self.params.discount_rate_costs) ** cycle
                discount_o = (1 + self.params.discount_rate_outcomes) ** cycle
                
                cycle_cost += (proportion * state_cost * multiplier) / discount_c
                cycle_qalys += (proportion * utility * multiplier) / discount_o
                
                if not is_dead:
                    cycle_ly += proportion * multiplier
            
            total_cost += cycle_cost
            total_qalys += cycle_qalys
            total_life_years += cycle_ly
            
            next_cohort = {sid: 0.0 for sid in state_ids}
            for from_sid, proportion in cohort.items():
                if proportion > 0:
                    transitions = target.transition_matrix.probabilities.get(from_sid, {from_sid: 1.0})
                    for to_sid, prob in transitions.items():
                        next_cohort[to_sid] += proportion * prob
            cohort = next_cohort
            
        return SimulationResult(
            total_cost=total_cost,
            total_qalys=total_qalys,
            life_years=total_life_years
        )

    def calculate_icer(self, is_deterministic: bool = True) -> ICERResult:
        int_res = self.run_simulation(self.intervention, is_deterministic)
        comp_res = self.run_simulation(self.comparator, is_deterministic)
        
        inc_cost = int_res.total_cost - comp_res.total_cost
        inc_qalys = int_res.total_qalys - comp_res.total_qalys
        
        icer = inc_cost / inc_qalys if inc_qalys != 0 else float('inf')
        nmb = (inc_qalys * self.params.willingness_to_pay_threshold) - inc_cost
        is_ce = nmb > 0
        
        return ICERResult(
            incremental_cost=inc_cost,
            incremental_qalys=inc_qalys,
            icer=icer,
            is_cost_effective=is_ce,
            net_monetary_benefit=nmb
        )

class PharmacoeconomicAgent:
    """
    H11-PHARMACOECONOMIA
    Agent for health economics and outcomes research.
    """
    def __init__(self, wtp_threshold: float = 100000.0):
        self.wtp_threshold = wtp_threshold
        self.session_id = uuid.uuid4()
    
    def evaluate_intervention(
        self,
        intervention: Intervention,
        comparator: Intervention,
        states: List[HealthState],
        time_horizon: int = 50,
        psa_iterations: int = 1000
    ) -> Dict:
        params = ModelParameters(
            time_horizon_cycles=time_horizon,
            willingness_to_pay_threshold=self.wtp_threshold
        )
        model = MarkovCohortModel(states, intervention, comparator, params)
        
        base_case = model.calculate_icer(is_deterministic=True)
        
        ce_count = 0
        psa_icers = []
        for _ in range(psa_iterations):
            res = model.calculate_icer(is_deterministic=False)
            if res.is_cost_effective:
                ce_count += 1
            psa_icers.append(res.icer)
            
        prob_ce = ce_count / psa_iterations
        
        return {
            "session_id": str(self.session_id),
            "base_case_icer": base_case.icer,
            "base_case_nmb": base_case.net_monetary_benefit,
            "is_cost_effective_base": base_case.is_cost_effective,
            "psa_probability_cost_effective": prob_ce,
            "incremental_cost": base_case.incremental_cost,
            "incremental_qalys": base_case.incremental_qalys
        }

if __name__ == "__main__":
    agent = PharmacoeconomicAgent(wtp_threshold=50000.0)
    healthy = HealthState("H", "Healthy", 0.95, 0.02, 1.0)
    sick = HealthState("S", "Sick", 0.60, 0.05, 2.5)
    dead = HealthState("D", "Dead", 0.0, 0.0, 0.0)
    
    int_matrix = TransitionMatrix({
        "H": {"H": 0.8, "S": 0.15, "D": 0.05},
        "S": {"H": 0.2, "S": 0.6, "D": 0.2},
        "D": {"H": 0.0, "S": 0.0, "D": 1.0}
    })
    
    comp_matrix = TransitionMatrix({
        "H": {"H": 0.7, "S": 0.2, "D": 0.1},
        "S": {"H": 0.1, "S": 0.6, "D": 0.3},
        "D": {"H": 0.0, "S": 0.0, "D": 1.0}
    })
    
    new_drug = Intervention("NewDrug", 1500.0, int_matrix)
    std_care = Intervention("StdCare", 500.0, comp_matrix)
    
    result = agent.evaluate_intervention(new_drug, std_care, [healthy, sick, dead], time_horizon=20)
    print("Pharmacoeconomic Evaluation Result:")
    for k, v in result.items():
        print(f"  {k}: {v}")
