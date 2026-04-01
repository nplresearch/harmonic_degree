# `harmonic_morphisms` Package Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a pip-installable `harmonic_morphisms` package with 6 notebooks reproducing the PRX paper's core figures.

**Architecture:** src-layout Python package wrapping the 3 existing library modules with minimal changes (import rewiring only). Notebooks load data from a co-located `data/` directory. No API changes to any function.

**Tech Stack:** Python ≥3.9, networkx, numpy, scipy, matplotlib. Jupyter for notebooks.

**Spec:** `docs/superpowers/specs/2026-04-01-harmonic-morphisms-package-design.md`

---

### Task 1: Directory structure and packaging

**Files:**
- Create: `harmonic_morphisms/pyproject.toml`
- Create: `harmonic_morphisms/README.md`
- Create: `harmonic_morphisms/src/harmonic_morphisms/__init__.py` (placeholder)

- [ ] **Step 1: Create directory tree**

```bash
cd /Users/gpetri/Library/CloudStorage/Dropbox/development/network-foundations/harmonic-morphisms/repo
mkdir -p harmonic_morphisms/src/harmonic_morphisms
mkdir -p harmonic_morphisms/notebooks
mkdir -p harmonic_morphisms/data/networks
mkdir -p harmonic_morphisms/data/precomputed
mkdir -p harmonic_morphisms/docs
```

- [ ] **Step 2: Write pyproject.toml**

Create `harmonic_morphisms/pyproject.toml`:

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

- [ ] **Step 3: Write README.md**

Create `harmonic_morphisms/README.md`:

```markdown
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
```

- [ ] **Step 4: Write placeholder __init__.py**

Create `harmonic_morphisms/src/harmonic_morphisms/__init__.py`:

```python
"""Harmonic degree diagnostics for network renormalization."""

__version__ = "0.1.0"
```

- [ ] **Step 5: Commit**

```bash
git add harmonic_morphisms/
git commit -m "feat: scaffold harmonic_morphisms package directory"
```

---

### Task 2: Create core.py from Harmonic_degree.py

**Files:**
- Create: `harmonic_morphisms/src/harmonic_morphisms/core.py`
- Source: `Harmonic_degree.py` (repo root)

The source file has no cross-module imports — copy as-is.

- [ ] **Step 1: Copy source file**

```bash
cp Harmonic_degree.py harmonic_morphisms/src/harmonic_morphisms/core.py
```

No import changes needed. `core.py` imports only `networkx`, `numpy`, `scipy.linalg`, `matplotlib.colors` — all external.

- [ ] **Step 2: Verify import works**

```bash
cd harmonic_morphisms && python -c "from src.harmonic_morphisms.core import H_CF_cluster; print('core.py OK')" && cd ..
```

Expected: `core.py OK`

- [ ] **Step 3: Commit**

```bash
git add harmonic_morphisms/src/harmonic_morphisms/core.py
git commit -m "feat: add core.py (Harmonic_degree.py)"
```

---

### Task 3: Create simplicial.py from HOLR_functions.py

**Files:**
- Create: `harmonic_morphisms/src/harmonic_morphisms/simplicial.py`
- Source: `HOLR_functions.py` (repo root)

The source file has no cross-module imports — copy as-is.

- [ ] **Step 1: Copy source file**

```bash
cp HOLR_functions.py harmonic_morphisms/src/harmonic_morphisms/simplicial.py
```

No import changes needed. `simplicial.py` imports only `networkx`, `numpy`, `scipy.sparse`, `itertools.combinations`, `matplotlib.pyplot` — all external.

- [ ] **Step 2: Verify import works**

```bash
cd harmonic_morphisms && python -c "from src.harmonic_morphisms.simplicial import pseudofractal_d2, laplacians; print('simplicial.py OK')" && cd ..
```

Expected: `simplicial.py OK`

- [ ] **Step 3: Commit**

```bash
git add harmonic_morphisms/src/harmonic_morphisms/simplicial.py
git commit -m "feat: add simplicial.py (HOLR_functions.py)"
```

---

### Task 4: Create higher_order.py from Higher_order_harmonic_degree.py

**Files:**
- Create: `harmonic_morphisms/src/harmonic_morphisms/higher_order.py`
- Source: `Higher_order_harmonic_degree.py` (repo root)

This file has two cross-module imports that must be converted to relative imports.

- [ ] **Step 1: Copy and fix imports**

```bash
cp Higher_order_harmonic_degree.py harmonic_morphisms/src/harmonic_morphisms/higher_order.py
```

Then edit `harmonic_morphisms/src/harmonic_morphisms/higher_order.py` — change lines 5-6 from:

```python
from  HOLR_functions import adjacency_of_order
from Harmonic_degree import H_CF_cluster
```

to:

```python
from .simplicial import adjacency_of_order
from .core import H_CF_cluster
```

- [ ] **Step 2: Verify import works**

```bash
cd harmonic_morphisms && python -c "from src.harmonic_morphisms.higher_order import higher_order_H_CF_curves; print('higher_order.py OK')" && cd ..
```

Expected: `higher_order.py OK`

- [ ] **Step 3: Commit**

```bash
git add harmonic_morphisms/src/harmonic_morphisms/higher_order.py
git commit -m "feat: add higher_order.py with relative imports"
```

---

### Task 5: Finalize __init__.py and verify pip install

**Files:**
- Modify: `harmonic_morphisms/src/harmonic_morphisms/__init__.py`

- [ ] **Step 1: Write final __init__.py**

Replace `harmonic_morphisms/src/harmonic_morphisms/__init__.py` with:

```python
"""Harmonic degree diagnostics for network renormalization."""

__version__ = "0.1.0"

from .core import (
    H_CF_cluster,
    H_CF_curves,
    simple_renorm,
    renorm_graph_harmonic,
    renorm_graph_plot,
    clust_plot,
    iter_g,
    iter_narrow_g,
    h_v,
    g_len,
)
from .higher_order import (
    higher_order_renormalization,
    higher_order_renormalization_series,
    higher_order_H_CF_curves,
    iter_g_higher_order,
    iter_narrow_g_higher_order,
    fbc,
)
```

- [ ] **Step 2: pip install in editable mode**

```bash
cd harmonic_morphisms && pip install -e . && cd ..
```

Expected: `Successfully installed harmonic-morphisms-0.1.0`

- [ ] **Step 3: Verify imports from installed package**

```bash
python -c "
from harmonic_morphisms import H_CF_cluster, H_CF_curves, __version__
from harmonic_morphisms.simplicial import pseudofractal_d2, laplacians, import_network_data
from harmonic_morphisms.higher_order import higher_order_H_CF_curves, fbc
print(f'harmonic_morphisms v{__version__} — all imports OK')
"
```

Expected: `harmonic_morphisms v0.1.0 — all imports OK`

- [ ] **Step 4: Quick smoke test**

```bash
python -c "
import networkx as nx
from harmonic_morphisms import H_CF_cluster

G = nx.karate_club_graph()
clusters = {n: n % 5 for n in G.nodes()}
G_c, deg_h, M_deg_h, std_h, av_h, std_v_h, Not_h, deg_cf, M_deg_cf, std_cf, av_cf, std_v_cf, Not_cf = H_CF_cluster(G, clusters)
print(f'H_mod={M_deg_h:.3f}, CF_mod={M_deg_cf:.3f}, H_dev={std_h:.3f}')
print(f'Coarse graph: {G_c.number_of_nodes()} nodes, {G_c.number_of_edges()} edges')
print('Smoke test OK')
"
```

Expected: prints metric values and `Smoke test OK`

- [ ] **Step 5: Commit**

```bash
git add harmonic_morphisms/src/harmonic_morphisms/__init__.py
git commit -m "feat: finalize __init__.py with re-exports"
```

---

### Task 6: Copy data files

**Files:**
- Copy: 6 network edgelists into `harmonic_morphisms/data/networks/`
- Copy: 16 pickle files into `harmonic_morphisms/data/precomputed/`

- [ ] **Step 1: Copy network edgelists**

```bash
cp Data/out.subelj_euroroad_euroroad harmonic_morphisms/data/networks/
cp Data/out.dimacs10-netscience harmonic_morphisms/data/networks/
cp Data/out.ego-facebook harmonic_morphisms/data/networks/
cp Data/out.dimacs10-celegans_metabolic harmonic_morphisms/data/networks/
cp Data/reptilia-tortoise-network-fi/reptilia-tortoise-network-fi.edges harmonic_morphisms/data/networks/
cp Higher_Order/random_10_0.85min_cliques_Thiers13.json harmonic_morphisms/data/networks/
```

- [ ] **Step 2: Copy precomputed pickles**

```bash
cp pre_computed_measures/*.pkl harmonic_morphisms/data/precomputed/
```

- [ ] **Step 3: Verify files exist**

```bash
ls harmonic_morphisms/data/networks/
ls harmonic_morphisms/data/precomputed/ | wc -l
```

Expected: 6 network files listed, 16 pickle files counted.

- [ ] **Step 4: Commit**

```bash
git add harmonic_morphisms/data/
git commit -m "feat: add network data and precomputed results"
```

---

### Task 7: Notebook 01 — Euroroad Laplacian (Figures 2a, 3)

**Files:**
- Create: `harmonic_morphisms/notebooks/01_euroroad_laplacian.ipynb`

This notebook loads the Euroroad network, runs Laplacian RG via `H_CF_curves`, and plots:
- Figure 2a: three-panel harmonic/conformal degree + deviation vs compression
- Figure 3: spatial clustering visualization at a specific time step

- [ ] **Step 1: Create notebook**

Create `harmonic_morphisms/notebooks/01_euroroad_laplacian.ipynb` with these cells:

**Cell 1 (markdown):**
```markdown
# Notebook 01: Euroroad Laplacian Renormalization
Reproduces **Figure 2a** (Laplacian harmonic/conformal degree curves) and **Figure 3** (spatial deviation map) from the PRX paper.
```

**Cell 2 (code):**
```python
%matplotlib inline
from pathlib import Path
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from harmonic_morphisms import H_CF_curves, renorm_graph_harmonic, g_len
from harmonic_morphisms.core import renorm_graph_plot
from harmonic_morphisms.simplicial import import_network_data

DATA_DIR = Path("../data")

SMALL_SIZE = 10
MEDIUM_SIZE = 12
BIGGER_SIZE = 13
plt.rc("font", size=SMALL_SIZE)
plt.rc("axes", titlesize=SMALL_SIZE)
plt.rc("axes", labelsize=MEDIUM_SIZE)
plt.rc("xtick", labelsize=SMALL_SIZE)
plt.rc("ytick", labelsize=SMALL_SIZE)
plt.rc("legend", fontsize=SMALL_SIZE)
plt.rc("figure", titlesize=BIGGER_SIZE)
```

**Cell 3 (code):**
```python
# Load Euroroad network
f_road = open(DATA_DIR / "networks" / "out.subelj_euroroad_euroroad")
Ag = import_network_data(f_road)
print(f"Euroroad: {Ag.number_of_nodes()} nodes, {Ag.number_of_edges()} edges")
```

**Cell 4 (code):**
```python
# Compute Laplacian and run H_CF_curves
L0 = nx.laplacian_matrix(Ag, nodelist=Ag.nodes()).todense()

GRAPHS_l, DEG_H_L, M_DEG_H_l, STD_H_l, AV_H_l, STD_V_H_l, NOT_H_l, \
    DEG_CF_l, M_DEG_CF_l, STD_CF_l, AV_CF_l, STD_V_CF_l, NOT_CF_l, \
    gV_l, t_h_l = H_CF_curves(Ag, L0, 100, pow(10, -4))

laplacian_compression = 1 - np.array(g_len(GRAPHS_l)) / len(Ag.nodes())
print(f"Collapse time: {t_h_l[-1]:.1f}, steps: {len(GRAPHS_l)}")
```

**Cell 5 (markdown):**
```markdown
## Figure 2a: Laplacian harmonic/conformal degree vs compression
```

**Cell 6 (code):**
```python
measure_colors = ["salmon", "lightseagreen", "goldenrod"]

f = plt.figure(figsize=(11, 2.5))

ax = plt.subplot(1, 3, 1)
ax.plot(laplacian_compression, M_DEG_H_l, '-o', color=measure_colors[0], markersize=4)
ax.set_xlabel("Compression")
ax.set_ylabel("Mod. harmonic degree")
ax.set_ylim([-0.05, 1.05])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax = plt.subplot(1, 3, 2)
ax.plot(laplacian_compression, M_DEG_CF_l, '-o', color=measure_colors[1], markersize=4)
ax.set_xlabel("Compression")
ax.set_ylabel("Mod. conformal degree")
ax.set_ylim([-0.05, 1.05])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax = plt.subplot(1, 3, 3)
ax.plot(laplacian_compression, STD_H_l, '-o', color=measure_colors[2], markersize=4)
ax.set_xlabel("Compression")
ax.set_ylabel("Harmonic deviation")
ax.set_ylim([-0.05, 0.65])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.suptitle("Laplacian renormalization on Euroroad network")
plt.tight_layout()
f.savefig("fig02a_euroroad_laplacian.pdf", bbox_inches="tight")
plt.show()
```

**Cell 7 (markdown):**
```markdown
## Figure 3: Spatial distribution of harmonic deviation
```

**Cell 8 (code):**
```python
t = 4
G, deg_h, M_deg_h, std_h, av_h, std_v_h, Not_h, \
    deg_cf, M_deg_cf, std_cf, av_cf, std_v_cf, Not_cf, Gv = \
    renorm_graph_harmonic(Ag, t, L0, pow(10, -4))

Values = [deg_h, M_deg_h, std_h, deg_cf, M_deg_cf, std_cf]
Labels = ["H", "Mod. H", "Std. H", "CF", "Mod. CF", "Std. CF"]
df = pd.DataFrame([Values], columns=Labels)
print(df.to_string(index=False))

G_plot, colors_d, sing_col = renorm_graph_plot(Ag, t, L0, pow(10, -4))
colors = [colors_d[n] for n in Ag.nodes()]
layout = nx.spring_layout(Ag, iterations=100, seed=42)
lay2 = nx.spring_layout(G_plot, iterations=100, seed=42)

f, ax = plt.subplots(1, 2, figsize=(8.3, 4))

nodes = nx.draw_networkx_nodes(Ag, ax=ax[0], pos=layout, node_color=colors, node_size=14)
nodes.set_edgecolor("white")
nx.draw_networkx_edges(Ag, ax=ax[0], pos=layout, width=0.8)
ax[0].collections[0].set_linewidth(0.7)
ax[0].collections[0].set_edgecolor("#FFFFFF")
ax[0].set_title("Clustering", fontsize=10)
ax[0].axis("off")

nodes_2 = nx.draw_networkx_nodes(G_plot, ax=ax[1], pos=lay2, node_color=sing_col, node_size=60)
nodes_2.set_edgecolor("white")
nx.draw_networkx_edges(G_plot, ax=ax[1], pos=lay2, width=1.2)
ax[1].collections[0].set_linewidth(0.6)
ax[1].collections[0].set_edgecolor("#FFFFFF")
compression = 1 - len(G_plot.nodes()) / len(Ag.nodes())
ax[1].set_title(f"Coarse-grained (t={t}, η={compression:.2f})", fontsize=10)
ax[1].axis("off")

f.suptitle(f"Laplacian renormalization at time {t}", fontsize=12)
plt.tight_layout()
f.savefig("fig03_euroroad_spatial.pdf", bbox_inches="tight")
plt.show()
```

- [ ] **Step 2: Test notebook runs**

```bash
cd harmonic_morphisms/notebooks && jupyter nbconvert --to notebook --execute 01_euroroad_laplacian.ipynb --output /dev/null 2>&1 && echo "Notebook 01 OK" && cd ../..
```

Expected: `Notebook 01 OK` (may take 1-2 minutes for `H_CF_curves` on Euroroad)

- [ ] **Step 3: Commit**

```bash
git add harmonic_morphisms/notebooks/01_euroroad_laplacian.ipynb
git commit -m "feat: add notebook 01 (Euroroad Laplacian, Figures 2a, 3)"
```

---

### Task 8: Notebook 02 — Average curves (Figures 2d-e, 7, 8)

**Files:**
- Create: `harmonic_morphisms/notebooks/02_average_curves.ipynb`

Loads the 16 precomputed pickles, interpolates to a common compression axis, plots per-network grids and grand averages for all 3 methods (Laplacian, Geometric, GNN).

- [ ] **Step 1: Create notebook**

Create `harmonic_morphisms/notebooks/02_average_curves.ipynb` with these cells:

**Cell 1 (markdown):**
```markdown
# Notebook 02: Average Harmonic/Conformal Degree Curves
Reproduces **Figures 2d-e** (average curves), **Figure 7** (harmonic degree per network), and **Figure 8** (conformal degree per network).
```

**Cell 2 (code):**
```python
%matplotlib inline
import os
from pathlib import Path
import pickle
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

DATA_DIR = Path("../data")

SMALL_SIZE = 10
MEDIUM_SIZE = 12
BIGGER_SIZE = 13
plt.rc("font", size=SMALL_SIZE)
plt.rc("axes", titlesize=SMALL_SIZE)
plt.rc("axes", labelsize=MEDIUM_SIZE)
plt.rc("xtick", labelsize=SMALL_SIZE)
plt.rc("ytick", labelsize=SMALL_SIZE)
plt.rc("legend", fontsize=SMALL_SIZE)
plt.rc("figure", titlesize=BIGGER_SIZE)
```

**Cell 3 (code):**
```python
# Load all 16 precomputed results
model_names = ["Laplacian", "Geometric", "GNN"]
model_colors = ["goldenrod", "salmon", "lightseagreen"]
measures_ids = {'Harmonic degree': 2, 'Conformal degree': 5, 'Harmonic deviation': 3}
# GNN DATA columns: [deg_h, std_h, M_deg_h, deg_cf, std_cf, M_deg_cf] → indices 2, 5 for M_deg_h, M_deg_cf

compressions = {m: {} for m in model_names}
h_deg = {m: {} for m in model_names}
c_deg = {m: {} for m in model_names}
net_list = []

res_path = DATA_DIR / "precomputed"
for p in sorted(os.listdir(res_path)):
    if not p.endswith(".pkl"):
        continue
    net_list.append(p)
    with open(res_path / p, "rb") as f:
        results = pickle.load(f)

    n_nodes = len(results['Graph'])

    compressions['Laplacian'][p] = results['Laplacian compression list']
    compressions['Geometric'][p] = 1 - np.array(results['Geometric graph length']) / n_nodes
    compressions['GNN'][p] = 1 - np.array(results['GNN realn number of nodes']) / n_nodes

    h_deg['Laplacian'][p] = results['Laplacian Harmonic Modified']
    h_deg['Geometric'][p] = results['Geometric Harmonic Modified']
    h_deg['GNN'][p] = np.array(results['GNN DATA']).reshape(-1, 6)[:, measures_ids['Harmonic degree']]

    c_deg['Laplacian'][p] = results['Laplacian Conformal Modified']
    c_deg['Geometric'][p] = results['Geometric Conformal Modified']
    c_deg['GNN'][p] = np.array(results['GNN DATA']).reshape(-1, 6)[:, measures_ids['Conformal degree']]

print(f"Loaded {len(net_list)} networks: {net_list}")
```

**Cell 4 (code):**
```python
def interpolate_and_average(compressions, metric_deg, model_names, net_list):
    """Interpolate all networks to common compression axis, compute mean±std."""
    compression_axis = np.linspace(0, 1, 100, endpoint=True)
    interpolated = {m: [] for m in model_names}

    for model in model_names:
        for net in net_list:
            comp = compressions[model][net]
            vals = metric_deg[model][net]
            if model == "GNN":
                sort_id = np.argsort(comp)
                vals = vals[sort_id]
                comp = np.sort(comp)
            f_interp = interp1d(comp, vals, kind='linear', fill_value='extrapolate')
            interpolated[model].append(f_interp(compression_axis))

    arrays = {m: np.array(interpolated[m]) for m in model_names}
    means = {m: arrays[m].mean(axis=0) for m in model_names}
    stds = {m: arrays[m].std(axis=0) for m in model_names}
    return compression_axis, arrays, means, stds
```

**Cell 5 (markdown):**
```markdown
## Figure 2d: Average harmonic degree vs compression
```

**Cell 6 (code):**
```python
compression_axis, h_arrays, h_means, h_stds = interpolate_and_average(
    compressions, h_deg, model_names, net_list
)

fig, ax = plt.subplots(figsize=(7, 3.5))
for i, model in enumerate(model_names):
    if model == "Geometric":
        mid = len(compression_axis) // 2
        ax.plot(compression_axis[mid:], h_means[model][mid:],
                '-o', color=model_colors[i], label=model, linewidth=2, markersize=3)
        ax.fill_between(compression_axis[mid:],
                        h_means[model][mid:] - h_stds[model][mid:],
                        h_means[model][mid:] + h_stds[model][mid:],
                        color=model_colors[i], alpha=0.2)
    else:
        ax.plot(compression_axis, h_means[model],
                '-o', color=model_colors[i], label=model, linewidth=2, markersize=3)
        ax.fill_between(compression_axis,
                        h_means[model] - h_stds[model],
                        h_means[model] + h_stds[model],
                        color=model_colors[i], alpha=0.2)

ax.vlines(0.5, 0, 1, color="gray", linestyles="dashed", alpha=0.2)
ax.set_xlabel("Compression")
ax.set_ylabel("Harmonic Degree")
ax.set_title("Average Harmonic Degree vs Compression")
ax.legend(ncols=1, bbox_to_anchor=(1, 0.4))
ax.set_ylim([-0.05, 1.05])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
fig.savefig("fig02d_average_harmonic.pdf", bbox_inches="tight")
plt.show()
```

**Cell 7 (markdown):**
```markdown
## Figure 2e: Average conformal degree vs compression
```

**Cell 8 (code):**
```python
compression_axis, c_arrays, c_means, c_stds = interpolate_and_average(
    compressions, c_deg, model_names, net_list
)

fig, ax = plt.subplots(figsize=(7, 3.5))
for i, model in enumerate(model_names):
    if model == "Geometric":
        mid = len(compression_axis) // 2
        ax.plot(compression_axis[mid:], c_means[model][mid:],
                '-o', color=model_colors[i], label=model, linewidth=2, markersize=3)
        ax.fill_between(compression_axis[mid:],
                        c_means[model][mid:] - c_stds[model][mid:],
                        c_means[model][mid:] + c_stds[model][mid:],
                        color=model_colors[i], alpha=0.2)
    else:
        ax.plot(compression_axis, c_means[model],
                '-o', color=model_colors[i], label=model, linewidth=2, markersize=3)
        ax.fill_between(compression_axis,
                        c_means[model] - c_stds[model],
                        c_means[model] + c_stds[model],
                        color=model_colors[i], alpha=0.2)

ax.vlines(0.5, 0, 1, color="gray", linestyles="dashed", alpha=0.2)
ax.set_xlabel("Compression")
ax.set_ylabel("Conformal Degree")
ax.set_title("Average Conformal Degree vs Compression")
ax.legend(ncols=1, bbox_to_anchor=(1, 0.4))
ax.set_ylim([-0.05, 1.05])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
fig.savefig("fig02e_average_conformal.pdf", bbox_inches="tight")
plt.show()
```

**Cell 9 (markdown):**
```markdown
## Figure 7: Per-network harmonic degree curves (4x4 grid)
```

**Cell 10 (code):**
```python
n_nets = len(net_list)
n_cols = 4
n_rows = (n_nets + n_cols - 1) // n_cols

fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 3.5 * n_rows), sharex=True, sharey=True)
axes = axes.flatten()

for idx, net in enumerate(net_list):
    ax = axes[idx]
    net_name = net.replace("_results.pkl", "")
    for i, model in enumerate(model_names):
        comp = compressions[model][net]
        vals = h_deg[model][net]
        if model == "GNN":
            sort_id = np.argsort(comp)
            vals = vals[sort_id]
            comp = np.sort(comp)
        label = model if idx == 0 else None
        ax.plot(comp, vals, '-o', color=model_colors[i], label=label, linewidth=1.5, markersize=2)
    ax.set_title(net_name, fontsize=9)
    ax.set_ylim([-0.05, 1.05])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# Hide unused axes
for idx in range(n_nets, len(axes)):
    axes[idx].set_visible(False)

axes[0].legend(fontsize=8)
fig.supxlabel("Compression")
fig.supylabel("Modified Harmonic Degree")
fig.suptitle("Harmonic Degree vs Compression (all networks)", fontsize=BIGGER_SIZE)
plt.tight_layout(rect=[0.02, 0.02, 1, 0.96])
fig.savefig("fig07_harmonic_all_networks.pdf", bbox_inches="tight")
plt.show()
```

**Cell 11 (markdown):**
```markdown
## Figure 8: Per-network conformal degree curves (4x4 grid)
```

**Cell 12 (code):**
```python
fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 3.5 * n_rows), sharex=True, sharey=True)
axes = axes.flatten()

for idx, net in enumerate(net_list):
    ax = axes[idx]
    net_name = net.replace("_results.pkl", "")
    for i, model in enumerate(model_names):
        comp = compressions[model][net]
        vals = c_deg[model][net]
        if model == "GNN":
            sort_id = np.argsort(comp)
            vals = vals[sort_id]
            comp = np.sort(comp)
        label = model if idx == 0 else None
        ax.plot(comp, vals, '-o', color=model_colors[i], label=label, linewidth=1.5, markersize=2)
    ax.set_title(net_name, fontsize=9)
    ax.set_ylim([-0.05, 1.05])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

for idx in range(n_nets, len(axes)):
    axes[idx].set_visible(False)

axes[0].legend(fontsize=8)
fig.supxlabel("Compression")
fig.supylabel("Modified Conformal Degree")
fig.suptitle("Conformal Degree vs Compression (all networks)", fontsize=BIGGER_SIZE)
plt.tight_layout(rect=[0.02, 0.02, 1, 0.96])
fig.savefig("fig08_conformal_all_networks.pdf", bbox_inches="tight")
plt.show()
```

- [ ] **Step 2: Test notebook runs**

```bash
cd harmonic_morphisms/notebooks && jupyter nbconvert --to notebook --execute 02_average_curves.ipynb --output /dev/null 2>&1 && echo "Notebook 02 OK" && cd ../..
```

Expected: `Notebook 02 OK`

- [ ] **Step 3: Commit**

```bash
git add harmonic_morphisms/notebooks/02_average_curves.ipynb
git commit -m "feat: add notebook 02 (average curves, Figures 2d-e, 7, 8)"
```

---

### Task 9: Notebook 03 — Individual Laplacian RG (Figures 12, 13, 14)

**Files:**
- Create: `harmonic_morphisms/notebooks/03_individual_laplacian.ipynb`

Runs Laplacian RG on NetSci, Facebook, and C.Elegans networks. For each: harmonic degree curves + visualization at a characteristic time.

- [ ] **Step 1: Create notebook**

Create `harmonic_morphisms/notebooks/03_individual_laplacian.ipynb` with these cells:

**Cell 1 (markdown):**
```markdown
# Notebook 03: Individual Network Laplacian Renormalization
Reproduces **Figure 12** (NetSci), **Figure 13** (Facebook), **Figure 14** (C.Elegans) — Laplacian renormalization with harmonic/conformal degree curves and coarse-grained visualizations.
```

**Cell 2 (code):**
```python
%matplotlib inline
from pathlib import Path
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from harmonic_morphisms import H_CF_curves, renorm_graph_harmonic, g_len
from harmonic_morphisms.core import renorm_graph_plot
from harmonic_morphisms.simplicial import import_network_data

DATA_DIR = Path("../data")

SMALL_SIZE = 10
MEDIUM_SIZE = 12
BIGGER_SIZE = 13
plt.rc("font", size=SMALL_SIZE)
plt.rc("axes", titlesize=SMALL_SIZE)
plt.rc("axes", labelsize=MEDIUM_SIZE)
plt.rc("xtick", labelsize=SMALL_SIZE)
plt.rc("ytick", labelsize=SMALL_SIZE)
plt.rc("legend", fontsize=SMALL_SIZE)
plt.rc("figure", titlesize=BIGGER_SIZE)
```

**Cell 3 (code):**
```python
# Network configurations: (filename, display_name, threshold, viz_time, figure_num)
networks = [
    ("out.dimacs10-netscience", "NetSci Collaboration", pow(10, -3), 1, 12),
    ("out.ego-facebook", "Facebook", pow(10, -3), 1.95, 13),
    ("out.dimacs10-celegans_metabolic", "C. Elegans", pow(10, -3), 1, 14),
]
```

**Cell 4 (code):**
```python
for filename, name, tresh, viz_t, fig_num in networks:
    print(f"\n{'='*60}")
    print(f"Figure {fig_num}: {name}")
    print(f"{'='*60}")

    # Load network
    f = open(DATA_DIR / "networks" / filename)
    Ag = import_network_data(f)
    print(f"N={Ag.number_of_nodes()}, E={Ag.number_of_edges()}")

    # Compute Laplacian
    L0 = nx.laplacian_matrix(Ag, nodelist=Ag.nodes()).todense()

    # Run H_CF_curves
    g, DEG_H, M_DEG_H, STD_H, AV_H, STD_V_H, NOT_H, \
        DEG_CF, M_DEG_CF, STD_CF, AV_CF, STD_V_CF, NOT_CF, \
        gV, t_h = H_CF_curves(Ag, L0, 100, tresh)

    compression = 1 - np.array(g_len(g)) / len(Ag.nodes())

    # Plot 1: Compression vs harmonic degree curves
    f_fig = plt.figure(figsize=(10, 5))
    plt.plot(compression, M_DEG_H, "ob--", label="H Mod.")
    plt.plot(compression, M_DEG_CF, "og--", label="CF Mod.")
    plt.plot(compression, STD_H, "ok--", label="STD H")
    plt.xlabel("Compression")
    plt.ylabel("H/CF degree")
    plt.title(f"{name}", fontsize=15, fontweight="bold")
    plt.legend()
    plt.ylim([-0.1, 1.2])
    plt.grid(alpha=0.3)
    plt.tight_layout()
    f_fig.savefig(f"fig{fig_num:02d}_{filename.split('.')[-1]}_curves.pdf", bbox_inches="tight")
    plt.show()

    # Plot 2: Visualization at characteristic time
    G, deg_h, M_deg_h, std_h, av_h, std_v_h, Not_h, \
        deg_cf, M_deg_cf, std_cf, av_cf, std_v_cf, Not_cf, Gv = \
        renorm_graph_harmonic(Ag, viz_t, L0, tresh)

    Values = [deg_h, M_deg_h, std_h, deg_cf, M_deg_cf, std_cf]
    Labels = ["H", "Mod. H", "Std. H", "CF", "Mod. CF", "Std. CF"]
    df = pd.DataFrame([Values], columns=Labels)
    print(df.to_string(index=False))

    G_plot, colors_d, sing_col = renorm_graph_plot(Ag, viz_t, L0, tresh)
    colors = [colors_d[n] for n in Ag.nodes()]
    layout = nx.spring_layout(Ag, iterations=100, seed=42)
    lay2 = nx.spring_layout(G_plot, iterations=100, seed=42)

    f_viz, ax = plt.subplots(1, 2, figsize=(12, 6))

    nodes = nx.draw_networkx_nodes(Ag, ax=ax[0], pos=layout, node_color=colors, node_size=50)
    nodes.set_edgecolor("white")
    nx.draw_networkx_edges(Ag, ax=ax[0], pos=layout, width=0.8)
    ax[0].collections[0].set_linewidth(0.6)
    ax[0].collections[0].set_edgecolor("#FFFFFF")
    ax[0].set_title("Clustering")
    ax[0].axis("off")

    nodes_2 = nx.draw_networkx_nodes(G_plot, ax=ax[1], pos=lay2, node_color=sing_col, node_size=200)
    nodes_2.set_edgecolor("white")
    nx.draw_networkx_edges(G_plot, ax=ax[1], pos=lay2, width=1.8)
    ax[1].collections[0].set_linewidth(0.6)
    ax[1].collections[0].set_edgecolor("#FFFFFF")
    ax[1].set_title("Coarse-grained")
    ax[1].axis("off")

    eta = 1 - len(G_plot.nodes()) / len(Ag.nodes())
    f_viz.suptitle(f"{name} — Laplacian RG at t={viz_t} (η={eta:.2f})", fontsize=14, fontweight="bold")
    plt.tight_layout()
    f_viz.savefig(f"fig{fig_num:02d}_{filename.split('.')[-1]}_viz.pdf", bbox_inches="tight")
    plt.show()
```

- [ ] **Step 2: Test notebook runs**

```bash
cd harmonic_morphisms/notebooks && jupyter nbconvert --to notebook --execute 03_individual_laplacian.ipynb --output /dev/null 2>&1 && echo "Notebook 03 OK" && cd ../..
```

Expected: `Notebook 03 OK` (may take several minutes — 3 networks × H_CF_curves)

- [ ] **Step 3: Commit**

```bash
git add harmonic_morphisms/notebooks/03_individual_laplacian.ipynb
git commit -m "feat: add notebook 03 (individual Laplacian RG, Figures 12-14)"
```

---

### Task 10: Notebook 04 — Higher-order synthetic (Figures 4, 17, 18)

**Files:**
- Create: `harmonic_morphisms/notebooks/04_higher_order_synthetic.ipynb`

Generates pseudofractal d2/d3 simplicial complexes, computes Hodge/Bochner/XO Laplacians, runs higher-order H_CF_curves.

- [ ] **Step 1: Create notebook**

Create `harmonic_morphisms/notebooks/04_higher_order_synthetic.ipynb` with these cells:

**Cell 1 (markdown):**
```markdown
# Notebook 04: Higher-Order Renormalization on Synthetic Simplicial Complexes
Reproduces **Figure 4** (Pseudofractal d2 spectral/harmonic panel), **Figure 17** (Pseudofractal d2 renormalization), and **Figure 18** (Pseudofractal d3 renormalization).
```

**Cell 2 (code):**
```python
%matplotlib inline
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from harmonic_morphisms import g_len, higher_order_H_CF_curves, fbc
from harmonic_morphisms.simplicial import (
    pseudofractal_d2, pseudofractal_d3, laplacians,
    XO_laplacian, compute_entropic_C, compute_spectral_d, plot_complex,
)
from harmonic_morphisms.higher_order import higher_order_renormalization

SMALL_SIZE = 10
MEDIUM_SIZE = 12
BIGGER_SIZE = 13
plt.rc("font", size=SMALL_SIZE)
plt.rc("axes", titlesize=SMALL_SIZE)
plt.rc("axes", labelsize=MEDIUM_SIZE)
plt.rc("xtick", labelsize=SMALL_SIZE)
plt.rc("ytick", labelsize=SMALL_SIZE)
plt.rc("legend", fontsize=SMALL_SIZE)
plt.rc("figure", titlesize=BIGGER_SIZE)
```

**Cell 3 (markdown):**
```markdown
## Pseudofractal d=2 (3 iterations)
```

**Cell 4 (code):**
```python
sc = pseudofractal_d2(3)
print(f"Pseudofractal d2: n0={sc['n0']}, n1={sc['n1']}, n2={sc['n2']}")

# Compute all Laplacians
L0, L1, L2, L3, L4, node_dict, edge_dict, face_dict, tet_dict = laplacians(sc)
B2, F2 = fbc(L2)       # Bochner decomposition
X2 = XO_laplacian(sc, 2, 1)  # Cross-order Laplacian

# Eigenvalues
e2, ev2 = np.linalg.eigh(L2)
eb2, evb2 = np.linalg.eigh(B2)
ex2, evx2 = np.linalg.eigh(X2)
```

**Cell 5 (markdown):**
```markdown
## Figure 4: Spectral properties and harmonic degree (Pseudofractal d2)
```

**Cell 6 (code):**
```python
# Spectral quantities
exm, exM, n_t = -2, 5, 1000
c2, t2, s2 = compute_entropic_C(e2, exm, exM, n_t)
cb2, tb2, sb2 = compute_entropic_C(eb2, exm, exM, n_t)
cx2, tx2, sx2 = compute_entropic_C(ex2, exm, exM, n_t)

sd2, ts2 = compute_spectral_d(e2, exm, exM, n_t)
sdb2, tsb2 = compute_spectral_d(eb2, exm, exM, n_t)
sdx2, tsx2 = compute_spectral_d(ex2, exm, exM, n_t)

# Harmonic degree curves for each operator
Ag_h, g_h, DEG_H_h, M_DEG_H_h, STD_H_h, AV_H_h, STD_V_H_h, NOT_H_h, \
    DEG_CF_h, M_DEG_CF_h, STD_CF_h, AV_CF_h, STD_V_CF_h, NOT_CF_h, \
    gV_h, t_span_h = higher_order_H_CF_curves(sc, n=100, dim=2, Lap=L2)

Ag_b, g_b, DEG_H_b, M_DEG_H_b, STD_H_b, AV_H_b, STD_V_H_b, NOT_H_b, \
    DEG_CF_b, M_DEG_CF_b, STD_CF_b, AV_CF_b, STD_V_CF_b, NOT_CF_b, \
    gV_b, t_span_b = higher_order_H_CF_curves(sc, n=100, dim=2, Lap=B2)

Ag_x, g_x, DEG_H_x, M_DEG_H_x, STD_H_x, AV_H_x, STD_V_H_x, NOT_H_x, \
    DEG_CF_x, M_DEG_CF_x, STD_CF_x, AV_CF_x, STD_V_CF_x, NOT_CF_x, \
    gV_x, t_span_x = higher_order_H_CF_curves(sc, n=100, dim=2, Lap=X2)
```

**Cell 7 (code):**
```python
f, ax = plt.subplots(2, 3, figsize=(10, 5))
ax = ax.flatten()

# Row 0: Spectral quantities
ax[0].loglog(t2, c2, "r", linewidth=3.5)
ax[0].loglog(tb2, cb2, '#FF8605', linewidth=3.5)
ax[0].loglog(tx2, cx2, '#0291F7', linewidth=3.5)
ax[0].set_ylabel("C")
ax[0].set_ylim([pow(10, -1), 10])
ax[0].legend(["Hodge-2", "Bochner-2", "XO-2"], loc="best")
ax[0].set_title("Entropic Susceptibility")

ax[1].loglog(t2, s2[1:], "r", linewidth=3.5)
ax[1].loglog(tb2, sb2[1:], '#FF8605', linewidth=3.5)
ax[1].loglog(tx2, sx2[1:], '#0291F7', linewidth=3.5)
ax[1].set_ylabel("S")
ax[1].legend(["Hodge-2", "Bochner-2", "XO-2"], loc="best")
ax[1].set_title("Entropy")

ax[2].loglog(ts2, sd2, "r", linewidth=3.5)
ax[2].loglog(tsb2, sdb2, '#FF8605', linewidth=3.5)
ax[2].loglog(tsx2, sdx2, '#0291F7', linewidth=3.5)
ax[2].set_ylabel("$d_S$")
ax[2].legend(["Hodge-2", "Bochner-2", "XO-2"], loc="best")
ax[2].set_title("Spectral Dimension")

# Row 1: Harmonic degree curves
for j, (t_span, M_H, M_CF, STD, title) in enumerate([
    (t_span_h, M_DEG_H_h, M_DEG_CF_h, STD_H_h, "Hodge L2"),
    (t_span_b, M_DEG_H_b, M_DEG_CF_b, STD_H_b, "Bochner B2"),
    (t_span_x, M_DEG_H_x, M_DEG_CF_x, STD_H_x, "XO X2"),
]):
    ax[3 + j].plot(t_span, M_H, 'b', linewidth=2.5)
    ax[3 + j].plot(t_span, M_CF, 'g', linewidth=2.5)
    ax[3 + j].plot(t_span, STD, 'k', linewidth=2.5)
    ax[3 + j].set_title(f"{title} Harm/CF degree")
    ax[3 + j].set_ylabel("Degree")
    ax[3 + j].legend(["H Mod.", "CF Mod.", "STD H"])
    ax[3 + j].set_ylim([-0.05, 1.2])
    ax[3 + j].set_xlabel("time")

plt.tight_layout()
f.savefig("fig04_pf2_panel.pdf", bbox_inches="tight")
plt.show()
```

**Cell 8 (markdown):**
```markdown
## Figure 17: Compression curves (Pseudofractal d2)
```

**Cell 9 (code):**
```python
l_h = 1 - np.array(g_len(g_h)) / len(Ag_h.nodes())
l_b = 1 - np.array(g_len(g_b)) / len(Ag_b.nodes())
l_x = 1 - np.array(g_len(g_x)) / len(Ag_x.nodes())

f, ax = plt.subplots(1, 3, figsize=(15, 5))

for j, (comp, M_H, M_CF, STD, title) in enumerate([
    (l_h, M_DEG_H_h, M_DEG_CF_h, STD_H_h, "Hodge-2"),
    (l_b, M_DEG_H_b, M_DEG_CF_b, STD_H_b, "Bochner-2"),
    (l_x, M_DEG_H_x, M_DEG_CF_x, STD_H_x, "XO-2"),
]):
    ax[j].plot(comp, M_H, "ob--")
    ax[j].plot(comp, M_CF, "og--")
    ax[j].plot(comp, STD, "ok--")
    ax[j].set_xlabel("Compression")
    ax[j].set_ylabel("H/CF degree")
    ax[j].set_title(f"{title} vs Compression", size=15)
    ax[j].legend(["H Mod.", "CF Mod.", "STD H"], loc="best")
    ax[j].set_ylim([-0.1, 1.2])
    ax[j].grid(alpha=0.3)

plt.tight_layout()
f.savefig("fig17_pf2_compression.pdf", bbox_inches="tight")
plt.show()
```

**Cell 10 (markdown):**
```markdown
## Figure 18: Pseudofractal d=3
```

**Cell 11 (code):**
```python
sc3 = pseudofractal_d3(2)
print(f"Pseudofractal d3: n0={sc3['n0']}, n1={sc3['n1']}, n2={sc3['n2']}, n3={sc3['n3']}")

L0_3, L1_3, L2_3, L3_3, L4_3, _, _, _, _ = laplacians(sc3)

# Dim 2 analysis on the d3 complex
B2_3, F2_3 = fbc(L2_3)
X2_3 = XO_laplacian(sc3, 2, 1)

Ag_h3, g_h3, _, M_DEG_H_h3, STD_H_h3, _, _, _, _, M_DEG_CF_h3, STD_CF_h3, \
    _, _, _, gV_h3, t_span_h3 = higher_order_H_CF_curves(sc3, n=100, dim=2, Lap=L2_3)
Ag_b3, g_b3, _, M_DEG_H_b3, STD_H_b3, _, _, _, _, M_DEG_CF_b3, STD_CF_b3, \
    _, _, _, gV_b3, t_span_b3 = higher_order_H_CF_curves(sc3, n=100, dim=2, Lap=B2_3)
Ag_x3, g_x3, _, M_DEG_H_x3, STD_H_x3, _, _, _, _, M_DEG_CF_x3, STD_CF_x3, \
    _, _, _, gV_x3, t_span_x3 = higher_order_H_CF_curves(sc3, n=100, dim=2, Lap=X2_3)

l_h3 = 1 - np.array(g_len(g_h3)) / len(Ag_h3.nodes())
l_b3 = 1 - np.array(g_len(g_b3)) / len(Ag_b3.nodes())
l_x3 = 1 - np.array(g_len(g_x3)) / len(Ag_x3.nodes())

f, ax = plt.subplots(1, 3, figsize=(15, 5))
for j, (comp, M_H, M_CF, STD, title) in enumerate([
    (l_h3, M_DEG_H_h3, M_DEG_CF_h3, STD_H_h3, "Hodge-2 (d3)"),
    (l_b3, M_DEG_H_b3, M_DEG_CF_b3, STD_H_b3, "Bochner-2 (d3)"),
    (l_x3, M_DEG_H_x3, M_DEG_CF_x3, STD_H_x3, "XO-2 (d3)"),
]):
    ax[j].plot(comp, M_H, "ob--")
    ax[j].plot(comp, M_CF, "og--")
    ax[j].plot(comp, STD, "ok--")
    ax[j].set_xlabel("Compression")
    ax[j].set_ylabel("H/CF degree")
    ax[j].set_title(f"{title} vs Compression", size=15)
    ax[j].legend(["H Mod.", "CF Mod.", "STD H"], loc="best")
    ax[j].set_ylim([-0.1, 1.2])
    ax[j].grid(alpha=0.3)

plt.suptitle("Pseudofractal d=3", fontsize=BIGGER_SIZE)
plt.tight_layout()
f.savefig("fig18_pf3_compression.pdf", bbox_inches="tight")
plt.show()
```

- [ ] **Step 2: Test notebook runs**

```bash
cd harmonic_morphisms/notebooks && jupyter nbconvert --to notebook --execute 04_higher_order_synthetic.ipynb --ExecutePreprocessor.timeout=600 --output /dev/null 2>&1 && echo "Notebook 04 OK" && cd ../..
```

Expected: `Notebook 04 OK` (may take several minutes for higher_order_H_CF_curves)

- [ ] **Step 3: Commit**

```bash
git add harmonic_morphisms/notebooks/04_higher_order_synthetic.ipynb
git commit -m "feat: add notebook 04 (higher-order synthetic, Figures 4, 17, 18)"
```

---

### Task 11: Notebook 05 — Higher-order real (Figure 19)

**Files:**
- Create: `harmonic_morphisms/notebooks/05_higher_order_real.ipynb`

Loads Thiers13 simplicial complex from JSON, runs higher-order RG.

- [ ] **Step 1: Create notebook**

Create `harmonic_morphisms/notebooks/05_higher_order_real.ipynb` with these cells:

**Cell 1 (markdown):**
```markdown
# Notebook 05: Higher-Order Renormalization on Real Simplicial Complexes
Reproduces **Figure 19** (Thiers13 simplicial complex — Hodge Laplacian renormalization on 2-faces).
```

**Cell 2 (code):**
```python
%matplotlib inline
import json
from pathlib import Path
from itertools import combinations
from collections import defaultdict
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from harmonic_morphisms import g_len, higher_order_H_CF_curves, fbc
from harmonic_morphisms.simplicial import laplacians, XO_laplacian, compute_entropic_C, compute_spectral_d

DATA_DIR = Path("../data")

SMALL_SIZE = 10
MEDIUM_SIZE = 12
BIGGER_SIZE = 13
plt.rc("font", size=SMALL_SIZE)
plt.rc("axes", titlesize=SMALL_SIZE)
plt.rc("axes", labelsize=MEDIUM_SIZE)
plt.rc("xtick", labelsize=SMALL_SIZE)
plt.rc("ytick", labelsize=SMALL_SIZE)
plt.rc("legend", fontsize=SMALL_SIZE)
plt.rc("figure", titlesize=BIGGER_SIZE)
```

**Cell 3 (code):**
```python
# Load Thiers13 simplicial complex from JSON
with open(DATA_DIR / "networks" / "random_10_0.85min_cliques_Thiers13.json", 'r') as f:
    doc = json.load(f)

simplices = doc[0]

nodes_set = set()
edges_set = set()
faces_set = set()

for simplex in simplices:
    for v in simplex:
        nodes_set.add(v)
    length = len(simplex)
    if length == 2:
        edges_set.add(tuple(sorted(simplex)))
    elif length == 3:
        face = tuple(sorted(simplex))
        faces_set.add(face)
        for edge in combinations(face, 2):
            edges_set.add(tuple(sorted(edge)))

# Remap nodes to 0..N-1
sorted_nodes = sorted(nodes_set)
node_mapping = {old: new for new, old in enumerate(sorted_nodes)}

def remap(simplices_list):
    return [sorted([node_mapping[v] for v in s]) for s in simplices_list]

edges = np.array(remap(list(edges_set)))
faces = np.array(remap(list(faces_set)))
nodes = np.array([[i] for i in range(len(sorted_nodes))])

# Extract largest connected component of faces
def build_face_adjacency(faces):
    edge_to_faces = defaultdict(set)
    for idx, face in enumerate(faces):
        for edge in combinations(sorted(face), 2):
            edge_to_faces[edge].add(idx)
    G = nx.Graph()
    G.add_nodes_from(range(len(faces)))
    for face_indices in edge_to_faces.values():
        face_list = list(face_indices)
        for i in range(len(face_list)):
            for j in range(i + 1, len(face_list)):
                G.add_edge(face_list[i], face_list[j])
    return G

G_adj = build_face_adjacency(faces)
largest_cc = max(nx.connected_components(G_adj), key=len)
faces = faces[list(largest_cc)]

sc = {
    'nodes': nodes, 'n0': len(nodes),
    'edges': edges, 'n1': len(edges),
    'faces': faces, 'n2': len(faces),
    'tetrahedra': np.zeros((0, 4), dtype=int), 'n3': 0,
    '4-simplices': np.zeros((0, 5), dtype=int), 'n4': 0,
}
print(f"Thiers13: n0={sc['n0']}, n1={sc['n1']}, n2={sc['n2']}")
```

**Cell 4 (markdown):**
```markdown
## Figure 19: Thiers13 higher-order renormalization
```

**Cell 5 (code):**
```python
# Compute Laplacians
L0, L1, L2, L3, L4, node_dict, edge_dict, face_dict, tet_dict = laplacians(sc)
B2, F2 = fbc(L2)
X2 = XO_laplacian(sc, 2, 1)

# Harmonic degree curves for each operator
Ag_h, g_h, _, M_DEG_H_h, STD_H_h, _, _, _, _, M_DEG_CF_h, STD_CF_h, \
    _, _, _, gV_h, t_span_h = higher_order_H_CF_curves(sc, n=100, dim=2, Lap=L2)
Ag_b, g_b, _, M_DEG_H_b, STD_H_b, _, _, _, _, M_DEG_CF_b, STD_CF_b, \
    _, _, _, gV_b, t_span_b = higher_order_H_CF_curves(sc, n=100, dim=2, Lap=B2)
Ag_x, g_x, _, M_DEG_H_x, STD_H_x, _, _, _, _, M_DEG_CF_x, STD_CF_x, \
    _, _, _, gV_x, t_span_x = higher_order_H_CF_curves(sc, n=100, dim=2, Lap=X2)

l_h = 1 - np.array(g_len(g_h)) / len(Ag_h.nodes())
l_b = 1 - np.array(g_len(g_b)) / len(Ag_b.nodes())
l_x = 1 - np.array(g_len(g_x)) / len(Ag_x.nodes())
```

**Cell 6 (code):**
```python
f, ax = plt.subplots(1, 3, figsize=(15, 5))
for j, (comp, M_H, M_CF, STD, title) in enumerate([
    (l_h, M_DEG_H_h, M_DEG_CF_h, STD_H_h, "Hodge-2"),
    (l_b, M_DEG_H_b, M_DEG_CF_b, STD_H_b, "Bochner-2"),
    (l_x, M_DEG_H_x, M_DEG_CF_x, STD_H_x, "XO-2"),
]):
    ax[j].plot(comp, M_H, "ob--")
    ax[j].plot(comp, M_CF, "og--")
    ax[j].plot(comp, STD, "ok--")
    ax[j].set_xlabel("Compression")
    ax[j].set_ylabel("H/CF degree")
    ax[j].set_title(f"Thiers13 {title}", size=15)
    ax[j].legend(["H Mod.", "CF Mod.", "STD H"], loc="best")
    ax[j].set_ylim([-0.1, 1.2])
    ax[j].grid(alpha=0.3)

plt.suptitle("Thiers13 Simplicial Complex", fontsize=BIGGER_SIZE)
plt.tight_layout()
f.savefig("fig19_thiers13.pdf", bbox_inches="tight")
plt.show()
```

- [ ] **Step 2: Test notebook runs**

```bash
cd harmonic_morphisms/notebooks && jupyter nbconvert --to notebook --execute 05_higher_order_real.ipynb --ExecutePreprocessor.timeout=600 --output /dev/null 2>&1 && echo "Notebook 05 OK" && cd ../..
```

Expected: `Notebook 05 OK`

- [ ] **Step 3: Commit**

```bash
git add harmonic_morphisms/notebooks/05_higher_order_real.ipynb
git commit -m "feat: add notebook 05 (higher-order real, Figure 19)"
```

---

### Task 12: Notebook 06 — Equilibrium Laplacian RG (Figure 16)

**Files:**
- Create: `harmonic_morphisms/notebooks/06_equilibrium_laplacian.ipynb`

Implements the equilibrium Laplacian RG variant (entropy-based merging) and applies to NetSci, C.Elegans, Tortoise. The functions `renorm_graph_harmonic_eq` and `H_CF_curves_eq` are defined inline since they're not in the core library.

- [ ] **Step 1: Create notebook**

Create `harmonic_morphisms/notebooks/06_equilibrium_laplacian.ipynb` with these cells:

**Cell 1 (markdown):**
```markdown
# Notebook 06: Equilibrium Laplacian Renormalization
Reproduces **Figure 16** — Equilibrium Laplacian renormalization on NetSci, C.Elegans, and Tortoise networks. Uses entropy-based merging criterion instead of time-parametrized diffusion.
```

**Cell 2 (code):**
```python
%matplotlib inline
from pathlib import Path
import numpy as np
import scipy.linalg
import networkx as nx
import matplotlib.pyplot as plt

from harmonic_morphisms import H_CF_cluster
from harmonic_morphisms.simplicial import import_network_data, compute_entropic_C

DATA_DIR = Path("../data")

SMALL_SIZE = 10
MEDIUM_SIZE = 12
BIGGER_SIZE = 13
plt.rc("font", size=SMALL_SIZE)
plt.rc("axes", titlesize=SMALL_SIZE)
plt.rc("axes", labelsize=MEDIUM_SIZE)
plt.rc("xtick", labelsize=SMALL_SIZE)
plt.rc("ytick", labelsize=SMALL_SIZE)
plt.rc("legend", fontsize=SMALL_SIZE)
plt.rc("figure", titlesize=BIGGER_SIZE)
```

**Cell 3 (code):**
```python
def renorm_graph_harmonic_eq(Ag, t_e, se, fraction, Lap, kappa=1):
    """Equilibrium Laplacian renormalization at a given compression fraction."""
    N = len(Ag.nodes())
    target_value = np.log((1 - kappa * fraction) * N)
    t_index = np.argmin(np.abs(se - target_value))
    t = t_e[t_index]

    rho = scipy.linalg.expm(-t * Lap)
    node_list = list(Ag.nodes())
    pair_metrics = []
    for i in range(N):
        for j in range(i + 1, N):
            metric = (rho[i, j] * rho[j, i]) / (rho[i, i] * rho[j, j])
            pair_metrics.append((metric, i, j))
    pair_metrics.sort(reverse=True, key=lambda x: x[0])

    Gv = nx.Graph()
    Gv.add_nodes_from(node_list)
    target_components = int((1 - fraction) * N)
    for metric, i, j in pair_metrics:
        Gv.add_edge(node_list[i], node_list[j])
        if nx.number_connected_components(Gv) <= target_components:
            break

    idx_components = {u: ci for ci, node_set in enumerate(nx.connected_components(Gv)) for u in node_set}
    clusters = {node: idx_components[node] for node in Gv.nodes()}

    G, deg_h, M_deg_h, std_h, av_h, std_v_h, Not_h, \
        deg_cf, M_deg_cf, std_cf, av_cf, std_v_cf, Not_cf = H_CF_cluster(Ag, clusters)
    return G, deg_h, M_deg_h, std_h, av_h, std_v_h, Not_h, \
        deg_cf, M_deg_cf, std_cf, av_cf, std_v_cf, Not_cf, Gv


def H_CF_curves_eq(Ag, t_e, se, n_f, Lap, kappa=1, stability=True):
    """Sweep compression fractions for equilibrium Laplacian RG."""
    g, M_DEG_H, M_DEG_CF, STD_H = [], [], [], []
    interval = np.linspace(0, 1, n_f)
    if stability:
        interval = interval[1:-1]

    for fraction in interval:
        G, _, M_deg_h, std_h, _, _, _, _, M_deg_cf, _, _, _, _, _ = \
            renorm_graph_harmonic_eq(Ag, t_e, se, fraction, Lap, kappa=kappa)
        g.append(G)
        M_DEG_H.append(M_deg_h)
        M_DEG_CF.append(M_deg_cf)
        STD_H.append(std_h)

    return g, M_DEG_H, M_DEG_CF, STD_H, interval
```

**Cell 4 (code):**
```python
networks = [
    ("out.dimacs10-netscience", "NetSci Collaboration"),
    ("out.dimacs10-celegans_metabolic", "C. Elegans"),
    ("reptilia-tortoise-network-fi.edges", "Tortoise"),
]

exm, exM, n_t = -2, 3, 1000

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for idx, (filename, name) in enumerate(networks):
    print(f"Processing {name}...")
    f = open(DATA_DIR / "networks" / filename)
    Ag = import_network_data(f)
    print(f"  N={Ag.number_of_nodes()}, E={Ag.number_of_edges()}")

    L0 = np.array(nx.laplacian_matrix(Ag, nodelist=Ag.nodes()).todense())
    e, ev = np.linalg.eigh(L0)
    ce, t_e, se = compute_entropic_C(e, exm, exM, n_t)

    g, M_DEG_H, M_DEG_CF, STD_H, interval = H_CF_curves_eq(
        Ag, t_e, se, 50, L0, stability=False
    )

    ax = axes[idx]
    ax.plot(interval, M_DEG_H, "ob--", label="H Mod.")
    ax.plot(interval, M_DEG_CF, "og--", label="CF Mod.")
    ax.plot(interval, STD_H, "ok--", label="STD H")
    ax.set_xlabel("Compression fraction")
    ax.set_ylabel("H/CF degree")
    ax.set_title(name, fontsize=13, fontweight="bold")
    ax.legend()
    ax.set_ylim([-0.1, 1.2])
    ax.grid(alpha=0.3)

plt.suptitle("Equilibrium Laplacian Renormalization", fontsize=BIGGER_SIZE)
plt.tight_layout()
fig.savefig("fig16_equilibrium_laplacian.pdf", bbox_inches="tight")
plt.show()
```

- [ ] **Step 2: Test notebook runs**

```bash
cd harmonic_morphisms/notebooks && jupyter nbconvert --to notebook --execute 06_equilibrium_laplacian.ipynb --ExecutePreprocessor.timeout=600 --output /dev/null 2>&1 && echo "Notebook 06 OK" && cd ../..
```

Expected: `Notebook 06 OK`

- [ ] **Step 3: Commit**

```bash
git add harmonic_morphisms/notebooks/06_equilibrium_laplacian.ipynb
git commit -m "feat: add notebook 06 (equilibrium Laplacian RG, Figure 16)"
```

---

### Task 13: Documentation

**Files:**
- Create: `harmonic_morphisms/docs/quickstart.md`
- Create: `harmonic_morphisms/docs/api.md`
- Create: `harmonic_morphisms/docs/paper_figures.md`

- [ ] **Step 1: Write quickstart.md**

Create `harmonic_morphisms/docs/quickstart.md`:

```markdown
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
```

- [ ] **Step 2: Write api.md**

Create `harmonic_morphisms/docs/api.md`:

```markdown
# API Reference

## `harmonic_morphisms.core`

### Harmonic degree computation

**`H_CF_cluster(Ag, clusters)`**
Computes harmonic and conformal degrees for a given clustering.
- `Ag`: `networkx.Graph` — original graph
- `clusters`: `dict` — `{node_id: cluster_id}` mapping
- Returns: `(G, deg_h, M_deg_h, std_h, av_h, std_v_h, Not_h, deg_cf, M_deg_cf, std_cf, av_cf, std_v_cf, Not_cf)`

**`clust_plot(Ag, clusters)`**
Generates coarse-grained graph and color mappings for visualization.
- Returns: `(G, colors_dict, sing_col)`

### Laplacian renormalization

**`simple_renorm(Ag, t, Lap, tresh=0)`**
Single-step Laplacian renormalization at diffusion time `t`.
- Returns: `G` (coarse-grained graph)

**`renorm_graph_plot(Ag, t, Lap, tresh=0)`**
Renormalization with color mappings for plotting.
- Returns: `(G, colors_dict, sing_col)`

**`renorm_graph_harmonic(Ag, t, Lap, tresh=0)`**
Renormalization with harmonic/conformal degree computation.
- Returns: `(G, deg_h, M_deg_h, std_h, av_h, std_v_h, Not_h, deg_cf, M_deg_cf, std_cf, av_cf, std_v_cf, Not_cf, Gv)`

### Sweep functions

**`iter_g(Ag, Lap, tresh=0)`**
Find integer collapse time (where graph reduces to 1 node).

**`iter_narrow_g(Ag, Lap, tresh=0)`**
Refined collapse time with 0.1 precision.

**`h_v(Ag, t_span, Lap, tresh=0)`**
Compute harmonic/conformal degrees over a given array of `t` values.

**`H_CF_curves(Ag, Lap, n, tresh=0)`**
Auto-find collapse time, sweep `n` points, return all metric histories.

**`g_len(g)`**
Extract node counts from a list of graphs.

---

## `harmonic_morphisms.higher_order`

**`fbc(L)`**
Forman-Bochner decomposition of Laplacian `L` into Bochner (`B`) and curvature (`F`) parts.
- Returns: `(B, F)`

**`higher_order_renormalization(sc, t, dim, Lap, tresh=0)`**
Single-step Hodge Laplacian renormalization on `dim`-dimensional faces.
- Returns: `(Ag, G, deg_h, M_deg_h, std_h, av_h, std_v_h, Not_h, deg_cf, M_deg_cf, std_cf, av_cf, std_v_cf, Not_cf, Gv, sing_col, colors)`

**`higher_order_renormalization_series(sc, t_span, dim, Lap, tresh=0)`**
Sweep over time range.

**`iter_g_higher_order(sc, dim, Lap, tresh=0)`**
Find collapse time for higher-order renormalization.

**`iter_narrow_g_higher_order(sc, dim, Lap, tresh=0)`**
Refined collapse time (0.1 precision).

**`higher_order_H_CF_curves(sc, dim, Lap, n, tresh=0)`**
Auto-sweep for higher-order renormalization. Returns `(Ag, g, DEG_H, M_DEG_H, STD_H, ..., gV, t_span)`.

---

## `harmonic_morphisms.simplicial`

### Network I/O

**`import_network_data(f)`**
Parse edge list file, extract LCC, relabel nodes 0..N-1.
- `f`: file object (first line skipped as header)
- Returns: `networkx.Graph`

### Simplicial complex generators

**`NGF(d, N, s, beta, M=1)`** — Network Geometry with Flavor (d-dimensional)

**`pseudofractal_d2(steps)`** — Pseudofractal simplicial complex, d=2

**`pseudofractal_d3(steps)`** — Pseudofractal simplicial complex, d=3

**`apollonian_d2(steps)`** — Apollonian simplicial complex, d=2

**`pseudofractal_d2_graph(steps)`** — Pseudofractal as NetworkX graph (no SC structure)

**`apollonian_d2_graph(steps)`** — Apollonian as NetworkX graph

**`convert_graph_to_sc(G, dim=2, type='clique')`** — Convert graph to clique complex

### Algebraic topology

**`boundary_matrices_ext(sc)`** — Boundary matrices B1..B4 for up to 4-simplices.

**`laplacians(sc)`** — Hodge Laplacians L0..L4. Returns `(L0, L1, L2, L3, L4, node_dict, edge_dict, face_dict, tet_dict)`.

**`adjacency_of_order(sc, k, l, sparse=False)`** — k-order adjacency through l-simplices.

**`XO_laplacian(sc, k, l, sparse=False)`** — Cross-order Laplacian.

### Spectral analysis

**`compute_entropic_C(D, exm, exM, n_t)`** — Entropic susceptibility from eigenvalues.
- Returns: `(C, tau_space, S)`

**`compute_spectral_d(D, exm, exM, n_t)`** — Spectral dimension from eigenvalues.
- Returns: `(dS, tau_space)`

### Visualization

**`plot_complex(sc, ax, ...)`** — Draw simplicial complex with face/edge/node coloring.
```

- [ ] **Step 3: Write paper_figures.md**

Create `harmonic_morphisms/docs/paper_figures.md`:

```markdown
# Paper Figure → Notebook Map

Figures from *"Harmonic morphisms and dynamical invariants in network renormalization"* (PRX).

| Figure | Description | Notebook | Output file |
|--------|------------|----------|-------------|
| 2a | Euroroad Laplacian RG curves | `01_euroroad_laplacian.ipynb` | `fig02a_euroroad_laplacian.pdf` |
| 2d | Average harmonic degree | `02_average_curves.ipynb` | `fig02d_average_harmonic.pdf` |
| 2e | Average conformal degree | `02_average_curves.ipynb` | `fig02e_average_conformal.pdf` |
| 3 | Euroroad spatial deviation | `01_euroroad_laplacian.ipynb` | `fig03_euroroad_spatial.pdf` |
| 4 | Pseudofractal d2 spectral + harmonic panel | `04_higher_order_synthetic.ipynb` | `fig04_pf2_panel.pdf` |
| 7 | Harmonic degree, all 16 networks | `02_average_curves.ipynb` | `fig07_harmonic_all_networks.pdf` |
| 8 | Conformal degree, all 16 networks | `02_average_curves.ipynb` | `fig08_conformal_all_networks.pdf` |
| 12 | NetSci Laplacian RG | `03_individual_laplacian.ipynb` | `fig12_*.pdf` |
| 13 | Facebook Laplacian RG | `03_individual_laplacian.ipynb` | `fig13_*.pdf` |
| 14 | C.Elegans Laplacian RG | `03_individual_laplacian.ipynb` | `fig14_*.pdf` |
| 16 | Equilibrium Laplacian RG | `06_equilibrium_laplacian.ipynb` | `fig16_equilibrium_laplacian.pdf` |
| 17 | Pseudofractal d2 compression curves | `04_higher_order_synthetic.ipynb` | `fig17_pf2_compression.pdf` |
| 18 | Pseudofractal d3 compression curves | `04_higher_order_synthetic.ipynb` | `fig18_pf3_compression.pdf` |
| 19 | Thiers13 higher-order RG | `05_higher_order_real.ipynb` | `fig19_thiers13.pdf` |

### Figures not included

These figures require external tools not in the core dependencies:

| Figure | Reason |
|--------|--------|
| 2b-c | Geometric and GNN panels require d-mercator and torch_geometric |
| 5 | Clustering comparisons require graph_tool for SBM |
| 6 | UMAP embeddings require umap-learn and graph_tool |
| 9-11 | Geometric renormalization requires d-mercator |
| 15 | GNN renormalization requires torch_geometric |
```

- [ ] **Step 4: Commit**

```bash
git add harmonic_morphisms/docs/
git commit -m "feat: add documentation (quickstart, API reference, figure map)"
```

---

### Task 14: Final verification

- [ ] **Step 1: Clean install test**

```bash
cd harmonic_morphisms && pip install -e . && cd ..
python -c "
from harmonic_morphisms import H_CF_cluster, H_CF_curves, higher_order_H_CF_curves, __version__
from harmonic_morphisms.simplicial import pseudofractal_d2, laplacians, import_network_data, compute_entropic_C
from harmonic_morphisms.higher_order import fbc, higher_order_renormalization
from harmonic_morphisms.core import renorm_graph_harmonic, renorm_graph_plot, simple_renorm
print(f'harmonic_morphisms v{__version__} — all imports OK')
"
```

Expected: `harmonic_morphisms v0.1.0 — all imports OK`

- [ ] **Step 2: List final directory structure**

```bash
find harmonic_morphisms -type f | grep -v __pycache__ | grep -v '.egg-info' | sort
```

Expected output:

```
harmonic_morphisms/README.md
harmonic_morphisms/data/networks/out.dimacs10-celegans_metabolic
harmonic_morphisms/data/networks/out.dimacs10-netscience
harmonic_morphisms/data/networks/out.ego-facebook
harmonic_morphisms/data/networks/out.subelj_euroroad_euroroad
harmonic_morphisms/data/networks/random_10_0.85min_cliques_Thiers13.json
harmonic_morphisms/data/networks/reptilia-tortoise-network-fi.edges
harmonic_morphisms/data/precomputed/Cel_results.pkl
harmonic_morphisms/data/precomputed/Euroroad_results.pkl
harmonic_morphisms/data/precomputed/Ns_results.pkl
harmonic_morphisms/data/precomputed/Sif_results.pkl
harmonic_morphisms/data/precomputed/b9_results.pkl
harmonic_morphisms/data/precomputed/bf_results.pkl
harmonic_morphisms/data/precomputed/em_results.pkl
harmonic_morphisms/data/precomputed/er_results.pkl
harmonic_morphisms/data/precomputed/hf_results.pkl
harmonic_morphisms/data/precomputed/lc_results.pkl
harmonic_morphisms/data/precomputed/pl_results.pkl
harmonic_morphisms/data/precomputed/pw_results.pkl
harmonic_morphisms/data/precomputed/tort_results.pkl
harmonic_morphisms/data/precomputed/we_results.pkl
harmonic_morphisms/data/precomputed/wpl_results.pkl
harmonic_morphisms/data/precomputed/yeast_results.pkl
harmonic_morphisms/docs/api.md
harmonic_morphisms/docs/paper_figures.md
harmonic_morphisms/docs/quickstart.md
harmonic_morphisms/notebooks/01_euroroad_laplacian.ipynb
harmonic_morphisms/notebooks/02_average_curves.ipynb
harmonic_morphisms/notebooks/03_individual_laplacian.ipynb
harmonic_morphisms/notebooks/04_higher_order_synthetic.ipynb
harmonic_morphisms/notebooks/05_higher_order_real.ipynb
harmonic_morphisms/notebooks/06_equilibrium_laplacian.ipynb
harmonic_morphisms/pyproject.toml
harmonic_morphisms/src/harmonic_morphisms/__init__.py
harmonic_morphisms/src/harmonic_morphisms/core.py
harmonic_morphisms/src/harmonic_morphisms/higher_order.py
harmonic_morphisms/src/harmonic_morphisms/simplicial.py
```

- [ ] **Step 3: Final commit**

```bash
git add -A harmonic_morphisms/
git commit -m "feat: complete harmonic_morphisms package v0.1.0"
```
