# Harmonic Morphisms and Dynamical Invariants in Network Renormalization

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg) ![Tests](https://img.shields.io/badge/tests-78%20passed-brightgreen.svg)

This repository provides code and data accompanying Guadagnuolo et al. (2026). We prove that discrete harmonic morphisms exactly characterize coarse-grainings that preserve random-walk dynamics across network scales. The code implements the harmonic degree diagnostic and applies it to geometric, Laplacian, and GNN-based renormalization across 50 real-world networks.

## Quick Start

```bash
pip install -r requirements.txt
cd harmonic_morphisms && pip install -e .
pytest tests/ -v  # 78 tests
```

## Repository Structure

```
├── Harmonic_degree.py                   # Core harmonic degree computation
├── Higher_order_harmonic_degree.py      # Hodge Laplacian extension
├── HOLR_functions.py                    # Higher-order utilities
├── harmonic_morphisms/                  # Installable Python package (refactored API)
│   ├── src/                             # Package source
│   ├── tests/                           # 78 unit tests
│   └── notebooks/                       # Figure reproduction notebooks
├── Data/                                # 50 network datasets (see Data/NETWORKS.md)
├── Clustering/                          # Clustering benchmark (50 networks × 5 methods)
├── Euroroad_results/                    # Complete RG analysis of Euro-Road network
├── Geometric/                           # Geometric renormalization (requires d-mercator)
├── Laplacian/                           # Laplacian + Equilibrium Laplacian RG
├── GNN_partition_function/              # GNN-based renormalization (requires PyTorch)
├── Higher_Order/                        # Higher-order simplicial complex analysis
├── Finding_harmonic_Morph/              # Harmonic morphism search algorithms
├── pre_computed_measures/               # Pre-computed results for 16-network comparison
└── plot_average.ipynb                   # Average fingerprint curves
```

## Reproducing Paper Figures

The 6 notebooks in `harmonic_morphisms/notebooks/` reproduce the main results. For the full figure-to-notebook mapping see `harmonic_morphisms/docs/paper_figures.md`. Figures involving geometric renormalization require d-mercator; GNN figures require PyTorch Geometric.

## Core API

```python
from Harmonic_degree import H_CF_cluster
import networkx as nx

G = nx.karate_club_graph()
clusters = {n: n % 4 for n in G.nodes()}  # example partition
results = H_CF_cluster(G, clusters)
print(f"H_mod = {results[1]:.3f}")
```

## Data

See `Data/NETWORKS.md` for the complete manifest of 50 networks.

## External Dependencies

| Tool | Used for | Install |
|------|----------|---------|
| [d-mercator](https://github.com/networkgeometry/d-mercator) | Geometric renormalization | See repo README |
| [graph-tool](https://graph-tool.skewed.de/) | SBM inference for clustering | `conda install -c conda-forge graph-tool` |
| [PyTorch Geometric](https://pyg.org/) | GNN renormalization | `pip install torch torch_geometric` |

## Tests

```bash
cd harmonic_morphisms && pytest tests/ -v
```

78 tests covering core algorithms, higher-order extensions, and integration.

## Citation

```bibtex
@article{guadagnuolo2026harmonic,
  title={Harmonic morphisms and dynamical invariants in network renormalization},
  author={Guadagnuolo, Francesco Maria and Nurisso, Marco and Galluzzi, Federica and Allard, Antoine and Petri, Giovanni},
  journal={Physical Review X},
  year={2026}
}
```

## License

MIT. See LICENSE.

## Contact

francesco.guadagnuolo@epfl.ch
