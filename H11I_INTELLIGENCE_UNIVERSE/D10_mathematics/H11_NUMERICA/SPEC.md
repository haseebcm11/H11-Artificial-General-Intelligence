> **Layer 10** · Mathematics · `H11-NUMERICA`

## Purpose

The H11-NUMERICA agent is the heavy-lifting engine for computational linear algebra and numeric approximations. It processes massive dimensional systems that cannot be solved analytically. It provides the core matrix operations required for machine learning (via `H11-OPTIMIZATIO`) and physics simulations (via `H11-DIFFERENTIALIS`).

## Technical Deep-Dive

H11-NUMERICA implements highly optimized BLAS/LAPACK routines, targeting both dense and sparse representations. It computes Singular Value Decompositions (SVD), QR factorizations, and Cholesky decompositions for symmetric positive-definite matrices. 

For extremely large sparse systems, it utilizes iterative Krylov subspace methods such as Generalized Minimal Residual (GMRES) and Conjugate Gradient (CG), coupled with algebraic multigrid preconditioners to accelerate convergence. Floating-point error tracking and condition number estimation are built-in to guarantee numerical stability.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `matrix` | `List[List[float]]` | Dense or sparse representation |
| `vector` | `List[float]` | Rhs vector |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `eigen_spectrum` | `Dict` | Spectral decomposition |
| `solution_vector` | `List[float]` | Solved states |

### State Schema
`factorization_cache`: Preserves computationally expensive LU or Cholesky factors when solving multiple systems with the same operator matrix.

## Dependencies

### Upstream (depends on)
- `H11-ALGEBRA`: Field definitions for matrices over arbitrary rings.

### Downstream (feeds into)
- `H11-OPTIMIZATIO`: Provides Hessians and gradient inverses.
- `H11-DIFFERENTIALIS`: Solves implicit step matrices.

## Failure Modes
- Catastrophic cancellation in ill-conditioned matrices.
- Non-convergence of iterative solvers (GMRES stalling) due to poor preconditioning.

## Performance Characteristics
Extreme memory bandwidth requirements. Matrix multiplications and factorizations are strictly offloaded to GPU tensor cores or AVX-512 vector units.

## Research References
- Golub, G. H., & Van Loan, C. F. (1996). Matrix Computations.
- Saad, Y., & Schultz, M. H. (1986). GMRES: A generalized minimal residual algorithm for solving nonsymmetric linear systems.

## Implementation Notes
Memory alignment is critical. Sparse matrices must use Compressed Sparse Row (CSR) format for efficient matrix-vector products.
