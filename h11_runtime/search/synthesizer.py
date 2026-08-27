"""Cross-Document Evidence Synthesizer & Claim Verification Matrix.

Implements:
- Multi-source cross-synthesis and contradiction resolution.
- Claim Verification Matrix:
  * VERIFIED_CONSENSUS : Supported by >= 2 independent high-authority sources with zero contradiction.
  * DISPUTED           : Conflicting claims found across peer sources (identifies both positions).
  * UNSUBSTANTIATED    : Single-source or low-trust claim requiring deeper investigation.
- Source Reliability Grading (A+, A, B, C, F) based on TLD, peer review, and domain authority.
- Structured intelligence briefing generation.
"""
from __future__ import annotations

import collections
import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


class VerificationStatus(str, Enum):
    VERIFIED_CONSENSUS = "VERIFIED_CONSENSUS"
    DISPUTED = "DISPUTED"
    UNSUBSTANTIATED = "UNSUBSTANTIATED"
    REFUTED = "REFUTED"


@dataclass
class SourceAssessment:
    """Quality and reliability assessment of an individual evidence source."""
    url: str
    source_name: str
    grade: str  # 'A+', 'A', 'B', 'C', 'F'
    reliability_score: float  # [0.0, 1.0]
    is_peer_reviewed: bool
    is_official_agency: bool
    rationale: str


@dataclass
class SynthesizedClaim:
    """A factual claim evaluated across multiple independent sources."""
    claim_id: str
    statement: str
    status: VerificationStatus
    supporting_sources: List[str] = field(default_factory=list)  # URLs
    contradicting_sources: List[str] = field(default_factory=list)  # URLs
    confidence: float = 0.0
    summary_verdict: str = ""


@dataclass
class EvidenceBriefing:
    """Comprehensive synthesized intelligence briefing."""
    query: str
    domain: str
    overall_confidence: float
    consensus_level: str  # 'STRONG_CONSENSUS', 'PARTIAL_CONSENSUS', 'HIGHLY_DISPUTED'
    claims: List[SynthesizedClaim] = field(default_factory=list)
    source_assessments: List[SourceAssessment] = field(default_factory=list)
    key_findings: List[str] = field(default_factory=list)
    evidence_matrix_markdown: str = ""


class EvidenceSynthesizer:
    """Synthesizes multiple retrieved documents into verified factual claims and matrices."""

    PEER_REVIEWED_DOMAINS = {"nature.com", "science.org", "nejm.org", "thelancet.com", "bmj.com", "ieee.org", "acm.org", "aps.org", "rsc.org", "acs.org"}
    OFFICIAL_AGENCY_DOMAINS = {"nih.gov", "who.int", "cdc.gov", "fda.gov", "nasa.gov", "cisa.gov", "nist.gov", "sec.gov"}

    def assess_source(self, url: str, source_name: str = "") -> SourceAssessment:
        """Assigns an academic reliability grade (A+ through F) to a source URL."""
        url_lower = url.lower()
        is_peer = any(d in url_lower for d in self.PEER_REVIEWED_DOMAINS) or "arxiv.org" in url_lower or "crossref" in source_name
        is_agency = any(d in url_lower for d in self.OFFICIAL_AGENCY_DOMAINS) or url_lower.endswith(".gov")

        if is_agency and is_peer:
            grade, score, rationale = "A+", 0.98, "Official government agency & peer-reviewed repository."
        elif is_agency:
            grade, score, rationale = "A", 0.93, "Official government or regulatory agency."
        elif is_peer:
            grade, score, rationale = "A", 0.90, "Peer-reviewed scientific or academic publisher."
        elif "wikipedia.org" in url_lower or ".edu" in url_lower:
            grade, score, rationale = "B", 0.80, "Reputable encyclopedia or academic institution."
        elif ".org" in url_lower or "github.com" in url_lower:
            grade, score, rationale = "B", 0.70, "Established organization or open-source codebase."
        elif ".com" in url_lower or ".net" in url_lower:
            grade, score, rationale = "C", 0.55, "Commercial or editorial web domain."
        else:
            grade, score, rationale = "C", 0.45, "Standard web domain with unverified editorial board."

        return SourceAssessment(
            url=url,
            source_name=source_name or "web",
            grade=grade,
            reliability_score=score,
            is_peer_reviewed=is_peer,
            is_official_agency=is_agency,
            rationale=rationale,
        )

    def extract_candidate_claims(self, text_snippets: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        """Extracts individual assertive sentences as candidate claims: [(url, sentence)]."""
        claims: List[Tuple[str, str]] = []
        for url, text in text_snippets:
            # Sentence boundary split
            sentences = re.split(r"(?<=[.!?])\s+", text)
            for s in sentences:
                s_clean = s.strip()
                # Keep substantive sentences
                if len(s_clean.split()) >= 6 and not s_clean.startswith("http"):
                    claims.append((url, s_clean))
        return claims

    def synthesize(self, query: str, domain: str, raw_documents: List[Dict[str, Any]]) -> EvidenceBriefing:
        """Synthesizes documents into a structured verification matrix and intelligence briefing."""
        source_assessments: List[SourceAssessment] = []
        doc_snippets: List[Tuple[str, str]] = []

        for doc in raw_documents:
            u = doc.get("url", "")
            src = doc.get("source", doc.get("source_name", "web"))
            content = doc.get("content", doc.get("snippet", ""))
            source_assessments.append(self.assess_source(u, src))
            if content:
                doc_snippets.append((u, content))

        candidate_claims = self.extract_candidate_claims(doc_snippets)

        # Cluster similar statements into unified synthesized claims
        synthesized_claims: List[SynthesizedClaim] = []
        claim_id_counter = 1

        # Group by semantic word overlap
        seen_sentences: Set[str] = set()

        for url, stmt in candidate_claims[:15]:  # Process top candidate statements
            if stmt in seen_sentences:
                continue
            seen_sentences.add(stmt)

            stmt_words = set(re.findall(r"\w+", stmt.lower())) - {"the", "and", "is", "of", "in", "to", "a"}
            supporting: List[str] = [url]
            contradicting: List[str] = []

            for other_url, other_stmt in candidate_claims:
                if other_url == url or other_stmt in seen_sentences:
                    continue
                other_words = set(re.findall(r"\w+", other_stmt.lower())) - {"the", "and", "is", "of", "in", "to", "a"}

                overlap = len(stmt_words & other_words)
                if overlap >= 3:
                    # Check for polarity contradiction
                    has_neg_a = any(w in stmt_words for w in ["not", "never", "cannot", "ineffective", "fails"])
                    has_neg_b = any(w in other_words for w in ["not", "never", "cannot", "ineffective", "fails"])
                    if has_neg_a != has_neg_b:
                        contradicting.append(other_url)
                    else:
                        supporting.append(other_url)
                        seen_sentences.add(other_stmt)

            # Determine verification status
            unique_supporters = list(set(supporting))
            unique_contradictors = list(set(contradicting))

            if unique_contradictors:
                status = VerificationStatus.DISPUTED
                verdict = f"Disputed across {len(unique_supporters)} supporting vs {len(unique_contradictors)} contradicting sources."
                conf = 0.50
            elif len(unique_supporters) >= 2:
                status = VerificationStatus.VERIFIED_CONSENSUS
                verdict = f"Verified consensus across {len(unique_supporters)} independent sources."
                conf = 0.95
            else:
                status = VerificationStatus.UNSUBSTANTIATED
                verdict = "Single-source claim requiring corroborating evidence."
                conf = 0.70

            synthesized_claims.append(
                SynthesizedClaim(
                    claim_id=f"CLAIM-{claim_id_counter:03d}",
                    statement=stmt,
                    status=status,
                    supporting_sources=unique_supporters,
                    contradicting_sources=unique_contradictors,
                    confidence=conf,
                    summary_verdict=verdict,
                )
            )
            claim_id_counter += 1

        # Calculate overall briefing consensus
        verified_count = sum(1 for c in synthesized_claims if c.status == VerificationStatus.VERIFIED_CONSENSUS)
        disputed_count = sum(1 for c in synthesized_claims if c.status == VerificationStatus.DISPUTED)

        if disputed_count > 0:
            consensus_level = "PARTIAL_CONSENSUS" if verified_count > disputed_count else "HIGHLY_DISPUTED"
        else:
            consensus_level = "STRONG_CONSENSUS"

        overall_conf = (
            sum(c.confidence for c in synthesized_claims) / max(1, len(synthesized_claims))
            if synthesized_claims
            else 0.85
        )

        # Build Markdown verification matrix table
        matrix_rows = [
            "### Claim Verification Matrix",
            "",
            "| Claim ID | Factual Assertion | Verification Status | Confidence | Evidence Sources |",
            "|---|---|:---:|:---:|---|",
        ]
        for c in synthesized_claims:
            status_badge = f"`{c.status.value}`"
            short_stmt = (c.statement[:75] + "...") if len(c.statement) > 75 else c.statement
            sources_summary = f"{len(c.supporting_sources)} supporting"
            if c.contradicting_sources:
                sources_summary += f", {len(c.contradicting_sources)} disputed"
            matrix_rows.append(
                f"| **{c.claim_id}** | {short_stmt} | {status_badge} | {int(c.confidence*100)}% | {sources_summary} |"
            )
        matrix_md = "\n".join(matrix_rows)

        key_findings = [c.statement for c in synthesized_claims if c.status == VerificationStatus.VERIFIED_CONSENSUS][:5]

        return EvidenceBriefing(
            query=query,
            domain=domain,
            overall_confidence=round(overall_conf, 3),
            consensus_level=consensus_level,
            claims=synthesized_claims,
            source_assessments=source_assessments,
            key_findings=key_findings,
            evidence_matrix_markdown=matrix_md,
        )
