"""Advanced Semantic, Scientific & Multi-Modal Document Extractor.

Extracts:
- LaTeX & ASCII Math equations ($...$, $$...$$, \\begin{equation}...\\end{equation})
- HTML Table structures converted to structured Markdown tables
- Programming code snippets with heuristic language classification
- Academic citations, DOIs, PubMed PMIDs, arXiv IDs, and ISBNs
- Temporal freshness & evergreen quality scoring
"""
from __future__ import annotations

import datetime
import html
import math
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class MathEquation:
    """Represents an extracted mathematical formula."""
    raw_expression: str
    is_block: bool
    domain_hint: Optional[str] = None  # e.g., 'D08_physics', 'D10_mathematics'


@dataclass
class StructuredTable:
    """Represents a structured table extracted from HTML or markdown."""
    headers: List[str]
    rows: List[List[str]]
    caption: str = ""
    markdown: str = ""


@dataclass
class CodeSnippet:
    """Represents an extracted source code snippet."""
    language: str
    code: str
    line_count: int


@dataclass
class AcademicCitation:
    """Represents an academic citation identifier found in the text."""
    citation_type: str  # 'DOI', 'ARXIV', 'PUBMED', 'ISBN'
    identifier: str
    raw_match: str


@dataclass
class SemanticDocument:
    """Rich semantic representation of a parsed web document."""
    url: str
    title: str
    clean_text: str
    equations: List[MathEquation] = field(default_factory=list)
    tables: List[StructuredTable] = field(default_factory=list)
    code_snippets: List[CodeSnippet] = field(default_factory=list)
    citations: List[AcademicCitation] = field(default_factory=list)
    freshness_score: float = 1.0  # [0.0, 1.0]
    is_evergreen: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


class SemanticParser:
    """Extracts scientific, code, mathematical, and tabular structures from documents."""

    # Regex patterns for academic identifiers
    DOI_PATTERN = re.compile(r"\b(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)\b")
    ARXIV_PATTERN = re.compile(r"\b(?:arXiv:\s*|arxiv\.org/abs/)(\d{4}\.\d{4,5}(?:v\d+)?)\b", re.IGNORECASE)
    PUBMED_PATTERN = re.compile(r"\b(?:PMID:\s*|pubmed\.ncbi\.nlm\.nih\.gov/)(\d{6,9})\b", re.IGNORECASE)
    ISBN_PATTERN = re.compile(r"\b(?:ISBN(?:-1[03])?:?\s*)?(?=[0-9X]{10}$|(?=(?:[0-9]+[-\s]){3})[-\s0-9X]{13}$|97[89][0-9]{10}$|(?=(?:[0-9]+[-\s]){4})[-\s0-9]{17}$)(?:97[89][-\s]?)?[0-9]{1,5}[-\s]?[0-9]+[-\s]?[0-9]+[-\s]?[0-9X]\b")

    # Math regex
    BLOCK_MATH = re.compile(r"(\$\$(?:\\.|[^\$])+\$\$|\\begin\{equation\}(?:\\.|[^\\])*?\\end\{equation\})", re.DOTALL)
    INLINE_MATH = re.compile(r"(\$(?:\\.|[^\$])+\$|\\\((?:\\.|[^\\])*?\\\))")

    # Table regex (HTML)
    TABLE_PATTERN = re.compile(r"<table[^>]*>(.*?)</table>", re.DOTALL | re.IGNORECASE)
    TR_PATTERN = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
    TH_PATTERN = re.compile(r"<th[^>]*>(.*?)</th>", re.DOTALL | re.IGNORECASE)
    TD_PATTERN = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL | re.IGNORECASE)

    # Code block regex
    PRE_CODE_PATTERN = re.compile(r"<pre(?: class=\"([^\"]*)\")?[^>]*><code[^>]*>(.*?)</code></pre>", re.DOTALL | re.IGNORECASE)
    FENCED_CODE_PATTERN = re.compile(r"```([a-zA-Z0-9_\-\+#]*)\n(.*?)```", re.DOTALL)

    def extract_equations(self, text: str) -> List[MathEquation]:
        """Extracts inline and block LaTeX/math expressions."""
        equations: List[MathEquation] = []
        # Extract block math
        for m in self.BLOCK_MATH.finditer(text):
            expr = m.group(1).strip()
            domain = self._classify_math_domain(expr)
            equations.append(MathEquation(raw_expression=expr, is_block=True, domain_hint=domain))

        # Extract inline math
        clean_text = self.BLOCK_MATH.sub("", text)
        for m in self.INLINE_MATH.finditer(clean_text):
            expr = m.group(1).strip()
            if len(expr) > 2:  # Avoid single $ signs
                domain = self._classify_math_domain(expr)
                equations.append(MathEquation(raw_expression=expr, is_block=False, domain_hint=domain))

        return equations

    def _classify_math_domain(self, expr: str) -> str:
        """Determines if equation is physical, chemical, or purely mathematical."""
        if any(sym in expr for sym in ["\\hbar", "\\psi", "\\nabla", "c^2", "dt", "\\partial"]):
            return "D08_physics"
        elif any(sym in expr for sym in ["\\rightarrow", "mol", "pH", "K_a", "K_d"]):
            return "D09_chemistry"
        elif any(sym in expr for sym in ["\\int", "\\sum", "\\prod", "\\in", "\\forall", "\\exists", "\\sigma"]):
            return "D10_mathematics"
        return "D10_mathematics"

    def extract_tables(self, html_text: str) -> List[StructuredTable]:
        """Converts HTML tables into structured schemas and Markdown strings."""
        tables: List[StructuredTable] = []
        for t_match in self.TABLE_PATTERN.finditer(html_text):
            t_content = t_match.group(1)
            rows: List[List[str]] = []
            headers: List[str] = []

            for tr in self.TR_PATTERN.finditer(t_content):
                r_content = tr.group(1)
                th_cells = [self._strip_html(c.group(1)).strip() for c in self.TH_PATTERN.finditer(r_content)]
                td_cells = [self._strip_html(c.group(1)).strip() for c in self.TD_PATTERN.finditer(r_content)]

                if th_cells and not headers:
                    headers = th_cells
                elif td_cells:
                    rows.append(td_cells)

            if not headers and rows:
                headers = [f"Col {i+1}" for i in range(len(rows[0]))]

            # Generate markdown table string
            md_lines = []
            if headers:
                md_lines.append("| " + " | ".join(headers) + " |")
                md_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
                for row in rows:
                    # Pad or truncate row to header length
                    padded = (row + [""] * len(headers))[: len(headers)]
                    md_lines.append("| " + " | ".join(padded) + " |")
            md_str = "\n".join(md_lines)

            if headers or rows:
                tables.append(StructuredTable(headers=headers, rows=rows, markdown=md_str))

        return tables

    def extract_code_snippets(self, raw_content: str) -> List[CodeSnippet]:
        """Extracts code snippets from HTML pre/code tags or Markdown fenced blocks."""
        snippets: List[CodeSnippet] = []

        # Check markdown fenced code
        for m in self.FENCED_CODE_PATTERN.finditer(raw_content):
            lang = m.group(1).lower().strip() or self._detect_language(m.group(2))
            code = m.group(2).strip()
            snippets.append(CodeSnippet(language=lang, code=code, line_count=len(code.splitlines())))

        # Check HTML pre/code
        for m in self.PRE_CODE_PATTERN.finditer(raw_content):
            class_hint = m.group(1) or ""
            raw_code = html.unescape(m.group(2))
            lang = self._extract_lang_from_class(class_hint) or self._detect_language(raw_code)
            snippets.append(CodeSnippet(language=lang, code=raw_code.strip(), line_count=len(raw_code.splitlines())))

        return snippets

    def _extract_lang_from_class(self, class_str: str) -> Optional[str]:
        m = re.search(r"language-([a-zA-Z0-9_\+#]+)", class_str)
        return m.group(1).lower() if m else None

    def _detect_language(self, code: str) -> str:
        """Heuristic programming language detector."""
        if re.search(r"\b(def |import |class |elif |self\.)\b", code):
            return "python"
        elif re.search(r"\b(#include|std::|int main|nullptr|cout)\b", code):
            return "cpp"
        elif re.search(r"\b(fn |let mut |impl |pub fn |match )\b", code):
            return "rust"
        elif re.search(r"\b(const |let |function|console\.log|=>)\b", code):
            return "javascript"
        elif re.search(r"\b(SELECT|FROM|WHERE|INSERT|UPDATE|JOIN)\b", code, re.IGNORECASE):
            return "sql"
        elif re.search(r"\b(__global__|__device__|cudaMalloc|blockIdx)\b", code):
            return "cuda"
        return "text"

    def extract_citations(self, text: str) -> List[AcademicCitation]:
        """Extracts DOIs, PMIDs, and arXiv references."""
        citations: List[AcademicCitation] = []
        for m in self.DOI_PATTERN.finditer(text):
            citations.append(AcademicCitation(citation_type="DOI", identifier=m.group(1), raw_match=m.group(0)))
        for m in self.ARXIV_PATTERN.finditer(text):
            citations.append(AcademicCitation(citation_type="ARXIV", identifier=m.group(1), raw_match=m.group(0)))
        for m in self.PUBMED_PATTERN.finditer(text):
            citations.append(AcademicCitation(citation_type="PUBMED", identifier=m.group(1), raw_match=m.group(0)))
        return citations

    def calculate_freshness(self, publish_date: Optional[datetime.datetime], is_scientific: bool = False) -> float:
        """Computes exponential half-life decay freshness score."""
        if not publish_date:
            return 0.8  # Default baseline when date unknown

        now = datetime.datetime.now(datetime.timezone.utc)
        if publish_date.tzinfo is None:
            publish_date = publish_date.replace(tzinfo=datetime.timezone.utc)

        age_days = max(0.0, (now - publish_date).total_seconds() / 86400.0)

        # Scientific papers decay slowly (half-life 5 years = 1825 days); News decays fast (half-life 30 days)
        half_life_days = 1825.0 if is_scientific else 30.0
        score = math.exp(-0.693 * (age_days / half_life_days))
        return max(0.1, min(1.0, score))

    def _strip_html(self, text: str) -> str:
        clean = re.sub(r"<[^>]+>", " ", text)
        return html.unescape(clean)

    def parse(self, raw_html_or_text: str, url: str = "", title: str = "", publish_date: Optional[datetime.datetime] = None) -> SemanticDocument:
        """Complete semantic parse pipeline."""
        clean = self._strip_html(raw_html_or_text)
        equations = self.extract_equations(raw_html_or_text)
        tables = self.extract_tables(raw_html_or_text)
        snippets = self.extract_code_snippets(raw_html_or_text)
        citations = self.extract_citations(raw_html_or_text)
        is_scientific = len(citations) > 0 or len(equations) > 0 or "doi.org" in url or "arxiv.org" in url
        freshness = self.calculate_freshness(publish_date, is_scientific=is_scientific)

        return SemanticDocument(
            url=url,
            title=title,
            clean_text=clean.strip(),
            equations=equations,
            tables=tables,
            code_snippets=snippets,
            citations=citations,
            freshness_score=freshness,
            is_evergreen=is_scientific,
        )
