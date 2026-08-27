"""
H11-ONCOLOGIA: Oncology & Cancer Biology
Layer 1 - Medicine & Health Sciences

Simulates cancer genomics, TNM 8th edition staging, Gompertzian tumor growth
kinetics under selective therapeutic pressure, RECIST 1.1 response evaluation,
clonal resistance trajectories, and Virtual Tumor Board multi-modality regimen stratification.
"""

from __future__ import annotations
import asyncio
import logging
import math
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

logger = logging.getLogger(__name__)


class CancerType(Enum):
    NSCLC = auto()
    SCLC = auto()
    BREAST = auto()
    COLORECTAL = auto()
    MELANOMA = auto()
    PANCREATIC = auto()
    PROSTATE = auto()
    GLIOBLASTOMA = auto()
    OVARIAN = auto()
    RENAL_CELL = auto()


class RECISTCategory(Enum):
    COMPLETE_RESPONSE = auto()
    PARTIAL_RESPONSE = auto()
    STABLE_DISEASE = auto()
    PROGRESSIVE_DISEASE = auto()
    NOT_EVALUABLE = auto()


class TherapyModality(Enum):
    TARGETED_THERAPY = auto()
    IMMUNOTHERAPY = auto()
    CHEMOTHERAPY = auto()
    RADIOTHERAPY = auto()
    SURGICAL_RESECTION = auto()
    COMBINATION = auto()


class ActionabilityTier(Enum):
    TIER_I_STRONG_EVIDENCE = auto()
    TIER_II_POTENTIAL_BENEFIT = auto()
    TIER_III_UNKNOWN_SIGNIFICANCE = auto()
    TIER_IV_BENIGN = auto()


class TreatmentIntent(Enum):
    CURATIVE = auto()
    NEOADJUVANT = auto()
    ADJUVANT = auto()
    DEFINITIVE = auto()
    PALLIATIVE = auto()
    MAINTENANCE = auto()


class OncologiaError(Exception):
    """Base exception for oncology domain agent operations."""


class InvalidStagingInputError(OncologiaError):
    """Raised when TNM parameters or biomarker combinations are invalid."""


class RECISTCalculationError(OncologiaError):
    """Raised when lesion measurements violate RECIST 1.1 constraints."""


class ClonalDynamicsSimulationError(OncologiaError):
    """Raised when clonal frequency calculations produce non-convergent states."""


@dataclass
class GenomicVariant:
    gene: str
    variant_syntax: str
    vaf: float
    tier: ActionabilityTier
    drug_sensitivities: List[str] = field(default_factory=list)
    resistance_signatures: List[str] = field(default_factory=list)


@dataclass
class TNMDescriptor:
    primary_site: CancerType
    t_stage: str
    n_stage: str
    m_stage: str
    histologic_grade: str = "G2"
    er_positive: Optional[bool] = None
    pr_positive: Optional[bool] = None
    her2_positive: Optional[bool] = None
    tmb_mut_per_mb: Optional[float] = None
    msi_high: Optional[bool] = None


@dataclass
class TNMStageResult:
    anatomical_stage: str
    prognostic_stage: str
    is_metastatic: bool
    risk_category: str


@dataclass
class LesionMeasurement:
    lesion_id: str
    anatomical_site: str
    longest_diameter_mm: float
    is_target: bool
    is_nodal: bool = False
    short_axis_mm: Optional[float] = None


@dataclass
class RECISTEvaluation:
    sum_longest_diameters_mm: float
    nadir_sum_mm: float
    pct_change_from_baseline: float
    pct_change_from_nadir: float
    category: RECISTCategory
    new_lesions_identified: bool


@dataclass
class ClonalSubpopulation:
    clone_id: str
    driver_mutations: List[str]
    current_vaf: float
    proliferation_rate: float
    drug_resistance_map: Dict[str, float] = field(default_factory=dict)


@dataclass
class TreatmentRegimen:
    regimen_id: str
    regimen_name: str
    modality: TherapyModality
    intent: TreatmentIntent
    drug_agents: List[str]
    evidence_tier: ActionabilityTier
    predicted_pfs_months: float
    predicted_orr: float
    rationale: str


@dataclass
class OncologyPatientState:
    patient_id: str
    cancer_type: CancerType
    staging: TNMStageResult
    baseline_sld_mm: float
    nadir_sld_mm: float
    current_line: int
    active_clones: List[ClonalSubpopulation] = field(default_factory=list)
    previous_regimens: List[TreatmentRegimen] = field(default_factory=list)


class GompertzianKineticsEngine:
    """Simulates tumor volume dynamics using Gompertzian kinetics and Norton-Simon cell kill."""
    def __init__(self, carrying_capacity_cm3: float = 500.0, alpha_growth: float = 0.045):
        self.carrying_capacity = carrying_capacity_cm3
        self.alpha_growth = alpha_growth

    def simulate_trajectory(self, initial_volume_cm3: float, days: int, drug_kill_rate: float, dt: float = 0.5) -> Tuple[np.ndarray, np.ndarray]:
        steps = int(days / dt)
        timeline = np.linspace(0, days, steps)
        volumes = np.zeros(steps)
        volumes[0] = max(1e-4, initial_volume_cm3)
        for i in range(1, steps):
            v_prev = volumes[i - 1]
            if v_prev <= 1e-4:
                volumes[i] = 0.0
                continue
            growth_term = self.alpha_growth * v_prev * math.log(max(1.001, self.carrying_capacity / v_prev))
            kill_term = drug_kill_rate * v_prev
            volumes[i] = max(0.0, v_prev + (growth_term - kill_term) * dt)
        return timeline, volumes


class TNMStagingEngine:
    """Calculates AJCC/UICC 8th Edition clinical and prognostic stage groupings."""
    @staticmethod
    def calculate_stage(desc: TNMDescriptor) -> TNMStageResult:
        t, n, m = desc.t_stage.upper(), desc.n_stage.upper(), desc.m_stage.upper()
        if m.startswith("M1"):
            return TNMStageResult("Stage IV", "Stage IVB" if "M1C" in m else "Stage IVA", True, "High")
        if t.startswith("T1") and n == "N0":
            stage, risk = "Stage IA", "Low"
        elif (t.startswith("T1") or t.startswith("T2")) and n == "N0":
            stage, risk = "Stage IB", "Low-Intermediate"
        elif (t.startswith("T1") or t.startswith("T2")) and n.startswith("N1"):
            stage, risk = "Stage IIA", "Intermediate"
        elif t.startswith("T3") and n == "N0":
            stage, risk = "Stage IIB", "Intermediate"
        elif (t.startswith("T3") or t.startswith("T4")) and (n.startswith("N1") or n.startswith("N2")):
            stage, risk = ("Stage IIIA" if n.startswith("N1") else "Stage IIIB"), "High"
        elif n.startswith("N3") or t.startswith("T4"):
            stage, risk = "Stage IIIC", "Very High"
        else:
            stage, risk = "Stage II", "Intermediate"

        prognostic_stage = stage
        if desc.primary_site == CancerType.BREAST:
            if desc.er_positive and desc.pr_positive and not desc.her2_positive:
                prognostic_stage = f"{stage} (Luminal A favorable)"
            elif not desc.er_positive and not desc.pr_positive and not desc.her2_positive:
                prognostic_stage, risk = f"{stage} (Triple-Negative aggressive)", "High"

        return TNMStageResult(stage, prognostic_stage, False, risk)


class OncologiaAgent:
    """Agent for oncology modeling, precision stratification, RECIST tracking, and tumor board synthesis."""
    def __init__(self, agent_id: str = "H11-ONCOLOGIA"):
        self.agent_id = agent_id
        self.patient_store: Dict[str, OncologyPatientState] = {}
        self.kinetics_engine = GompertzianKineticsEngine()
        self.staging_engine = TNMStagingEngine()

    async def stage_tumor(self, descriptor: TNMDescriptor) -> TNMStageResult:
        """Determines anatomical and prognostic stage under AJCC 8th Edition rules."""
        if not descriptor.t_stage or not descriptor.n_stage or not descriptor.m_stage:
            raise InvalidStagingInputError("T, N, and M parameters must all be populated.")
        return self.staging_engine.calculate_stage(descriptor)

    async def evaluate_recist_response(self, baseline_lesions: List[LesionMeasurement], current_lesions: List[LesionMeasurement], prior_nadir_sld: Optional[float] = None, has_new_lesions: bool = False) -> RECISTEvaluation:
        """Applies RECIST 1.1 quantitative criteria to target and non-target lesions."""
        target_baseline = [l for l in baseline_lesions if l.is_target]
        target_current = [l for l in current_lesions if l.is_target]
        if not target_baseline:
            raise RECISTCalculationError("At least one baseline target lesion is required.")
        base_sld = sum(l.longest_diameter_mm for l in target_baseline)
        curr_sld = sum(l.longest_diameter_mm for l in target_current)
        if base_sld <= 0:
            raise RECISTCalculationError("Baseline SLD must be strictly positive.")

        nadir_sld = min(base_sld, curr_sld) if prior_nadir_sld is None else min(prior_nadir_sld, curr_sld)
        pct_change_base = ((curr_sld - base_sld) / base_sld) * 100.0
        pct_change_nadir = ((curr_sld - nadir_sld) / nadir_sld * 100.0) if nadir_sld > 0 else 0.0

        if has_new_lesions or (pct_change_nadir >= 20.0 and (curr_sld - nadir_sld) >= 5.0):
            category = RECISTCategory.PROGRESSIVE_DISEASE
        elif curr_sld == 0.0:
            category = RECISTCategory.COMPLETE_RESPONSE
        elif pct_change_base <= -30.0:
            category = RECISTCategory.PARTIAL_RESPONSE
        else:
            category = RECISTCategory.STABLE_DISEASE

        return RECISTEvaluation(round(curr_sld, 2), round(nadir_sld, 2), round(pct_change_base, 2), round(pct_change_nadir, 2), category, has_new_lesions)

    async def simulate_tumor_growth_kinetics(self, initial_volume_cm3: float, days: int, therapy_kill_rate: float) -> Dict[str, Any]:
        """Integrates Gompertzian ODEs to project tumor volumetric burden under therapy."""
        timeline, trajectory = self.kinetics_engine.simulate_trajectory(initial_volume_cm3, days, therapy_kill_rate)
        return {
            "initial_volume_cm3": initial_volume_cm3,
            "terminal_volume_cm3": float(trajectory[-1]),
            "percent_volume_reduction": float((1.0 - trajectory[-1] / max(1e-4, initial_volume_cm3)) * 100.0),
            "trajectory_samples": [float(x) for x in trajectory[:: max(1, len(trajectory) // 10)]]
        }

    async def stratify_precision_regimens(self, cancer_type: CancerType, staging: TNMStageResult, variants: List[GenomicVariant], msi_high: bool = False, pd_l1_tps: float = 0.0) -> List[TreatmentRegimen]:
        """Generates evidence-ranked treatment regimens matching oncogenic drivers and biomarkers."""
        regimens: List[TreatmentRegimen] = []
        variant_genes = {v.gene.upper(): v for v in variants}

        if cancer_type == CancerType.NSCLC:
            if "EGFR" in variant_genes and "L858R" in variant_genes["EGFR"].variant_syntax:
                regimens.append(TreatmentRegimen("REG-EGFR-1L", "Osimertinib Monotherapy", TherapyModality.TARGETED_THERAPY, TreatmentIntent.DEFINITIVE if staging.is_metastatic else TreatmentIntent.ADJUVANT, ["Osimertinib"], ActionabilityTier.TIER_I_STRONG_EVIDENCE, 18.9, 0.80, "3rd generation EGFR TKI with CNS penetrance."))
            if "KRAS" in variant_genes and "G12C" in variant_genes["KRAS"].variant_syntax:
                regimens.append(TreatmentRegimen("REG-KRAS-G12C", "Sotorasib / Adagrasib", TherapyModality.TARGETED_THERAPY, TreatmentIntent.PALLIATIVE, ["Sotorasib"], ActionabilityTier.TIER_I_STRONG_EVIDENCE, 6.8, 0.37, "Direct covalent inhibitor targeting GDP-bound KRAS G12C."))
            if pd_l1_tps >= 50.0 and not ({"EGFR", "ALK"} & set(variant_genes.keys())):
                regimens.append(TreatmentRegimen("REG-IO-1L", "Pembrolizumab Monotherapy", TherapyModality.IMMUNOTHERAPY, TreatmentIntent.DEFINITIVE if staging.is_metastatic else TreatmentIntent.NEOADJUVANT, ["Pembrolizumab"], ActionabilityTier.TIER_I_STRONG_EVIDENCE, 10.3, 0.45, "Frontline checkpoint inhibition for PD-L1 TPS >= 50% without actionable driver."))

        if msi_high:
            regimens.append(TreatmentRegimen("REG-MSI-PAN-CANCER", "Pembrolizumab / Dostarlimab", TherapyModality.IMMUNOTHERAPY, TreatmentIntent.DEFINITIVE, ["Pembrolizumab"], ActionabilityTier.TIER_I_STRONG_EVIDENCE, 16.5, 0.40, "Tissue-agnostic approval for dMMR/MSI-H solid tumors."))

        if not regimens:
            regimens.append(TreatmentRegimen("REG-STD-CHEMO", "Platinum-Doublet Chemotherapy", TherapyModality.CHEMOTHERAPY, TreatmentIntent.PALLIATIVE if staging.is_metastatic else TreatmentIntent.CURATIVE, ["Carboplatin", "Paclitaxel"], ActionabilityTier.TIER_II_POTENTIAL_BENEFIT, 5.5, 0.28, "Standard cytoreductive backbone in absence of targetable driver."))

        return sorted(regimens, key=lambda r: (r.evidence_tier.value, -r.predicted_orr))

    async def model_clonal_evolution(self, initial_clones: List[ClonalSubpopulation], applied_drug: str, days: int) -> List[ClonalSubpopulation]:
        """Simulates subclonal selection dynamics and emergent resistance under drug pressure."""
        updated_clones: List[ClonalSubpopulation] = []
        for clone in initial_clones:
            resistance_factor = clone.drug_resistance_map.get(applied_drug, 0.0)
            effective_growth = clone.proliferation_rate * (1.0 - (1.0 - resistance_factor) * 0.8)
            new_vaf = min(1.0, max(0.001, clone.current_vaf * math.exp(effective_growth * (days / 30.0))))
            mutations = list(clone.driver_mutations)
            if resistance_factor > 0.6 and "RESISTANCE_GATE" not in mutations:
                mutations.append("RESISTANCE_GATE")
            updated_clones.append(ClonalSubpopulation(clone.clone_id, mutations, round(new_vaf, 4), clone.proliferation_rate, clone.drug_resistance_map))

        total_vaf = sum(c.current_vaf for c in updated_clones)
        if total_vaf > 1.0:
            for c in updated_clones:
                c.current_vaf = round(c.current_vaf / total_vaf, 4)
        return updated_clones

    async def calculate_synthetic_lethality_index(self, variants: List[GenomicVariant], msi_high: bool = False) -> Dict[str, Any]:
        """Evaluates DNA damage repair deficiencies and synthetic lethality vulnerabilities."""
        hrd_genes = {"BRCA1", "BRCA2", "PALB2", "ATM", "RAD51C", "BARD1"}
        detected_hrd = [v.gene for v in variants if v.gene.upper() in hrd_genes]
        has_hrd = len(detected_hrd) > 0
        return {
            "hrd_deficiency_detected": has_hrd,
            "hrd_mutations": detected_hrd,
            "parp_inhibitor_sensitivity": 0.88 if has_hrd else 0.05,
            "platinum_sensitivity_enhancement": 1.75 if has_hrd else 1.0,
            "msi_high_immune_vulnerability": 0.92 if msi_high else 0.15
        }

    async def register_patient(self, patient_id: str, cancer_type: CancerType, descriptor: TNMDescriptor, baseline_lesions: List[LesionMeasurement]) -> OncologyPatientState:
        """Initializes a new longitudinal oncology patient record."""
        staging = await self.stage_tumor(descriptor)
        base_sld = sum(l.longest_diameter_mm for l in baseline_lesions if l.is_target)
        state = OncologyPatientState(patient_id, cancer_type, staging, base_sld, base_sld, 1)
        self.patient_store[patient_id] = state
        return state

    async def conduct_virtual_tumor_board(self, patient_id: str, current_lesions: List[LesionMeasurement], variants: List[GenomicVariant], msi_high: bool = False, pd_l1_tps: float = 0.0) -> Dict[str, Any]:
        """Synthesizes staging, RECIST 1.1 dynamics, synthetic lethality, and precision regimens."""
        state = self.patient_store.get(patient_id)
        if not state:
            raise OncologiaError(f"Patient ID {patient_id} is not registered in state store.")

        recist = await self.evaluate_recist_response([LesionMeasurement("T1", "Primary", state.baseline_sld_mm, is_target=True)], current_lesions, state.nadir_sld_mm)
        state.nadir_sld_mm = recist.nadir_sum_mm

        regimens = await self.stratify_precision_regimens(state.cancer_type, state.staging, variants, msi_high, pd_l1_tps)
        synthetic_lethality = await self.calculate_synthetic_lethality_index(variants, msi_high)
        top_regimen = regimens[0] if regimens else None

        kinetics = await self.simulate_tumor_growth_kinetics(
            initial_volume_cm3=(recist.sum_longest_diameters_mm / 10.0) ** 3 * (math.pi / 6.0),
            days=90,
            therapy_kill_rate=0.08 if top_regimen and top_regimen.modality == TherapyModality.TARGETED_THERAPY else 0.04
        )

        return {
            "patient_id": patient_id,
            "cancer_type": state.cancer_type.name,
            "ajcc_stage": state.staging.anatomical_stage,
            "recist_status": recist.category.name,
            "sld_change_pct": recist.pct_change_from_baseline,
            "recommended_regimens": [{"regimen": r.regimen_name, "modality": r.modality.name, "tier": r.evidence_tier.name, "predicted_pfs": r.predicted_pfs_months, "rationale": r.rationale} for r in regimens],
            "synthetic_lethality": synthetic_lethality,
            "projected_90d_volume_cm3": kinetics["terminal_volume_cm3"]
        }

    async def get_patient_state(self, patient_id: str) -> Optional[OncologyPatientState]:
        """Retrieves patient state from the store."""
        return self.patient_store.get(patient_id)
