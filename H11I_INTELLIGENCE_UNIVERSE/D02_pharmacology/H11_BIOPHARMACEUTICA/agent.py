import uuid
import re
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from enum import Enum
import math

class ExpressionSystem(Enum):
    CHO_CELLS = "CHO"
    E_COLI = "E. coli"
    YEAST = "P. pastoris"
    HEK293 = "HEK293"

class MoleculeType(Enum):
    MAB = "Monoclonal Antibody"
    FUSION = "Fusion Protein"
    ENZYME = "Recombinant Enzyme"

@dataclass
class BiologicMolecule:
    id: str
    name: str
    mol_type: MoleculeType
    sequence_heavy: str
    sequence_light: Optional[str] = None
    molecular_weight_kda: float = 150.0

@dataclass
class LiabilityReport:
    deamidation_sites: List[int]
    oxidation_sites: List[int]
    isomerization_sites: List[int]
    aggregation_score: float
    isoelectric_point: float

@dataclass
class UpstreamProcess:
    system: ExpressionSystem
    culture_volume_L: float
    seed_density: float
    run_time_days: int
    feed_strategy: str

@dataclass
class ProcessYield:
    titer_g_per_L: float
    total_yield_kg: float
    cell_viability_end: float

class ProteinAnalyzer:
    """Analyzes primary sequence for biophysical liabilities."""
    def __init__(self, molecule: BiologicMolecule):
        self.molecule = molecule
        self.seq = self.molecule.sequence_heavy + (self.molecule.sequence_light or "")
        
    def _find_motifs(self, pattern: str) -> List[int]:
        return [m.start() for m in re.finditer(pattern, self.seq)]
        
    def scan_liabilities(self) -> LiabilityReport:
        deamidation = self._find_motifs(r'N[GS]')
        oxidation = self._find_motifs(r'[MW]')
        isomerization = self._find_motifs(r'DG')
        
        hydrophobic_residues = sum(self.seq.count(aa) for aa in 'VILMFW')
        agg_score = hydrophobic_residues / len(self.seq) if self.seq else 0
        
        basic_count = sum(self.seq.count(aa) for aa in 'KRH')
        acidic_count = sum(self.seq.count(aa) for aa in 'DE')
        estimated_pi = 6.8 + (basic_count - acidic_count) * 0.05
        
        return LiabilityReport(
            deamidation_sites=deamidation,
            oxidation_sites=oxidation,
            isomerization_sites=isomerization,
            aggregation_score=round(agg_score, 3),
            isoelectric_point=round(estimated_pi, 2)
        )

class BioprocessSimulator:
    """Simulates upstream cell culture."""
    def __init__(self, process: UpstreamProcess):
        self.process = process
        
    def simulate_fed_batch(self, mol_type: MoleculeType) -> ProcessYield:
        mu_max = 0.6 if self.process.system == ExpressionSystem.CHO_CELLS else 1.2
        max_density = 20e6 if self.process.system == ExpressionSystem.CHO_CELLS else 50e6
        
        ivcd = (max_density * 0.7) * self.process.run_time_days
        
        if mol_type == MoleculeType.MAB:
            qp = 30.0 
        elif mol_type == MoleculeType.FUSION:
            qp = 15.0
        else:
            qp = 50.0
            
        titer_pg = qp * ivcd
        titer_g = titer_pg / 1e12
        
        if self.process.system == ExpressionSystem.E_COLI and mol_type == MoleculeType.MAB:
            titer_g *= 0.01
            
        total_kg = (titer_g * self.process.culture_volume_L) / 1000
        viability = max(0.4, 0.95 - (self.process.run_time_days * 0.02))
        
        return ProcessYield(
            titer_g_per_L=round(titer_g, 2),
            total_yield_kg=round(total_kg, 3),
            cell_viability_end=round(viability, 3)
        )

class BiopharmaceuticaAgent:
    """
    H11-BIOPHARMACEUTICA
    Agent for large-molecule drug discovery and bioprocessing.
    """
    def __init__(self):
        self.agent_id = uuid.uuid4()
        
    def analyze_molecule(self, molecule: BiologicMolecule) -> Dict:
        analyzer = ProteinAnalyzer(molecule)
        liabilities = analyzer.scan_liabilities()
        
        return {
            "molecule_name": molecule.name,
            "molecular_weight": molecule.molecular_weight_kda,
            "isoelectric_point": liabilities.isoelectric_point,
            "liability_counts": {
                "deamidation": len(liabilities.deamidation_sites),
                "oxidation": len(liabilities.oxidation_sites),
                "isomerization": len(liabilities.isomerization_sites)
            },
            "aggregation_propensity": liabilities.aggregation_score
        }
        
    def simulate_production(self, molecule: BiologicMolecule, process: UpstreamProcess) -> ProcessYield:
        sim = BioprocessSimulator(process)
        return sim.simulate_fed_batch(molecule.mol_type)

if __name__ == "__main__":
    agent = BiopharmaceuticaAgent()
    mab = BiologicMolecule(
        id="MAB-001",
        name="Trastuzumab_Sim",
        mol_type=MoleculeType.MAB,
        sequence_heavy="EVQLVESGGGLVQPGGSLRLSCAASGFNIKDTYIHWVRQAPGKGLEWVARIYPTNGYTRYADSVKGRFTISADTSKNTAYLQMNSLRAEDTAVYYCSRWGGDGFYAMDYWGQGTLVTVSS",
        sequence_light="DIQMTQSPSSLSASVGDRVTITCRASQDVNTAVAWYQQKPGKAPKLLIYSASFLYSGVPSRFSGSRSGTDFTLTISSLQPEDFATYYCQQHYTTPPTFGQGTKVEIK"
    )
    
    analysis = agent.analyze_molecule(mab)
    print("Molecule Analysis:", analysis)
    
    process = UpstreamProcess(
        system=ExpressionSystem.CHO_CELLS,
        culture_volume_L=2000.0,
        seed_density=0.5e6,
        run_time_days=14,
        feed_strategy="Daily starting day 3"
    )
            
    sim = BioprocessSimulator(process)
    prod = sim.simulate_fed_batch(mab.mol_type)
    print("Production Simulation:", prod)
