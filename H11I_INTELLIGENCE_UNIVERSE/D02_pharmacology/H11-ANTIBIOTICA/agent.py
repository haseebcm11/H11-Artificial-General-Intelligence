import json
import random
import math
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

class AntibioticClass(Enum):
    BETA_LACTAM = "Beta-Lactam"
    FLUOROQUINOLONE = "Fluoroquinolone"
    MACROLIDE = "Macrolide"
    AMINOGLYCOSIDE = "Aminoglycoside"
    GLYCOPEPTIDE = "Glycopeptide"
    TETRACYCLINE = "Tetracycline"

class GramStain(Enum):
    POSITIVE = "Gram-Positive"
    NEGATIVE = "Gram-Negative"
    ATYPICAL = "Atypical"

@dataclass
class BacterialStrain:
    species: str
    gram_stain: GramStain
    resistance_genes: List[str]
    baseline_mutation_rate: float

@dataclass
class AntibioticCompound:
    name: str
    drug_class: AntibioticClass
    molecular_weight: float
    lipophilicity_logp: float
    protein_binding_pct: float

class ResistanceMechanismAnalyzer:
    """Analyzes genes to determine active resistance pathways."""
    
    def analyze_genes(self, strain: BacterialStrain, compound: AntibioticCompound) -> float:
        """Returns a resistance multiplier (1.0 = baseline, higher = resistant)."""
        multiplier = 1.0
        
        if compound.drug_class == AntibioticClass.BETA_LACTAM:
            if "blaTEM" in strain.resistance_genes or "blaCTX-M" in strain.resistance_genes:
                multiplier *= 50.0 # ESBL production
            if "mecA" in strain.resistance_genes:
                multiplier *= 100.0 # MRSA mechanism
                
        if compound.drug_class == AntibioticClass.GLYCOPEPTIDE:
            if "vanA" in strain.resistance_genes or "vanB" in strain.resistance_genes:
                multiplier *= 120.0 # VRE mechanism
                
        if compound.drug_class == AntibioticClass.FLUOROQUINOLONE:
            if "gyrA" in strain.resistance_genes or "parC" in strain.resistance_genes:
                multiplier *= 30.0 # Target modification
                
        # Gram negative general efflux/porin barrier for large molecules
        if strain.gram_stain == GramStain.NEGATIVE and compound.molecular_weight > 600:
            multiplier *= 20.0
            
        return multiplier

class QSARMicEngine:
    """Quantitative Structure-Activity Relationship MIC Engine."""
    
    def __init__(self):
        self.resistance_analyzer = ResistanceMechanismAnalyzer()
        
    def predict_mic(self, compound: AntibioticCompound, strain: BacterialStrain) -> float:
        """Predicts the Minimum Inhibitory Concentration (MIC) in mcg/mL."""
        # Base MIC calculation using dummy QSAR logic based on drug class and logP
        base_mic = 1.0
        
        if strain.gram_stain == GramStain.NEGATIVE:
            if compound.drug_class in [AntibioticClass.MACROLIDE, AntibioticClass.GLYCOPEPTIDE]:
                base_mic = 64.0 # Inherent resistance due to outer membrane
            else:
                base_mic = 2.0 - (compound.lipophilicity_logp * 0.2)
        else:
            base_mic = 0.5 + (abs(compound.lipophilicity_logp - 2.0) * 0.1)
            
        base_mic = max(0.01, base_mic)
        
        # Apply specific resistance mechanisms
        res_multiplier = self.resistance_analyzer.analyze_genes(strain, compound)
        
        final_mic = base_mic * res_multiplier
        
        # Add slight biological variance
        variance = random.uniform(0.8, 1.2)
        return round(final_mic * variance, 3)

class StewardshipOptimizer:
    """Generates antimicrobial stewardship recommendations."""
    
    def generate_recommendation(self, compound: AntibioticCompound, mic: float, strain: BacterialStrain) -> Dict[str, str]:
        clinical_breakpoint = 8.0 # Simplified universal breakpoint
        
        susceptibility = "Susceptible"
        if mic > clinical_breakpoint:
            susceptibility = "Resistant"
        elif mic > (clinical_breakpoint / 2):
            susceptibility = "Intermediate"
            
        pk_pd_target = "Time > MIC (T>MIC)" # Default for Beta-Lactams
        if compound.drug_class in [AntibioticClass.FLUOROQUINOLONE, AntibioticClass.AMINOGLYCOSIDE]:
            pk_pd_target = "Peak/MIC ratio or AUC/MIC"
            
        stewardship_note = "Standard dosing recommended."
        if susceptibility == "Resistant":
            stewardship_note = "DO NOT PRESCRIBE. Escalate to alternative class or combination therapy. Consider ID consult."
        elif compound.drug_class == AntibioticClass.FLUOROQUINOLONE:
            stewardship_note = "Reserve for severe infections due to collateral damage (C. diff risk, tendonopathy)."
            
        return {
            "interpretation": susceptibility,
            "pk_pd_target": pk_pd_target,
            "guideline": stewardship_note
        }

class H11AntibioticaAgent:
    """Core agent for H11-ANTIBIOTICA."""
    
    def __init__(self):
        self.mic_engine = QSARMicEngine()
        self.stewardship = StewardshipOptimizer()
        
    def evaluate_treatment(self, drug_data: Dict, pathogen_data: Dict) -> Dict:
        compound = AntibioticCompound(
            name=drug_data.get("name", "UnknownDrug"),
            drug_class=AntibioticClass(drug_data.get("class", "Beta-Lactam")),
            molecular_weight=float(drug_data.get("mw", 400.0)),
            lipophilicity_logp=float(drug_data.get("logp", 1.5)),
            protein_binding_pct=float(drug_data.get("protein_binding", 50.0))
        )
        
        strain = BacterialStrain(
            species=pathogen_data.get("species", "E. coli"),
            gram_stain=GramStain(pathogen_data.get("gram", "Gram-Negative")),
            resistance_genes=pathogen_data.get("genes", []),
            baseline_mutation_rate=float(pathogen_data.get("mutation_rate", 1e-7))
        )
        
        predicted_mic = self.mic_engine.predict_mic(compound, strain)
        recommendations = self.stewardship.generate_recommendation(compound, predicted_mic, strain)
        
        return {
            "antibiotic": compound.name,
            "pathogen": strain.species,
            "predicted_mic_mcg_ml": predicted_mic,
            "clinical_interpretation": recommendations["interpretation"],
            "pk_pd_optimization": recommendations["pk_pd_target"],
            "stewardship_directive": recommendations["guideline"]
        }

if __name__ == "__main__":
    agent = H11AntibioticaAgent()
    drug = {
        "name": "Ceftriaxone",
        "class": "Beta-Lactam",
        "mw": 554.58,
        "logp": -1.7,
        "protein_binding": 90.0
    }
    bug = {
        "species": "Klebsiella pneumoniae",
        "gram": "Gram-Negative",
        "genes": ["blaCTX-M"], # ESBL producer
        "mutation_rate": 2.5e-7
    }
    
    report = agent.evaluate_treatment(drug, bug)
    print(json.dumps(report, indent=2))
