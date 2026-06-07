# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Research codebase for the PRX paper "Harmonic morphisms and dynamical invariants in network renormalization" (Guadagnuolo, Nurisso, Galluzzi, Allard, Petri). Manuscript source: `docs/main_prx_edited.tex`.

The paper proves that **discrete harmonic morphisms** (surjective maps preserving harmonic functions, equivalent to horizontally conformal maps by Urakawa's theorem) are the minimal condition under which random walks on a fine-grained network project exactly onto random walks on a coarse-grained image (Theorem 2: Random Walk Preservation). The code:

1. Implements the **harmonic degree** diagnostic (H_mean, H_mod, H_Dev) and conformal degree analogs to quantify how closely any coarse-graining approximates a harmonic morphism
2. Applies this to three renormalization methods (Geometric, Laplacian, GNN-based) across ~50 real networks, revealing distinct **dynamical fingerprints** (S-curve, high-low-high, uniformly low)
3. Discovers that Laplacian renormalization spontaneously yields **exact harmonic morphisms** in some networks (Facebook, Web-edu, CS Collab, Yeast)
4. Extends harmonic degree to **higher-order structures** (simplicial complexes) via Hodge Laplacian renormalization

Contact: francesco.guadagnuolo@epfl.ch

## Dependencies

A root `requirements.txt` pins the core dependencies (`networkx`, `numpy`, `scipy`, `matplotlib`, `pandas`, `jupyter`, `pytest`); heavier optional dependencies are commented out there. Full breakdown by use case:

- **Core**: `networkx`, `numpy`, `scipy`, `matplotlib`, `pandas`, `pickle`
- **GNN notebooks** (Euroroad_results, GNN_partition_function): `torch`, `torch_geometric`, `tqdm`
- **Clustering/SBM notebooks**: `graph_tool` (used for stochastic block model inference)
- **UMAP notebooks**: `umap-learn`, `sklearn`
- **Geometric renormalization**: requires external repos [d-mercator](https://github.com/networkgeometry/d-mercator) and [Geometric-renormalization-of-weighted-network](https://github.com/zhmh163/Geometric-renormalization-of-weighted-network)

## Architecture

### Core Library (repo root)

Three Python modules that all notebooks import:

- **`Harmonic_degree.py`** — The central module. Key function `H_CF_cluster(Ag, clusters)` takes a NetworkX graph and a node→cluster dict, returns harmonic degree, conformal degree, and deviation measures. Also contains `renorm_graph_harmonic()` for Laplacian renormalization with harmonic analysis, and `H_CF_curves()` which auto-finds the collapse time and sweeps.
- **`Higher_order_harmonic_degree.py`** — Extends harmonic degree to simplicial complexes of arbitrary dimension. Uses `higher_order_renormalization()` which projects out the kernel of the Hodge Laplacian before diffusing. Imports from both `Harmonic_degree` and `HOLR_functions`.
- **`HOLR_functions.py`** — Utilities from [higher_order_LRG](https://github.com/nplresearch/higher_order_LRG). Provides: simplicial complex generators (`NGF`, `pseudofractal_d2`, `apollonian_d2`), boundary matrix construction (`boundary_matrices_ext`), Hodge Laplacians (`laplacians`), cross-order adjacency (`adjacency_of_order`), spectral dimension (`compute_spectral_d`), entropic susceptibility (`compute_entropic_C`), and simplicial complex plotting (`plot_complex`).

### Packaged Library (`harmonic_morphisms/`)

Alongside the root-level scripts, a packaged version lives under `harmonic_morphisms/` (`src/`, `tests/`, `pyproject.toml`). This is what the test suite and CI target:

- Install: `pip install -e "harmonic_morphisms/[test]"`
- Test: `pytest harmonic_morphisms/tests/` — GitHub Actions runs these on Python 3.9 / 3.11 / 3.12 via `.github/workflows/tests.yml`

### Key Concepts in the Code

- **Clusters dict**: `{node_id: cluster_id}` — the standard input format for `H_CF_cluster`. All renormalization methods produce this. Represents the surjective map φ: V → V from the paper.
- **Horizontal conformality check**: `H_CF_cluster` iterates over each node x, counts neighbors in each adjacent macro-set (the multiplicity k_{y'}(x) from Eq. 5 in the paper), and checks if all counts are equal. If so, x is a "harmonic node." The conformal check additionally includes within-macro-set neighbors + self.
- **Metagraph (Gv)**: For Laplacian renormalization, nodes are connected when ρ_ij(t) ≥ min(ρ_ii, ρ_jj) − ε, where ρ = exp(−tL). Connected components of Gv define the clusters. The diffusion time t is the continuous scale parameter.
- **Compression η**: Defined as 1 − |V|/|V|, the fraction of nodes removed. Used as the x-axis for fingerprint plots.
- **Simplicial complex (sc)**: A dict with keys `"nodes"`, `"edges"`, `"faces"`, `"tetrahedra"`, `"4-simplices"` (sorted numpy arrays) and counts `"n0"` through `"n4"`.
- **Collapse time (t_f)**: The smallest diffusion time at which Laplacian renormalization reduces the graph to a single node. Found by `iter_narrow_g()` with 0.1 precision.

### Experiment Directories

- **`Clustering/`** — Main clustering experiments. Data preprocessing is in `GT_Tools_producing_data/Preprocessing_and_SBM_creation.ipynb` (must run first, outputs to `Intermediate_outputs_*` folders). `Producing_Harmonic_degree_clustering.ipynb` generates results stored in `Final_outputs/`. `Visualizations_UMAP/` produces UMAP plots.
- **`Euroroad_results/`** — Complete renormalization group analysis of the Euroroad network across all three methods (Laplacian, Geometric, GNN). The main notebook `Euroroad_make_all_results.ipynb` imports from the root modules and from `gnn_files/`.
- **`GNN_partition_function/`** — GNN-based renormalization using code adapted from [Nature paper](https://www.nature.com/articles/s41467-025-56034-2). Contains `model.py` (Encoder, WeightSumDecoder), `data.py` (feature extraction), `utils.py` (cross-entropy loss).
- **`Higher_Order/`** — Higher-order Laplacian renormalization on simplicial complexes (synthetic and real).
- **`Laplacian/`** — Standard and equilibrium Laplacian renormalization experiments.
- **`Geometric/1/`** — Geometric renormalization (requires external d-mercator tool).
- **`Finding_harmonic_Morph/`** — Experimental approaches for finding harmonic morphisms.
- **`pre_computed_measures/`** — Pickled results (`.pkl`) for various networks, used by `plot_average.ipynb`.

### Data Flow

1. Raw network data lives in `Data/` (edgelists, MTX files from networkrepository.com, SNAP, BioSNAP)
2. `Clustering/GT_Tools_producing_data/Preprocessing_and_SBM_creation.ipynb` preprocesses into 7 grouped `Intermediate_outputs_*/` folders
3. Experiment notebooks import core modules from root (`sys.path.append('..')` is common)
4. Results are pickled to `pre_computed_measures/` or `Clustering/Final_outputs/`
5. `plot_average.ipynb` (root) and UMAP notebooks produce final figures

## Running Code

All experiments are Jupyter notebooks. Notebooks in subdirectories typically add the repo root to `sys.path` to import the core modules:
```python
sys.path.append('..')
from Harmonic_degree import *
from HOLR_functions import *
```

GNN notebooks additionally need to be run from their own directory (they import local `model.py`, `data.py`, `utils.py`).

## Paper-Code Correspondence

| Paper concept | Code location |
|---|---|
| H_mean, H_mod, H_Dev (Sec. III) | `H_CF_cluster()` in `Harmonic_degree.py` — returns `deg_h`, `M_deg_h`, `std_h` |
| CF_mean, CF_mod, CF_Dev (SM Sec. S2) | Same function — returns `deg_cf`, `M_deg_cf`, `std_cf` |
| Laplacian RG merging criterion (Sec. IV) | `renorm_graph_harmonic()` in `Harmonic_degree.py` |
| Fingerprint curves (Fig. 2d,e) | `plot_average.ipynb` using `pre_computed_measures/*.pkl` |
| Euroroad full analysis (Fig. 2a-c, Fig. 3) | `Euroroad_results/Euroroad_make_all_results.ipynb` |
| Higher-order Hodge renormalization (Sec. VI) | `higher_order_renormalization()` in `Higher_order_harmonic_degree.py` |
| GNN partition function preservation | `GNN_partition_function/model.py` (Encoder, WeightSumDecoder) |
| Entropic susceptibility C(t) | `compute_entropic_C()` in `HOLR_functions.py` |
| Spectral dimension | `compute_spectral_d()` in `HOLR_functions.py` |
