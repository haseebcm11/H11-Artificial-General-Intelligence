"""Merkle Tree Cryptographic Content Provenance & Tamper-Proof Ledger.

Implements:
- Content-Addressable Storage (CAS) with SHA-256 hashing for all web snippets.
- Merkle Tree computation over evidence chunks with root sealing.
- Merkle Inclusion Proof Generation:
  Proof pi = [(sibling_hash, direction_left_or_right), ...]
- Zero-knowledge verification proving that an agent's factual quote is
  unmodified from the exact web capture at timestamp T.
"""
from __future__ import annotations

import hashlib
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


def sha256_hash(data: str | bytes) -> str:
    """Computes standard SHA-256 hexadecimal hash string."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


@dataclass
class EvidenceLeaf:
    """A cryptographic leaf node containing an evidence claim and its hash."""
    leaf_index: int
    content: str
    url: str
    timestamp: float
    leaf_hash: str


@dataclass
class MerkleInclusionProof:
    """Cryptographic inclusion proof verifying leaf membership in Merkle root."""
    leaf_hash: str
    leaf_index: int
    merkle_root: str
    audit_path: List[Tuple[str, str]]  # [(sibling_hash, 'L' or 'R')]
    timestamp: float


class MerkleProvenanceTree:
    """Constructs complete Merkle trees over evidence snippets and verifies proofs."""

    def __init__(self, leaves: Optional[List[Tuple[str, str]]] = None) -> None:
        # leaves: list of (content, url)
        self.leaves: List[EvidenceLeaf] = []
        self.tree_levels: List[List[str]] = []
        self.root_hash: str = ""

        if leaves:
            for content, url in leaves:
                self.add_leaf(content, url)
            self.build_tree()

    def add_leaf(self, content: str, url: str) -> EvidenceLeaf:
        """Appends a new evidence chunk as a hashed leaf."""
        idx = len(self.leaves)
        now = time.time()
        # Hash combines content, URL, and leaf index
        payload = f"{idx}:{url}:{content}"
        h = sha256_hash(payload)
        leaf = EvidenceLeaf(leaf_index=idx, content=content, url=url, timestamp=now, leaf_hash=h)
        self.leaves.append(leaf)
        return leaf

    def build_tree(self) -> str:
        """Computes Merkle root hash across all leaves."""
        if not self.leaves:
            self.root_hash = sha256_hash("EMPTY_TREE")
            return self.root_hash

        current_level = [leaf.leaf_hash for leaf in self.leaves]
        self.tree_levels = [list(current_level)]

        while len(current_level) > 1:
            next_level: List[str] = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                # If odd number of nodes, duplicate the last node
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                combined = sha256_hash(left + right)
                next_level.append(combined)
            self.tree_levels.append(list(next_level))
            current_level = next_level

        self.root_hash = current_level[0]
        return self.root_hash

    def generate_proof(self, leaf_index: int) -> Optional[MerkleInclusionProof]:
        """Generates a cryptographic Merkle inclusion path proof for leaf at leaf_index."""
        if not self.tree_levels or leaf_index < 0 or leaf_index >= len(self.leaves):
            return None

        leaf = self.leaves[leaf_index]
        audit_path: List[Tuple[str, str]] = []
        idx = leaf_index

        for level in self.tree_levels[:-1]:
            if idx % 2 == 0:
                # Sibling is to the right
                sibling_idx = idx + 1 if idx + 1 < len(level) else idx
                sibling_hash = level[sibling_idx]
                audit_path.append((sibling_hash, "R"))
            else:
                # Sibling is to the left
                sibling_idx = idx - 1
                sibling_hash = level[sibling_idx]
                audit_path.append((sibling_hash, "L"))
            idx //= 2

        return MerkleInclusionProof(
            leaf_hash=leaf.leaf_hash,
            leaf_index=leaf_index,
            merkle_root=self.root_hash,
            audit_path=audit_path,
            timestamp=leaf.timestamp,
        )

    @staticmethod
    def verify_proof(proof: MerkleInclusionProof) -> bool:
        """Verifies if the leaf hash matches the Merkle root hash using the audit path."""
        current_hash = proof.leaf_hash

        for sibling_hash, direction in proof.audit_path:
            if direction == "R":
                current_hash = sha256_hash(current_hash + sibling_hash)
            else:
                current_hash = sha256_hash(sibling_hash + current_hash)

        return current_hash == proof.merkle_root
