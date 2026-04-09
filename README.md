# Harmonic Morphisms and Dynamical Invariants in Network Renormalization

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org)
[![Tests](https://github.com/nplresearch/harmonic_degree/actions/workflows/tests.yml/badge.svg)](https://github.com/nplresearch/harmonic_degree/actions)

Code and data accompanying:

> **Harmonic morphisms and dynamical invariants in network renormalization**  
> F. M. Guadagnuolo, M. Nurisso, F. Galluzzi, A. Allard, G. Petri  
> *Physical Review X*, 2026

We show that discrete harmonic morphisms — surjective graph maps that preserve harmonic functions — exactly characterize coarse-grainings that maintain first-exit random-walk dynamics across scales. The **harmonic degree** is a scalar diagnostic that measures how closely any coarse-graining approximates a harmonic morphism. We apply this to three renormalization methods (geometric, Laplacian, GNN-based) across 50 real-world networks, revealing characteristic dynamical fingerprints and discovering that Laplacian renormalization spontaneously produces *exact* harmonic morphisms in certain networks.

---

## Quick start

```bash
# 1. Install core dependencies
pip install -r requirements.txt

# 2. (Optional) install the refactored API package
cd harmonic_morphisms && pip install -e . && cd ..

# 3. Run the test suite
cd harmonic_morphisms && pytest tests/ -v
```

Then open any notebook in the experiment folders listed below. Each notebook imports the core modules from the repo root via `sys.path.insert(1, '../')`.

---

## Repository structure

```
harmonic_degree/
│
│  # Core Python modules — imported by all experiment notebooks
├── Harmonic_degree.py
├── Higher_order_harmonic_degree.py
├── HOLR_functions.py
│
│  # Main experiment notebooks and pre-computed results
├── plot_average.ipynb
├── pre_computed_measures/
│
│  # Experiment folders (one per analysis type)
├── Euroroad_results/
├── Clustering/
├── Geometric/
├── Laplacian/
├── GNN_partition_function/
├── Higher_Order/
├── Finding_harmonic_Morph/
│
│  # All 50 network datasets
├── Data/
│
│  # Installable Python package (refactored API + tests)
└── harmonic_morphisms/
```

---

## Core modules

These three files live at the repo root and are the computational foundation for all experiments.

### `Harmonic_degree.py`

The central module. Key functions:

| Function | Description |
|---|---|
| `H_CF_cluster(Ag, clusters)` | Compute all harmonic and conformal degree metrics for a given partition. Returns H_mean, H_mod, H_dev and CF analogues. |
| `renorm_graph_harmonic(G, t)` | Laplacian renormalization at diffusion time t. Returns the coarse-grained graph and the partition. |
| `H_CF_curves(G)` | Sweep over diffusion times from t=0 to collapse, returning harmonic degree curves. |
| `clust_plot(Ag, clusters)` | Build and colour the coarse-grained graph for visualisation. |

The `clusters` argument throughout is a `{node_id: cluster_id}` dict — the discrete representation of the map φ: V → V̄.

### `Higher_order_harmonic_degree.py`

Extends harmonic degree to simplicial complexes of arbitrary dimension using Hodge Laplacians. Key function: `higher_order_renormalization()`, which projects out the Laplacian kernel before diffusion and sweeps over scales, returning harmonic degree curves at each order k.

### `HOLR_functions.py`

Utilities for higher-order Laplacian renormalization, adapted from [nplresearch/higher_order_LRG](https://github.com/nplresearch/higher_order_LRG). Provides simplicial complex construction (`NGF`, `pseudofractal_d2`, `apollonian_d2`), Hodge Laplacians (`laplacians`), boundary matrices (`boundary_matrices_ext`), spectral dimension (`compute_spectral_d`), and entropic susceptibility (`compute_entropic_C`).

---

## Experiment folders

### `Euroroad_results/`

**Full three-method renormalization analysis of the Euro-Road network.**  
`Euroroad_make_all_results.ipynb` runs all three methods (Laplacian, Geometric, GNN) on the same network and generates the harmonic degree curves, spatial deviation maps, and coarse-grained graph visualisations. This is the primary worked example in the paper (Figs 2a–c, 3).

Geometric results require the `geom_files/` pre-processed coordinates (produced by d-mercator). GNN results use the `gnn_files/` local modules (model.py, data.py, utils.py).

### `Clustering/`

**Clustering benchmark across 50 real-world networks.**  
Tests five community-detection methods (Louvain, Leiden, SBM, Infomap, Label Propagation) against the harmonic degree standard. Results feed into the UMAP and comparison tables in the paper.

Sub-structure:
- `GT_Tools_producing_data/Preprocessing_and_SBM_creation.ipynb` — **must run first** to preprocess raw networks from `Data/` into the `Intermediate_outputs_*/` folders (requires `graph_tool`).
- `Producing_Harmonic_degree_clustering.ipynb` — computes H_mod for each (network, method) pair; outputs to `Final_outputs/df_1.pkl–df_7.pkl`.
- `Clustering_examples.ipynb` — produces the clustering visualisations shown in the paper (Fig 5).
- `Visualizations_UMAP/` — UMAP embeddings of networks in harmonic degree space (Fig 6; requires `umap-learn`).
- `Classical_Summaries/` — pre-computed classical network metrics used in the UMAP.

### `Geometric/1/`

**Geometric renormalization on real networks.**  
Hyperbolic embedding-based coarse-graining (García-Pérez et al. 2018). Requires the external tool [d-mercator](https://github.com/networkgeometry/d-mercator) to compute hyperbolic coordinates, plus [Geometric-renormalization-of-weighted-network](https://github.com/zhmh163/Geometric-renormalization-of-weighted-network) for the renormalization step.

### `Laplacian/`

**Laplacian renormalization on real networks, including the Equilibrium Laplacian variant.**  
`Real_networks_LRG.ipynb` applies the standard diffusion-based coarse-graining. The `In Equilibrium Laplacian/` sub-folder contains experiments with the equilibrium version (finite-temperature limit of the Laplacian RG).

### `GNN_partition_function/`

**GNN-based renormalization.**  
Implements the partition-function-preserving GNN renormalization from [De Domenico et al., Nature Communications 2025](https://www.nature.com/articles/s41467-025-56034-2). Local modules: `model.py` (Encoder + WeightSumDecoder), `data.py` (feature extraction), `utils.py` (loss functions). Requires `torch` and `torch_geometric`.

`Real_nets_GNN.ipynb` applies this to the full set of real networks.

### `Higher_Order/`

**Harmonic degree on simplicial complexes via Hodge Laplacian renormalization.**  
`Higher_order_synthetic_examples.ipynb` tests on synthetic complexes (pseudofractals, apollonian). `Higher_order_real_examples.ipynb` applies to real contact-network simplicial complexes (Thiers13, LyonSchool, InVS15, SFHH, LH10) stored as `.json` files in this folder.

Demonstrates dimensional selectivity: harmonic degree at order k measures harmonicity of k-th order structure, and the renormalization path differs across Hodge orders.

### `Finding_harmonic_Morph/`

**Direct search for harmonic morphisms via greedy optimisation.**  
`Harmonic_Modularity.ipynb` frames partition search as an optimisation problem with a **harmonic modularity** objective:

$$Q_H = Q_\text{mod} + \lambda \cdot (-\text{H}_\text{dev})$$

A greedy best-improvement algorithm explores all single-node reassignments and accepts the best move at each step. Three cases are compared on a Barabási–Albert graph: harmonicity-only (λ → ∞), modularity-only (λ = 0), and joint (λ = 1).

### `pre_computed_measures/`

**Pre-computed results for the 16-network three-method comparison.**  
Pickle files `<network>_results.pkl` store (compression η, H_mod, H_dev) curves for all three methods on 16 networks. Loaded by `plot_average.ipynb` to reproduce the fingerprint curve figures (Figs 2d–e, 7–8).

The 16 networks here are the subset for which all three renormalization methods converge fully; the broader 50-network set is used only for the clustering benchmark.

### `plot_average.ipynb`

**Average harmonic degree fingerprint curves across all 16 networks and methods.**  
Loads from `pre_computed_measures/`, computes method-wise averages with confidence bands, and produces Figs 2d–e, 7–8 of the paper.

---

## Paper figure map

For the complete figure-to-notebook mapping see `harmonic_morphisms/docs/paper_figures.md`.

| Figures | Notebook |
|---------|----------|
| 2a, 3 (Euroroad curves) | `Euroroad_results/Euroroad_make_all_results.ipynb` |
| 2d–e, 7–8 (average fingerprints) | `plot_average.ipynb` |
| 4, 17–19 (higher-order) | `harmonic_morphisms/notebooks/04_higher_order_synthetic.ipynb`, `05_higher_order_real.ipynb` |
| 5 (clustering examples) | `Clustering/Clustering_examples.ipynb` |
| 6 (UMAP) | `Clustering/Visualizations_UMAP/Visualize_Harmonic_Degree.ipynb` |
| 12–14 (individual Laplacian) | `harmonic_morphisms/notebooks/03_individual_laplacian.ipynb` |
| 16 (equilibrium Laplacian) | `harmonic_morphisms/notebooks/06_equilibrium_laplacian.ipynb` |
| 2b–c, 9–11 (geometric) | `Geometric/1/` (requires d-mercator) |
| 15 (GNN) | `GNN_partition_function/Real_nets_GNN.ipynb` (requires torch_geometric) |

---

## Data

`Data/` contains all 50 network datasets in their original formats (`.edges`, `.mtx`, `.txt`). See `Data/NETWORKS.md` for the full manifest with node/edge counts, categories, and sources.

Networks are drawn from three public repositories:
- [Network Repository](https://networkrepository.com/)
- [SNAP](https://snap.stanford.edu/)
- [BioSNAP](https://snap.stanford.edu/biodata/)

---

## Installable package: `harmonic_morphisms/`

A refactored, pip-installable version of the core algorithms with a clean API and a full test suite.

```bash
cd harmonic_morphisms
pip install -e ".[test]"
pytest tests/ -v          # 79 tests
```

The package source lives in `harmonic_morphisms/src/harmonic_morphisms/`. The `notebooks/` sub-folder (01–06) contains cleaned versions of the main figure notebooks that use the package API rather than `sys.path` imports.

---

## External tools (optional)

Some analyses require separate installation:

| Tool | Used for | Install |
|------|----------|---------|
| [d-mercator](https://github.com/networkgeometry/d-mercator) | Geometric renormalization hyperbolic embedding | See repo README |
| [Geometric-renorm-weighted](https://github.com/zhmh163/Geometric-renormalization-of-weighted-network) | Geometric renormalization coarse-graining step | See repo README |
| [graph-tool](https://graph-tool.skewed.de/) | SBM inference in clustering benchmark | `conda install -c conda-forge graph-tool` |
| [PyTorch Geometric](https://pyg.org/) | GNN renormalization | `pip install torch torch_geometric` |
| [umap-learn](https://umap-learn.readthedocs.io/) | UMAP visualisations | `pip install umap-learn` |

---

## Citation

```bibtex
@article{guadagnuolo2026harmonic,
  title   = {Harmonic morphisms and dynamical invariants in network renormalization},
  author  = {Guadagnuolo, Francesco Maria and Nurisso, Marco and Galluzzi, Federica
             and Allard, Antoine and Petri, Giovanni},
  journal = {Arxiv},
  year    = {2026}
}
```

---

## License

MIT. See [LICENSE](LICENSE).

## Contact

Francesco Maria Guadagnuolo — francesco.guadagnuolo@epfl.ch 
Giovanni Petri — g.petri@northeastern.edu

