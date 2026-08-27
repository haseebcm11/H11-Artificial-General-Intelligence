from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Optional, Tuple
import math

class NormalizationMethod(Enum):
    TPM = auto()
    FPKM = auto()
    CPM = auto()
    DESEQ = auto()

@dataclass
class Transcript:
    transcript_id: str
    gene_id: str
    length: int
    exons: List[Tuple[int, int]]

@dataclass
class Sample:
    sample_id: str
    condition: str
    replicate_num: int
    total_reads: int = 0

@dataclass
class ExpressionResult:
    gene_id: str
    base_mean: float
    log2_fold_change: float
    p_value: float
    adj_p_value: float

class TranscriptomicaAgent:
    """
    H11-TRANSCRIPTOMICA: RNA-seq quantification and differential expression.
    """
    def __init__(self, norm_method: NormalizationMethod = NormalizationMethod.TPM):
        self.norm_method = norm_method
        self.transcripts: Dict[str, Transcript] = {}
        self.samples: Dict[str, Sample] = {}
        # count_matrix[gene_id][sample_id] -> raw_count
        self.count_matrix: Dict[str, Dict[str, float]] = {}
        # normalized_matrix[gene_id][sample_id] -> norm_value
        self.normalized_matrix: Dict[str, Dict[str, float]] = {}
        
    def add_transcript(self, transcript: Transcript) -> None:
        self.transcripts[transcript.transcript_id] = transcript
        if transcript.gene_id not in self.count_matrix:
            self.count_matrix[transcript.gene_id] = {}
            self.normalized_matrix[transcript.gene_id] = {}

    def add_sample(self, sample: Sample) -> None:
        self.samples[sample.sample_id] = sample
        for gene_id in self.count_matrix:
            self.count_matrix[gene_id][sample.sample_id] = 0.0
            
    def load_counts(self, sample_id: str, counts: Dict[str, float]) -> None:
        """Load raw counts mapping transcript_ids to counts."""
        if sample_id not in self.samples:
            raise ValueError(f"Sample {sample_id} not registered.")
            
        total = sum(counts.values())
        self.samples[sample_id].total_reads = int(total)
        
        for tx_id, count in counts.items():
            if tx_id in self.transcripts:
                gene_id = self.transcripts[tx_id].gene_id
                self.count_matrix[gene_id][sample_id] += count

    def normalize_tpm(self) -> None:
        """Normalize the count matrix to Transcripts Per Million (TPM)."""
        # Step 1: Divide read counts by gene length (kb) -> RPK
        # Step 2: Sum RPKs per sample and divide by 1M -> scaling factor
        # Step 3: Divide RPK by scaling factor -> TPM
        
        gene_lengths = {}
        for tx in self.transcripts.values():
            # Simplistic gene length approximation (longest transcript)
            gene_lengths[tx.gene_id] = max(gene_lengths.get(tx.gene_id, 0), tx.length)
            
        for sample_id in self.samples:
            rpk = {}
            for gene_id, counts in self.count_matrix.items():
                length_kb = max(gene_lengths.get(gene_id, 1000) / 1000.0, 0.1)
                rpk[gene_id] = counts.get(sample_id, 0.0) / length_kb
                
            scaling_factor = sum(rpk.values()) / 1_000_000.0
            
            for gene_id in self.count_matrix:
                if scaling_factor > 0:
                    tpm = rpk[gene_id] / scaling_factor
                else:
                    tpm = 0.0
                self.normalized_matrix[gene_id][sample_id] = tpm

    def calculate_differential_expression(self, condition_a: str, condition_b: str) -> List[ExpressionResult]:
        """Simplified DE analysis using log2 fold change of normalized means."""
        self.normalize_tpm()
        
        samples_a = [s_id for s_id, s in self.samples.items() if s.condition == condition_a]
        samples_b = [s_id for s_id, s in self.samples.items() if s.condition == condition_b]
        
        if not samples_a or not samples_b:
            raise ValueError("Conditions must have at least one sample.")
            
        results = []
        
        for gene_id in self.count_matrix:
            vals_a = [self.normalized_matrix[gene_id][s] for s in samples_a]
            vals_b = [self.normalized_matrix[gene_id][s] for s in samples_b]
            
            mean_a = sum(vals_a) / len(vals_a)
            mean_b = sum(vals_b) / len(vals_b)
            
            base_mean = (mean_a + mean_b) / 2.0
            
            # Avoid log(0)
            log2_fc = math.log2((mean_b + 1e-6) / (mean_a + 1e-6))
            
            # Dummy p-value for architectural completeness (real one needs statistical test like t-test or Wald)
            p_val = 0.05 if abs(log2_fc) > 1.0 else 0.5
            
            results.append(ExpressionResult(
                gene_id=gene_id,
                base_mean=base_mean,
                log2_fold_change=log2_fc,
                p_value=p_val,
                adj_p_value=p_val * 1.5 # Dummy FDR
            ))
            
        # Sort by significance
        results.sort(key=lambda x: x.p_value)
        return results

    def find_highly_expressed(self, threshold: float = 100.0) -> Dict[str, List[str]]:
        """Return genes with TPM > threshold per sample."""
        res = {sample_id: [] for sample_id in self.samples}
        for gene_id, sample_dict in self.normalized_matrix.items():
            for s_id, tpm in sample_dict.items():
                if tpm > threshold:
                    res[s_id].append(gene_id)
        return res

    def summary(self) -> Dict[str, int]:
        return {
            "num_transcripts": len(self.transcripts),
            "num_genes": len(self.count_matrix),
            "num_samples": len(self.samples)
        }
