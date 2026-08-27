import json
import math
import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum

class VaccinePlatform(Enum):
    MRNA = "mRNA"
    VIRAL_VECTOR = "viral_vector"
    SUBUNIT = "subunit"
    LIVE_ATTENUATED = "live_attenuated"
    INACTIVATED = "inactivated"

class AdjuvantType(Enum):
    ALUM = "Alum"
    MF59 = "MF59"
    AS01 = "AS01"
    AS03 = "AS03"
    CPG_1018 = "CpG_1018"
    NONE = "None"

@dataclass
class PathogenProfile:
    name: str
    r0_value: float
    mutation_rate: float
    primary_antigen: str
    cellular_entry_receptor: str

@dataclass
class Formulation:
    platform: VaccinePlatform
    adjuvant: AdjuvantType
    storage_temp_celsius: float
    lipid_nanoparticle_used: bool

@dataclass
class VaccineCandidate:
    candidate_id: str
    formulation: Formulation
    predicted_efficacy: float
    immunogenicity_score: float
    safety_profile_score: float

class ImmunogenicityPredictor:
    """Predicts T-cell and B-cell responses based on antigen and platform."""
    
    def predict_score(self, pathogen: PathogenProfile, platform: VaccinePlatform, adjuvant: AdjuvantType) -> float:
        # Base score derived from pathogen mutation rate (higher mutation -> lower baseline efficacy)
        base = max(10.0, 80.0 - (pathogen.mutation_rate * 1000))
        
        # Platform modifiers
        if platform == VaccinePlatform.MRNA:
            base += 15.0
        elif platform == VaccinePlatform.LIVE_ATTENUATED:
            base += 20.0
        elif platform == VaccinePlatform.SUBUNIT:
            base -= 5.0
            
        # Adjuvant modifiers (crucial for subunit)
        if platform == VaccinePlatform.SUBUNIT and adjuvant != AdjuvantType.NONE:
            base += 15.0
        elif platform == VaccinePlatform.MRNA and adjuvant != AdjuvantType.NONE:
            # mRNA typically uses LNP, not traditional adjuvants; penalize mismatch
            base -= 10.0
            
        # Add stochastic noise for biological variance
        noise = random.uniform(-5.0, 5.0)
        return min(100.0, max(0.0, base + noise))

class EpidemiologicalSimulator:
    """Simulates population dynamics to determine herd immunity thresholds."""
    
    def calculate_hit(self, r0: float, vaccine_efficacy: float) -> float:
        """
        Calculate Herd Immunity Threshold.
        Formula: HIT = (1 - 1/R0) / Vaccine_Efficacy
        """
        if r0 <= 1.0:
            return 0.0
        if vaccine_efficacy <= 0.0:
            return 1.0 # Impossible to reach
            
        hit = (1 - (1 / r0)) / vaccine_efficacy
        return min(1.0, max(0.0, hit))

class H11VaccinologiaAgent:
    """
    Core agent for H11-VACCINOLOGIA.
    Manages the pipeline from pathogen analysis to vaccine candidate generation and population modeling.
    """
    
    def __init__(self):
        self.immuno_predictor = ImmunogenicityPredictor()
        self.epi_simulator = EpidemiologicalSimulator()
        self.candidate_counter = 0
        self.memory_bank: List[VaccineCandidate] = []

    def _generate_candidate_id(self) -> str:
        self.candidate_counter += 1
        return f"VAC-{self.candidate_counter:04d}"

    def evaluate_platform_suitability(self, pathogen: PathogenProfile) -> List[Tuple[VaccinePlatform, float]]:
        """Scores platforms based on pathogen characteristics."""
        scores = {}
        
        # Fast mutating pathogens favor adaptable platforms
        if pathogen.mutation_rate > 0.01:
            scores[VaccinePlatform.MRNA] = 0.9
            scores[VaccinePlatform.VIRAL_VECTOR] = 0.7
            scores[VaccinePlatform.LIVE_ATTENUATED] = 0.3
        else:
            scores[VaccinePlatform.LIVE_ATTENUATED] = 0.85
            scores[VaccinePlatform.SUBUNIT] = 0.8
            scores[VaccinePlatform.MRNA] = 0.75
            
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)

    def design_vaccine(self, pathogen: PathogenProfile, target_efficacy: float = 0.85) -> VaccineCandidate:
        """Designs an optimal vaccine candidate for the given pathogen."""
        platforms_ranked = self.evaluate_platform_suitability(pathogen)
        best_platform = platforms_ranked[0][0]
        
        # Determine formulation specifics
        adjuvant = AdjuvantType.NONE
        lnp_used = False
        storage_temp = 2.0 # standard fridge temp by default
        
        if best_platform == VaccinePlatform.MRNA:
            lnp_used = True
            storage_temp = -70.0 # Ultra-cold chain requirement
        elif best_platform == VaccinePlatform.SUBUNIT:
            # Need an adjuvant for strong response
            adjuvant = AdjuvantType.AS01
            
        formulation = Formulation(
            platform=best_platform,
            adjuvant=adjuvant,
            storage_temp_celsius=storage_temp,
            lipid_nanoparticle_used=lnp_used
        )
        
        immuno_score = self.immuno_predictor.predict_score(pathogen, best_platform, adjuvant)
        predicted_efficacy = immuno_score / 100.0 * 0.95 # Mapping score to efficacy
        
        safety = 95.0
        if best_platform == VaccinePlatform.LIVE_ATTENUATED:
            safety -= 15.0 # Higher risk of reversion
            
        candidate = VaccineCandidate(
            candidate_id=self._generate_candidate_id(),
            formulation=formulation,
            predicted_efficacy=predicted_efficacy,
            immunogenicity_score=immuno_score,
            safety_profile_score=safety
        )
        
        self.memory_bank.append(candidate)
        return candidate

    def run_pipeline(self, pathogen_data: Dict) -> Dict:
        """Main entry point for external interaction."""
        pathogen = PathogenProfile(
            name=pathogen_data.get("name", "Unknown Pathogen"),
            r0_value=float(pathogen_data.get("r0", 2.5)),
            mutation_rate=float(pathogen_data.get("mutation_rate", 0.001)),
            primary_antigen=pathogen_data.get("antigen", "Spike"),
            cellular_entry_receptor=pathogen_data.get("receptor", "ACE2")
        )
        
        candidate = self.design_vaccine(pathogen)
        hit = self.epi_simulator.calculate_hit(pathogen.r0_value, candidate.predicted_efficacy)
        
        return {
            "candidate_id": candidate.candidate_id,
            "platform": candidate.formulation.platform.value,
            "adjuvant": candidate.formulation.adjuvant.value,
            "storage_requirement": f"{candidate.formulation.storage_temp_celsius}C",
            "predicted_efficacy": candidate.predicted_efficacy,
            "immunogenicity_score": candidate.immunogenicity_score,
            "herd_immunity_threshold_pct": round(hit * 100, 2),
            "safety_score": candidate.safety_profile_score
        }

if __name__ == "__main__":
    agent = H11VaccinologiaAgent()
    sample_pathogen = {
        "name": "SARS-CoV-2 Variant",
        "r0": 5.5,
        "mutation_rate": 0.015,
        "antigen": "S-protein",
        "receptor": "ACE2"
    }
    result = agent.run_pipeline(sample_pathogen)
    print(json.dumps(result, indent=2))
