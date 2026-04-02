# harmonic_morphisms

Harmonic degree diagnostics for network renormalization.

Companion code for the PRX paper: *"Harmonic morphisms and dynamical invariants in network renormalization"* (Guadagnuolo, Nurisso, Galluzzi, Allard, Petri).

## Installation

```bash
pip install -e .
```

For running the notebooks:

```bash
pip install -e ".[notebooks]"
```

## Quick start

```python
import networkx as nx
from harmonic_morphisms import H_CF_cluster

# Any graph + any node→cluster mapping
G = nx.karate_club_graph()
clusters = {n: n % 5 for n in G.nodes()}

(G_coarse, deg_h, M_deg_h, std_h, av_h, std_v_h, Not_h,
 deg_cf, M_deg_cf, std_cf, av_cf, std_v_cf, Not_cf) = H_CF_cluster(G, clusters)

print(f"Modified harmonic degree: {M_deg_h:.3f}")
print(f"Modified conformal degree: {M_deg_cf:.3f}")
print(f"Harmonic deviation: {std_h:.3f}")
```

## Notebooks

Notebooks in `notebooks/` reproduce core figures from the paper. See `docs/paper_figures.md` for the mapping.

## API

See `docs/api.md` for full API reference.
