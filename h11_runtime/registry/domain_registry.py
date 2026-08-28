"""Domain Registry with Taxonomy and Ontology Mapping for All 30 H11I Domains."""
from __future__ import annotations

from typing import Dict, List, Optional, Set


class DomainRegistry:
    """Taxonomy and agent catalog of the 30 H11I intelligence domains (D01-D30)."""

    # Complete 30-Domain Ontology Catalog
    DOMAIN_CATALOG = {
        "D01": ("medicine_health", "Human Medicine, Clinical Diagnostics & Healthcare"),
        "D02": ("pharmacology", "Pharmacology, Drug Interaction & Pharmacokinetics"),
        "D03": ("dental", "Dentistry, Orthodontics & Oral Maxillofacial"),
        "D04": ("veterinary", "Veterinary Medicine & Comparative Physiology"),
        "D05": ("life_sciences", "Genetics, Molecular Biology & Ecology"),
        "D06": ("earth_environment", "Geophysics, Meteorology & Oceanography"),
        "D07": ("space_astronomy", "Astrophysics, Orbital Mechanics & Cosmology"),
        "D08": ("physics", "Quantum Physics, Relativity & Statistical Mechanics"),
        "D09": ("chemistry", "Organic, Inorganic & Physical Chemistry"),
        "D10": ("mathematics", "Topology, Abstract Algebra & Numerical Analysis"),
        "D11": ("computer_science", "Algorithms, Distributed Systems & AI/ML"),
        "D12": ("cybersecurity", "Cryptography, Threat Intelligence & Zero-Trust"),
        "D13": ("data_science", "Inferential Statistics, Causal Inference & Time-Series"),
        "D14": ("engineering", "Mechanical, Electrical, Structural & Materials Engineering"),
        "D15": ("architecture", "Structural Design, Spatial Geometry & Urban Systems"),
        "D16": ("transportation", "Autonomous Vehicles, Logistics & Aerospace Transport"),
        "D17": ("business_finance", "Quantitative Finance, Asset Pricing & Macroeconomics"),
        "D18": ("law_governance", "Jurisprudence, Regulatory Compliance & Constitutional Law"),
        "D19": ("arts_design", "Aesthetics, Visual Design & Human-Computer Ergonomics"),
        "D20": ("music_audio", "Acoustic Physics, Psychoacoustics & Signal Synthesis"),
        "D21": ("literature_linguistics", "Computational Linguistics, Semantics & Philology"),
        "D22": ("humanities_social", "Anthropology, Sociology, History & Philosophy"),
        "D23": ("allied_health", "Physical Therapy, Medical Imaging & Diagnostics"),
        "D24": ("agriculture_food", "Agronomy, Soil Chemistry & Crop Physiology"),
        "D25": ("energy_resources", "Thermodynamics, Nuclear Energy & Renewable Systems"),
        "D26": ("telecommunications", "Information Theory, RF Engineering & Optical Comms"),
        "D27": ("media_communication", "Media Dynamics, Information Dissemination & Rhetoric"),
        "D28": ("education", "Pedagogy, Cognitive Load Theory & Learning Systems"),
        "D29": ("sports_recreation", "Biomechanics, Exercise Physiology & Kinesiology"),
        "D30": ("specialized_niche", "Actuarial Science, Forensic Metrology & Micro-Domains"),
    }

    def __init__(self) -> None:
        self.domains: Dict[str, Set[str]] = {}
        # Pre-seed domain buckets
        for d_code in self.DOMAIN_CATALOG:
            self.domains[d_code] = set()

    def register_domain_agent(self, domain_code: str, agent_id: str) -> None:
        code_prefix = domain_code.split("_")[0].upper()
        if code_prefix in self.domains:
            self.domains[code_prefix].add(agent_id)
        else:
            self.domains.setdefault(domain_code, set()).add(agent_id)

    def list_domain_agents(self, domain_code: str) -> List[str]:
        code_prefix = domain_code.split("_")[0].upper()
        return sorted(list(self.domains.get(code_prefix, self.domains.get(domain_code, set()))))

    def get_domain_metadata(self, domain_code: str) -> Optional[tuple[str, str]]:
        code_prefix = domain_code.split("_")[0].upper()
        return self.DOMAIN_CATALOG.get(code_prefix)

    def get_all_domains(self) -> Dict[str, Dict[str, Any]]:
        return {
            code: {
                "name": name,
                "description": desc,
                "agent_count": len(self.domains.get(code, set())),
                "agents": sorted(list(self.domains.get(code, set()))),
            }
            for code, (name, desc) in self.DOMAIN_CATALOG.items()
        }
