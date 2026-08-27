import json
import math
import random
from dataclasses import dataclass, field
from typing import List, Dict, Set
from enum import Enum

class AntiviralClass(Enum):
    NUCLEOSIDE_ANALOG = "Nucleoside_Analog"
    PROTEASE_INHIBITOR = "Protease_Inhibitor"
    INTEGRASE_INHIBITOR = "Integrase_Inhibitor"
    ENTRY_INHIBITOR = "Entry_Inhibitor"
    NNRTI = "Non_Nucleoside_Reverse_Transcriptase_Inhibitor"

class ViralFamily(Enum):
    CORONAVIRIDAE = "Coronaviridae"
    RETROVIRIDAE = "Retroviridae"
    FLAVIVIRIDAE = "Flaviviridae"
    ORTHOMYXOVIRIDAE = "Orthomyxoviridae"
    FILOVIRIDAE = "Filoviridae"

@dataclass
class ViralTarget:
    family: ViralFamily
    enzyme_name: str
    has_exonuclease_proofreading: bool
    active_site_conservation: float # 0.0 to 1.0
    current_mutations: List[str]

@dataclass
class AntiviralCompound:
    name: str
    drug_class: AntiviralClass
    smiles_proxy: str
    steric_hindrance_score: float # important for escaping exonuclease
    broad_spectrum_potential: float

class ViralTargetBinder:
    """Calculates theoretical IC50 binding affinities."""
    
    def calculate_ic50(self, compound: AntiviralCompound, target: ViralTarget) -> float:
        # Base IC50 in nanomolar (nM)
        base_ic50 = 50.0 
        
        # Modify based on active site conservation
        # Highly conserved sites are easier to design for reliably
        base_ic50 *= (2.0 - target.active_site_conservation)
        
        # Determine resistance penalty from mutations
        mutation_penalty = 1.0
        if compound.drug_class == AntiviralClass.NUCLEOSIDE_ANALOG:
            if "M184V" in target.current_mutations or "K65R" in target.current_mutations:
                mutation_penalty = 50.0
        elif compound.drug_class == AntiviralClass.PROTEASE_INHIBITOR:
            if "L90M" in target.current_mutations or "V82A" in target.current_mutations:
                mutation_penalty = 25.0
                
        final_ic50 = base_ic50 * mutation_penalty
        
        # Biological jitter
        return round(final_ic50 * random.uniform(0.9, 1.1), 2)

class ResistanceMutationAnalyzer:
    """Evaluates fold-change in resistance and proofreading evasion."""
    
    def evaluate_evasion(self, compound: AntiviralCompound, target: ViralTarget) -> float:
        if not target.has_exonuclease_proofreading:
            return 100.0 # No proofreading to evade
            
        if compound.drug_class != AntiviralClass.NUCLEOSIDE_ANALOG:
            return 100.0 # Only NRTIs/Nucs suffer from exonuclease excision
            
        # For Nucs, steric hindrance prevents excision (e.g., Remdesivir's 1'-CN group)
        evasion_score = min(100.0, compound.steric_hindrance_score * 10.0)
        return round(evasion_score, 2)

class ReadinessEvaluator:
    """Scores a compound for pandemic preparedness."""
    
    def score_readiness(self, compound: AntiviralCompound, ic50: float, evasion: float) -> float:
        # Lower IC50 is better
        potency_score = max(0.0, 100.0 - (math.log10(ic50 + 1) * 20.0))
        
        # Evasion is critical
        evasion_weight = evasion * 0.4
        
        # Broad spectrum is the most important for unknown pathogens
        spectrum_score = compound.broad_spectrum_potential * 100.0 * 0.4
        
        potency_weight = potency_score * 0.2
        
        total_score = evasion_weight + spectrum_score + potency_weight
        return round(min(100.0, max(0.0, total_score)), 2)

class H11AntiviralisAgent:
    """Core agent for H11-ANTIVIRALIS."""
    
    def __init__(self):
        self.binder = ViralTargetBinder()
        self.mutation_analyzer = ResistanceMutationAnalyzer()
        self.readiness_eval = ReadinessEvaluator()
        
    def analyze_compound(self, drug_data: Dict, virus_data: Dict) -> Dict:
        compound = AntiviralCompound(
            name=drug_data.get("name", "Experimental-DAA"),
            drug_class=AntiviralClass(drug_data.get("class", "Nucleoside_Analog")),
            smiles_proxy=drug_data.get("smiles", ""),
            steric_hindrance_score=float(drug_data.get("steric_score", 5.0)),
            broad_spectrum_potential=float(drug_data.get("broad_spectrum", 0.5))
        )
        
        target = ViralTarget(
            family=ViralFamily(virus_data.get("family", "Coronaviridae")),
            enzyme_name=virus_data.get("enzyme", "RdRp"),
            has_exonuclease_proofreading=bool(virus_data.get("has_exo", True)),
            active_site_conservation=float(virus_data.get("conservation", 0.8)),
            current_mutations=virus_data.get("mutations", [])
        )
        
        predicted_ic50 = self.binder.calculate_ic50(compound, target)
        wild_type_target = ViralTarget(target.family, target.enzyme_name, target.has_exonuclease_proofreading, target.active_site_conservation, [])
        wt_ic50 = self.binder.calculate_ic50(compound, wild_type_target)
        
        fold_change = round(predicted_ic50 / wt_ic50, 2) if wt_ic50 > 0 else 1.0
        
        exo_evasion = self.mutation_analyzer.evaluate_evasion(compound, target)
        pri = self.readiness_eval.score_readiness(compound, predicted_ic50, exo_evasion)
        
        return {
            "compound_name": compound.name,
            "target_enzyme": target.enzyme_name,
            "predicted_ic50_nm": predicted_ic50,
            "resistance_fold_change": fold_change,
            "exonuclease_evasion_score": exo_evasion,
            "pandemic_readiness_index": pri,
            "status": "APPROVED_FOR_FURTHER_SCREENING" if pri > 70.0 else "REQUIRE_STRUCTURAL_OPTIMIZATION"
        }

if __name__ == "__main__":
    agent = H11AntiviralisAgent()
    drug = {
        "name": "Remdesivir-Analog",
        "class": "Nucleoside_Analog",
        "steric_score": 8.5,
        "broad_spectrum": 0.75
    }
    virus = {
        "family": "Coronaviridae",
        "enzyme": "RdRp",
        "has_exo": True,
        "conservation": 0.9,
        "mutations": []
    }
    
    result = agent.analyze_compound(drug, virus)
    print(json.dumps(result, indent=2))
