# Quick Start

## Installation

```bash
cd harmonic_morphisms
pip install -e .
```

For running the notebooks:

```bash
pip install -e ".[notebooks]"
```

## Minimal example

```python
import networkx as nx
from harmonic_morphisms import H_CF_cluster

# Create any graph and any node-to-cluster mapping
G = nx.karate_club_graph()
clusters = {n: n % 5 for n in G.nodes()}

# Compute harmonic and conformal degrees
(G_coarse, deg_h, M_deg_h, std_h, av_h, std_v_h, Not_h,
 deg_cf, M_deg_cf, std_cf, av_cf, std_v_cf, Not_cf) = H_CF_cluster(G, clusters)

print(f"Modified harmonic degree (H_mod): {M_deg_h:.3f}")
print(f"Modified conformal degree (CF_mod): {M_deg_cf:.3f}")
print(f"Harmonic deviation (H_dev): {std_h:.3f}")
```

## Laplacian renormalization

```python
import numpy as np
import networkx as nx
from harmonic_morphisms import H_CF_curves, g_len

G = nx.karate_club_graph()
L = np.array(nx.laplacian_matrix(G, nodelist=G.nodes()).todense())

# Sweep diffusion time from 0 to collapse, 50 steps, threshold 1e-3
graphs, DEG_H, M_DEG_H, STD_H, AV_H, STD_V_H, NOT_H, \
    DEG_CF, M_DEG_CF, STD_CF, AV_CF, STD_V_CF, NOT_CF, \
    gV, t_span = H_CF_curves(G, L, 50, tresh=1e-3)

# Compression axis
compression = 1 - np.array(g_len(graphs)) / G.number_of_nodes()
```

## Higher-order renormalization

```python
from harmonic_morphisms import higher_order_H_CF_curves, g_len
from harmonic_morphisms.simplicial import pseudofractal_d2, laplacians

sc = pseudofractal_d2(3)
L0, L1, L2, L3, L4, *_ = laplacians(sc)

Ag, graphs, DEG_H, M_DEG_H, STD_H, AV_H, STD_V_H, NOT_H, \
    DEG_CF, M_DEG_CF, STD_CF, AV_CF, STD_V_CF, NOT_CF, \
    gV, t_span = higher_order_H_CF_curves(sc, dim=2, Lap=L2, n=50)

compression = 1 - np.array(g_len(graphs)) / len(Ag.nodes())
```
