# Design: `harmonic_morphisms` — packaged library + reproducible notebooks

**Date:** 2026-04-01
**Author:** Claude (brainstorming with Giovanni Petri)
**Status:** Draft

## Purpose

Create a properly packaged, pip-installable Python library for the PRX paper "Harmonic morphisms and dynamical invariants in network renormalization" (Guadagnuolo, Nurisso, Galluzzi, Allard, Petri), with notebooks that reproduce the paper's core figures.

**Dual role:**
1. **Reusable library** — `pip install -e .` gives researchers `H_CF_cluster`, Laplacian RG, Hodge RG on their own networks
2. **Reproducibility companion** — notebooks reproduce core paper figures from shipped data

## Scope

### In scope
- Package the 3 core library modules under `harmonic_morphisms/`
- 6 notebooks reproducing ~14 core figures (those needing only the core library)
- Ship small network edgelists + 16 precomputed result pickles
- Minimal docs: quickstart, API reference, figure-to-notebook map

### Out of scope
- Figures requiring d-mercator, torch/torch_geometric, or graph_tool (Figures 5, 6, 9, 10, 11, 15)
- S1H2 experiment (stays in `S1H2_experiment/`, separate from this package)
- Existing experiment directories (Clustering/, Euroroad_results/, etc.) — untouched
- Original root-level .py files — untouched, existing notebooks keep working
- PyPI publishing (future step)
- License selection (deferred)

## Directory Structure

```
repo/harmonic_morphisms/
├── pyproject.toml
├── README.md
├── src/
│   └── harmonic_morphisms/
│       ├── __init__.py           # version + re-exports of key functions
│       ├── core.py               # ← Harmonic_degree.py
│       ├── higher_order.py       # ← Higher_order_harmonic_degree.py
│       └── simplicial.py         # ← HOLR_functions.py
├── notebooks/
│   ├── 01_euroroad_laplacian.ipynb
│   ├── 02_average_curves.ipynb
│   ├── 03_individual_laplacian.ipynb
│   ├── 04_higher_order_synthetic.ipynb
│   ├── 05_higher_order_real.ipynb
│   └── 06_equilibrium_laplacian.ipynb
├── data/
│   ├── networks/                 # Small edgelist files (~7 files)
│   └── precomputed/              # 16 pre_computed_measures/*.pkl files
└── docs/
    ├── quickstart.md
    ├── api.md
    └── paper_figures.md
```

## Module Mapping

Each module is a cleaned-up copy of the original source file. Changes are strictly limited to:

1. PEP8 filename (lowercase, no caps)
2. Internal imports converted to package-relative (`from .simplicial import ...`)
3. Remove `sys.path.append` hacks
4. **No API changes** — all function signatures stay identical

| New file | Source file | Key exports |
|----------|------------|-------------|
| `core.py` | `Harmonic_degree.py` | `H_CF_cluster`, `simple_renorm`, `renorm_graph_harmonic`, `H_CF_curves`, `iter_narrow_g`, `iter_g`, `h_v`, `g_len`, `clust_plot`, `renorm_graph_plot` |
| `higher_order.py` | `Higher_order_harmonic_degree.py` | `higher_order_renormalization`, `higher_order_renormalization_series`, `higher_order_H_CF_curves`, `iter_g_higher_order`, `iter_narrow_g_higher_order`, `fbc` |
| `simplicial.py` | `HOLR_functions.py` | `import_network_data`, `NGF`, `pseudofractal_d2`, `pseudofractal_d3`, `apollonian_d2`, `convert_graph_to_sc`, `boundary_matrices_ext`, `laplacians`, `adjacency_of_order`, `XO_laplacian`, `compute_entropic_C`, `compute_spectral_d`, `make_dict_ext`, `plot_complex` |

### `__init__.py`

Re-exports the most frequently used functions for convenience:

```python
"""Harmonic degree diagnostics for network renormalization."""

__version__ = "0.1.0"

from .core import (
    H_CF_cluster,
    H_CF_curves,
    simple_renorm,
    renorm_graph_harmonic,
)
from .higher_order import (
    higher_order_renormalization,
    higher_order_H_CF_curves,
)
```

Less common functions accessed via submodule: `from harmonic_morphisms.simplicial import pseudofractal_d2`.

### Import rewiring

The original cross-module imports:

| Original | Packaged |
|----------|----------|
| `from Harmonic_degree import H_CF_cluster` | `from .core import H_CF_cluster` |
| `from HOLR_functions import *` | `from .simplicial import import_network_data, NGF, ...` (explicit) |
| `from Harmonic_degree import *` (in Higher_order) | `from .core import H_CF_cluster, simple_renorm` (explicit) |

Wildcard imports (`from X import *`) are replaced with explicit imports listing only what's used.

## `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "harmonic-morphisms"
version = "0.1.0"
description = "Harmonic degree diagnostics for network renormalization"
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
    "networkx>=3.0",
    "numpy>=1.24",
    "scipy>=1.10",
    "matplotlib>=3.7",
]

[project.optional-dependencies]
notebooks = ["jupyter", "pandas"]

[tool.setuptools.packages.find]
where = ["src"]
```

Only the 4 core dependencies that every function needs. No torch, graph_tool, umap-learn.

## Notebooks

Each notebook is self-contained: imports the package, loads data from `../data/`, produces figures, optionally saves PDFs.

| # | Notebook | Paper figures | What it computes | Data inputs |
|---|----------|--------------|-----------------|-------------|
| 1 | `01_euroroad_laplacian.ipynb` | 2a (Laplacian panel), 3 | Load Euroroad → `H_CF_curves()` → harmonic/conformal degree vs compression + spatial harmonic deviation map | `data/networks/euroroad.edgelist` |
| 2 | `02_average_curves.ipynb` | 2d-e, 7, 8 | Load 16 precomputed pickles → interpolate to common compression axis → plot per-network 4×4 grid + grand averages (all 3 methods from precomputed data) | `data/precomputed/*.pkl` |
| 3 | `03_individual_laplacian.ipynb` | 12, 13, 14 | NetSci, Facebook, C.Elegans: run Laplacian RG with `H_CF_curves()`, plot harmonic degree + coarse-grained graph visualizations | `data/networks/{netscience,facebook,celegans}.edgelist` |
| 4 | `04_higher_order_synthetic.ipynb` | 4, 17, 18 | Generate pseudofractal d2/d3 → Hodge Laplacians → `higher_order_H_CF_curves()` → entropic susceptibility + spectral dimension + harmonic degree for Hodge/Bochner/XO operators | None (programmatic) |
| 5 | `05_higher_order_real.ipynb` | 19 | Load Thiers13 simplicial complex → same pipeline as notebook 4 | `data/networks/thiers13.json` |
| 6 | `06_equilibrium_laplacian.ipynb` | 16 | NetSci, C.Elegans, Tortoise: equilibrium Laplacian RG variant | `data/networks/{netscience,celegans,tortoise}.edgelist` |

### Notebook conventions
- First cell: `%matplotlib inline` + package import
- Second cell: `DATA_DIR = Path("../data")` — single path constant
- Plotting style matches paper: use matplotlib RC from `simplicial.py` conventions (SMALL_SIZE=10, MEDIUM_SIZE=12, BIGGER_SIZE=13)
- Each figure gets its own clearly labeled section with a markdown header: `## Figure 7: Harmonic degree (all networks)`
- Final cell of each figure section: `fig.savefig("fig07_harmonic_degree.pdf", bbox_inches="tight")`

## Data

### `data/networks/` — edgelist files

Copied from existing `Data/` directory, only the files needed by the 6 notebooks:

| File | Source path (relative to repo root) | Used by |
|------|--------------------------------------|---------|
| `out.subelj_euroroad_euroroad` | `Data/out.subelj_euroroad_euroroad` | Notebook 1 |
| `out.dimacs10-netscience` | `Data/out.dimacs10-netscience` | Notebooks 3, 6 |
| `out.ego-facebook` | `Data/out.ego-facebook` | Notebook 3 |
| `out.dimacs10-celegans_metabolic` | `Data/out.dimacs10-celegans_metabolic` | Notebooks 3, 6 |
| `reptilia-tortoise-network-fi.edges` | `Data/reptilia-tortoise-network-fi/reptilia-tortoise-network-fi.edges` | Notebook 6 |
| `random_10_0.85min_cliques_Thiers13.json` | `Higher_Order/random_10_0.85min_cliques_Thiers13.json` | Notebook 5 |

Files are copied with their original names to preserve compatibility with `import_network_data()`.

### `data/precomputed/` — result pickles

All 16 files from `pre_computed_measures/`, copied as-is:

`pw_results.pkl`, `lc_results.pkl`, `yeast_results.pkl`, `tort_results.pkl`, `er_results.pkl`, `em_results.pkl`, `Cel_results.pkl`, `b9_results.pkl`, `Sif_results.pkl`, `Euroroad_results.pkl`, `we_results.pkl`, `bf_results.pkl`, `pl_results.pkl`, `Ns_results.pkl`, `wpl_results.pkl`, `hf_results.pkl`

These contain Laplacian, Geometric, and GNN results already computed, so notebook 02 can plot all three methods without external dependencies.

## Documentation

### `docs/quickstart.md`
- Installation: `pip install -e .`
- Minimal example (~10 lines): generate a random graph, apply a random clustering, compute harmonic degree with `H_CF_cluster`
- Pointer to notebooks for full usage

### `docs/api.md`
Hand-written API reference, one section per module:

- **`harmonic_morphisms.core`** — each exported function with signature, one-line description, and parameter types
- **`harmonic_morphisms.higher_order`** — same
- **`harmonic_morphisms.simplicial`** — same

Grouped by purpose within each module (e.g., "Harmonic degree computation", "Laplacian renormalization", "Utilities").

### `docs/paper_figures.md`
Table mapping every reproducible figure to its notebook:

| Figure | Description | Notebook | Section |
|--------|------------|----------|---------|
| 2a | Euroroad Laplacian RG | `01_euroroad_laplacian.ipynb` | "Figure 2a" |
| 2d-e | Average curves | `02_average_curves.ipynb` | "Figures 2d-e" |
| ... | ... | ... | ... |

## What stays unchanged

- `Harmonic_degree.py`, `HOLR_functions.py`, `Higher_order_harmonic_degree.py` at repo root — untouched
- All existing experiment directories (`Clustering/`, `Euroroad_results/`, `Higher_Order/`, `Laplacian/`, `Geometric/`, `GNN_partition_function/`, `Finding_harmonic_Morph/`) — untouched
- `S1H2_experiment/` — untouched, stays separate
- `plot_average.ipynb` at repo root — untouched
- `Data/` — untouched (we copy needed files into `harmonic_morphisms/data/networks/`)
- `pre_computed_measures/` — untouched (we copy into `harmonic_morphisms/data/precomputed/`)

## Implementation sequence

1. Create directory structure + `pyproject.toml` + `README.md`
2. Copy and adapt `core.py` ← `Harmonic_degree.py` (fix imports)
3. Copy and adapt `simplicial.py` ← `HOLR_functions.py` (fix imports)
4. Copy and adapt `higher_order.py` ← `Higher_order_harmonic_degree.py` (fix imports)
5. Write `__init__.py`
6. Verify: `pip install -e .` + `python -c "from harmonic_morphisms import H_CF_cluster"`
7. Copy data files into `data/`
8. Create notebooks 01-06 (one at a time, test each)
9. Write docs (quickstart, api, paper_figures)
