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
Auto-sweep for higher-order renormalization.

---

## `harmonic_morphisms.simplicial`

### Network I/O

**`import_network_data(f)`**
Parse edge list file, extract LCC, relabel nodes 0..N-1.

### Simplicial complex generators

**`NGF(d, N, s, beta, M=1)`** — Network Geometry with Flavor

**`pseudofractal_d2(steps)`** — Pseudofractal d=2

**`pseudofractal_d3(steps)`** — Pseudofractal d=3

**`apollonian_d2(steps)`** — Apollonian d=2

**`convert_graph_to_sc(G, dim=2, type='clique')`** — Graph to clique complex

### Algebraic topology

**`boundary_matrices_ext(sc)`** — Boundary matrices B1..B4.

**`laplacians(sc)`** — Hodge Laplacians L0..L4.

**`adjacency_of_order(sc, k, l, sparse=False)`** — k-order adjacency.

**`XO_laplacian(sc, k, l, sparse=False)`** — Cross-order Laplacian.

### Spectral analysis

**`compute_entropic_C(D, exm, exM, n_t)`** — Entropic susceptibility.

**`compute_spectral_d(D, exm, exM, n_t)`** — Spectral dimension.

### Visualization

**`plot_complex(sc, ax, ...)`** — Draw simplicial complex.
