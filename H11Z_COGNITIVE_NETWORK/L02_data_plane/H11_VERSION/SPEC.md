> **Layer 2** · Data Plane & Ingestion · `H11-VERSION`

## Purpose

The H11-VERSION agent introduces Git-like version control semantics to massive, multi-terabyte ML datasets. Since duplicating terabytes of data for every minor change (e.g., correcting a label, removing a poisoned document) is financially and computationally prohibitive, this agent implements delta storage, deduplication, and snapshotting.

It ensures that any specific training run can be perfectly reproduced by pinning it to a specific dataset version hash, completely independent of subsequent mutations to the underlying data lake.

## Technical Deep-Dive

H11-VERSION relies on Merkle trees and content-addressable storage (CAS). Datasets are divided into chunks or shards. Each chunk is hashed, and these hashes form the leaves of a Merkle tree. A dataset version is simply the root hash of this tree. 

When a dataset is mutated (e.g., via decontamination by H11-CURATOR), H11-VERSION computes the delta. It only physically stores the modified chunks, while unmodified chunks are simply referenced by their existing hash. This provides O(1) branching and highly efficient storage.

The agent implements an API similar to Data Version Control (DVC) or Iceberg, supporting operations like `commit`, `checkout`, and `diff`. It also maintains schema evolution metadata, ensuring that changes to dataset columns (e.g., adding a "language_score" column) remain backward compatible.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `target_dataset_uri` | `str` | Pointer to the current state of the dataset files. |
| `commit_message` | `str` | Description of the changes made. |
| `parent_hash` | `Optional[str]` | The previous version hash to diff against. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `version_hash` | `str` | The immutable Merkle root of the new snapshot. |
| `delta_manifest` | `DeltaManifest` | List of added, removed, and modified chunks. |

### State Schema
- `merkle_trees`: In-memory caching of dataset directory structures.
- `commit_log`: Linear (or branched) history of commits per dataset.
- `cas_index`: Mapping of chunk hashes to physical storage locations.

## Dependencies

### Upstream (depends on)
- `H11-CURATOR`: Creates new iterations of datasets.
- `H11-CORPUS`: Mutates raw corpus data requiring versioning.

### Downstream (feeds into)
- `H11-SHARDER`: Requests a specific version hash to partition for training.

## Failure Modes
- **Dangling References**: If physical CAS chunks are garbage-collected prematurely, version checkouts will fail.
- **Hash Collision**: Extremely rare, but catastrophic failure if two different chunks produce the same SHA-256 hash.
- **Delta Bloat**: If data is appended randomly rather than sequentially, delta compression efficiency plummets.

## Performance Characteristics
- **Compute**: High I/O and CPU for chunking and hashing large files.
- **Storage**: Highly optimized; minimizes duplication across versions.
- **Latency**: Committing a 1TB dataset delta takes ~minutes depending on file layout and I/O.

## Research References
- "DVC: Data Version Control - Git for Data & Models"
- "Apache Iceberg: A Table Format for Huge Analytic Datasets"
- Merkle, "A Digital Signature Based on a Conventional Encryption Function"

## Implementation Notes
Implement chunking using Rabin fingerprinting (Content-Defined Chunking) to ensure that inserting a few bytes at the beginning of a file doesn't shift and invalidate all subsequent chunk hashes.
