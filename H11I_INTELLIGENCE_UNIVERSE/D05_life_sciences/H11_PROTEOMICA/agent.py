from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Optional, Set, Tuple
import math

class AminoAcid(Enum):
    ALA = 'A'; CYS = 'C'; ASP = 'D'; GLU = 'E'; PHE = 'F'
    GLY = 'G'; HIS = 'H'; ILE = 'I'; LYS = 'K'; LEU = 'L'
    MET = 'M'; ASN = 'N'; PRO = 'P'; GLN = 'Q'; ARG = 'R'
    SER = 'S'; THR = 'T'; VAL = 'V'; TRP = 'W'; TYR = 'Y'

@dataclass
class AtomCoordinate:
    element: str
    x: float
    y: float
    z: float
    b_factor: float = 0.0

@dataclass
class ProteinStructure:
    protein_id: str
    sequence: str
    coordinates: List[AtomCoordinate] = field(default_factory=list)
    secondary_structures: List[str] = field(default_factory=list) # e.g., 'H' for helix, 'E' for sheet

@dataclass
class MassSpectrum:
    scan_id: str
    precursor_mz: float
    charge: int
    peaks: List[Tuple[float, float]] # mz, intensity

@dataclass
class PeptideSpectralMatch:
    scan_id: str
    peptide_sequence: str
    protein_id: str
    score: float
    e_value: float

class ProteomicaAgent:
    """
    H11-PROTEOMICA: Protein structure analysis and mass spectrometry interpreter.
    """
    def __init__(self, ms_tolerance: float = 0.02):
        self.ms_tolerance = ms_tolerance
        self.proteome_db: Dict[str, str] = {}
        self.structures: Dict[str, ProteinStructure] = {}
        self.psms: List[PeptideSpectralMatch] = []
        
        # Monoisotopic masses
        self.aa_masses = {
            'A': 71.03711, 'C': 103.00919, 'D': 115.02694, 'E': 129.04259,
            'F': 147.06841, 'G': 57.02146, 'H': 137.05891, 'I': 113.08406,
            'K': 128.09496, 'L': 113.08406, 'M': 131.04049, 'N': 114.04293,
            'P': 97.05276, 'Q': 128.05858, 'R': 156.10111, 'S': 87.03203,
            'T': 101.04768, 'V': 99.06841, 'W': 186.07931, 'Y': 163.06333
        }
        self.mass_H2O = 18.01056
        self.mass_proton = 1.00728

    def load_protein_sequence(self, protein_id: str, sequence: str) -> None:
        self.proteome_db[protein_id] = sequence.upper()

    def digest_trypsin(self, sequence: str, missed_cleavages: int = 1) -> List[str]:
        """In-silico digestion using Trypsin (cleaves after K/R except before P)."""
        peptides = []
        cuts = [0]
        for i in range(len(sequence) - 1):
            if sequence[i] in ['K', 'R'] and sequence[i+1] != 'P':
                cuts.append(i + 1)
        cuts.append(len(sequence))
        
        for i in range(len(cuts) - 1):
            peptides.append(sequence[cuts[i]:cuts[i+1]])
            
        # Add missed cleavages
        if missed_cleavages > 0:
            for i in range(len(cuts) - 2):
                peptides.append(sequence[cuts[i]:cuts[i+2]])
                
        return [p for p in peptides if len(p) >= 6] # Filter short peptides

    def calculate_peptide_mass(self, peptide: str) -> float:
        """Calculate uncharged monoisotopic mass of a peptide."""
        mass = self.mass_H2O
        for aa in peptide:
            mass += self.aa_masses.get(aa, 0.0)
        return mass

    def search_spectrum(self, spectrum: MassSpectrum) -> Optional[PeptideSpectralMatch]:
        """Naive MS/MS search matching precursor mass to theoretical peptides."""
        precursor_mass = (spectrum.precursor_mz * spectrum.charge) - (self.mass_proton * spectrum.charge)
        
        best_peptide = None
        best_protein = None
        min_error = float('inf')
        
        for prot_id, seq in self.proteome_db.items():
            peptides = self.digest_trypsin(seq)
            for pep in peptides:
                theo_mass = self.calculate_peptide_mass(pep)
                mass_error_da = abs(theo_mass - precursor_mass)
                
                if mass_error_da < self.ms_tolerance and mass_error_da < min_error:
                    min_error = mass_error_da
                    best_peptide = pep
                    best_protein = prot_id
                    
        if best_peptide:
            score = 1.0 / (min_error + 0.001) # Simple score
            psm = PeptideSpectralMatch(
                scan_id=spectrum.scan_id,
                peptide_sequence=best_peptide,
                protein_id=best_protein,
                score=score,
                e_value=min_error
            )
            self.psms.append(psm)
            return psm
            
        return None

    def calculate_distance(self, atom1: AtomCoordinate, atom2: AtomCoordinate) -> float:
        """Calculate Euclidean distance between two atoms."""
        dx = atom1.x - atom2.x
        dy = atom1.y - atom2.y
        dz = atom1.z - atom2.z
        return math.sqrt(dx*dx + dy*dy + dz*dz)

    def detect_clashes(self, structure_id: str, threshold: float = 1.5) -> int:
        """Detect steric clashes in a 3D protein structure."""
        if structure_id not in self.structures:
            return 0
            
        coords = self.structures[structure_id].coordinates
        clashes = 0
        
        for i in range(len(coords)):
            for j in range(i + 2, len(coords)): # Skip adjacent bonded atoms roughly
                dist = self.calculate_distance(coords[i], coords[j])
                if dist < threshold:
                    clashes += 1
                    
        return clashes
        
    def summary(self) -> Dict[str, int]:
        return {
            "proteins_in_db": len(self.proteome_db),
            "structures_loaded": len(self.structures),
            "spectral_matches": len(self.psms)
        }
