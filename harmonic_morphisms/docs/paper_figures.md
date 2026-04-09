# Paper Figure to Notebook Map

Figures from *"Harmonic morphisms and dynamical invariants in network renormalization"* (PRX).

## Main Figures

| Figure | Label | Description | Notebook | Output file |
|--------|-------|-------------|----------|-------------|
| 1 | `fig:figure_1` | Schematic examples of harmonic morphisms (Urakawa example, node collapse, torus-to-cycle, combinatorial conformal map, harmonic measure on grid, non-harmonic vs harmonic coarse-graining) | Created in vector graphics editor / generated separately (`New_Images/New_Images_2/Figure_1_merged.pdf`) | — |
| 2a | `fig:euroroad_comparison` (panel a) | Euroroad Laplacian RG curves | `01_euroroad_laplacian.ipynb` | `fig02a_euroroad_laplacian.pdf` |
| 2b | `fig:euroroad_comparison` (panel b) | Euroroad modified harmonic degree vs compression | `01_euroroad_laplacian.ipynb` | — |
| 2c | `fig:euroroad_comparison` (panel c) | Euroroad modified conformal degree vs compression | `01_euroroad_laplacian.ipynb` | — |
| 2b-c (geometric) | `fig:euroroad_comparison` | Geometric panel of Euroroad fingerprints | `Geometric/1/Real_nets_Geometric_1.ipynb` (requires d-mercator) | — |
| 2b-c (GNN) | `fig:euroroad_comparison` | GNN panel of Euroroad fingerprints | `GNN_partition_function/Real_nets_GNN.ipynb` (requires torch_geometric) | — |
| 2d | `fig:euroroad_comparison` (panel d) | Average harmonic degree across 16 networks | `02_average_curves.ipynb` | `fig02d_average_harmonic.pdf` |
| 2e | `fig:euroroad_comparison` (panel e) | Average conformal degree across 16 networks | `02_average_curves.ipynb` | `fig02e_average_conformal.pdf` |
| 3 | `fig:hdev_viz` | Spatial distribution of harmonic deviation under Laplacian RG of NetSci network (deviation curve, community assignments, per-node deviation maps) | `01_euroroad_laplacian.ipynb` or `03_individual_laplacian.ipynb` | `fig03_euroroad_spatial.pdf` |
| 4 | `fig:figure_4` | Harmonic degree and entropic susceptibility (two networks with H_mod ≈ 1 showing distinct vs scale-invariant structure) | `Laplacian/Real_networks_LRG.ipynb` (repo root) | — |
| 5 | `fig:higher_order` (panels a,b) | Harmonic degrees of pseudofractal simplicial complex d=2 (1-skeleton Laplacian; triangle-edge adjacency graph) | `04_higher_order_synthetic.ipynb` | `fig04_pf2_panel.pdf` |
| 6 | — | Clustering comparisons (SBM) | `Clustering/Clustering_examples.ipynb` (requires graph_tool for SBM) | — |
| 7 | — | UMAP embeddings | `Clustering/Visualizations_UMAP/Visualize_NetSci_Metrics.ipynb` (requires umap-learn and graph_tool) | — |

> **Note on Figure 2:** The full multi-panel figure (`fig:euroroad_comparison`) is assembled from outputs of three separate notebooks corresponding to the three renormalization methods. The Laplacian panels come from `01_euroroad_laplacian.ipynb` and the average panels from `02_average_curves.ipynb`; the geometric and GNN panels require external tools (see below).

## Supplementary Material Figures

| SM Figure | Label | Description | Notebook |
|-----------|-------|-------------|----------|
| SM: all networks harmonic | `fig:si:all_results_harmonic` | Harmonic degree vs compression for all 16 networks + average, all three methods | `02_average_curves.ipynb` |
| SM: all networks conformal | `fig:si:all_results_conformal` | Conformal degree vs compression for all 16 networks + average, all three methods | `02_average_curves.ipynb` |
| SM: geometric examples | `fig:si:geometric_renorm_examples` | Geometric renormalization of power (bcspwr09), Minnesota Road, Song of Ice and Fire networks | `Geometric/1/Real_nets_Geometric_1.ipynb` (requires d-mercator) |
| SM: Laplacian examples | `fig:si:laplacian_renorm_examples` | Laplacian RG of NetSci, C. elegans, Facebook networks with community visualizations | `03_individual_laplacian.ipynb` |
| SM: GNN examples | `fig:si:gnn_renormalization_examples` | GNN renormalization of Weaver network (partition function difference, harmonicity measures, sampled partitions) | `GNN_partition_function/Real_nets_GNN.ipynb` (requires torch_geometric) |
| SM: equilibrium Laplacian | `fig:si:eq_lap` | Equilibrium Laplacian RG for NetSci, C. elegans, Tortoise networks | `06_equilibrium_laplacian.ipynb` or `Laplacian/In Equilibrium Laplacian/Eq_Laplacian.ipynb` (repo root) |
| SM: higher-order pf2 comparison | `fig:si:ho_pf2` | Higher-order and node-based RG schemes on pseudofractal d=2 (4 steps) via harmonic degree | `04_higher_order_synthetic.ipynb` |
| SM: pf2 harmonic degrees | `fig:si:pf2d` | Harmonic degrees of pseudofractal d=2 (no 2-D holes; Hodge-Laplacian transformation) | `04_higher_order_synthetic.ipynb` |
| SM: pf3 harmonic degrees | `fig:si:pf3d` | Harmonic degrees vs compression for 2nd and 3rd order operators on pseudofractal d=3 | `04_higher_order_synthetic.ipynb` |
| SM: Thiers13 | `fig:si:thiers13` | Harmonic degrees of Thiers13 simplicial complex under 2-order operators | `05_higher_order_real.ipynb` |

## Previously numbered figures (old numbering)

These correspond to the numbered entries from the original map, cross-referenced with labels above:

| Old # | Description | Notebook | Output file |
|-------|-------------|----------|-------------|
| 12 | NetSci Laplacian RG | `03_individual_laplacian.ipynb` | `fig12_*.pdf` |
| 13 | Facebook Laplacian RG | `03_individual_laplacian.ipynb` | `fig13_*.pdf` |
| 14 | C. elegans Laplacian RG | `03_individual_laplacian.ipynb` | `fig14_*.pdf` |
| 16 | Equilibrium Laplacian RG | `06_equilibrium_laplacian.ipynb` | `fig16_equilibrium_laplacian.pdf` |
| 17 | Pseudofractal d2 compression curves | `04_higher_order_synthetic.ipynb` | `fig17_pf2_compression.pdf` |
| 18 | Pseudofractal d3 compression curves | `04_higher_order_synthetic.ipynb` | `fig18_pf3_compression.pdf` |
| 19 | Thiers13 higher-order RG | `05_higher_order_real.ipynb` | `fig19_thiers13.pdf` |

## Figures requiring external tools

These panels cannot be reproduced with the core package dependencies alone:

| Figure / Label | Reason | Notebook |
|----------------|--------|----------|
| Fig. 2b-c (geometric) / `fig:euroroad_comparison` | Geometric renormalization requires external d-mercator tool | `Geometric/1/Real_nets_Geometric_1.ipynb` |
| Fig. 2b-c (GNN) / `fig:euroroad_comparison` | GNN renormalization requires torch_geometric | `GNN_partition_function/Real_nets_GNN.ipynb` |
| Fig. 6 (clustering) | Clustering comparisons require graph_tool for SBM inference | `Clustering/Clustering_examples.ipynb` |
| Fig. 7 (UMAP) | UMAP embeddings require umap-learn and graph_tool | `Clustering/Visualizations_UMAP/Visualize_NetSci_Metrics.ipynb` |
| `fig:si:geometric_renorm_examples` | Requires d-mercator | `Geometric/1/Real_nets_Geometric_1.ipynb` |
| `fig:si:gnn_renormalization_examples` | Requires torch_geometric | `GNN_partition_function/Real_nets_GNN.ipynb` |

## Complete label inventory

All `\label{fig:...}` entries found in `prx_preprint.tex`:

| LaTeX label | Figure |
|-------------|--------|
| `fig:figure_1` | Figure 1 (schematic) |
| `fig:euroroad_comparison` | Figure 2 (Euroroad fingerprints + averages) |
| `fig:hdev_viz` | Figure 3 (NetSci spatial harmonic deviation) |
| `fig:figure_4` | Figure 4 (entropic susceptibility) |
| `fig:higher_order` | Figure 5 (higher-order pseudofractal d=2) |
| `fig:si:all_results_harmonic` | SM: all networks harmonic degree |
| `fig:si:all_results_conformal` | SM: all networks conformal degree |
| `fig:si:geometric_renorm_examples` | SM: geometric renorm examples |
| `fig:si:laplacian_renorm_examples` | SM: Laplacian renorm examples |
| `fig:si:gnn_renormalization_examples` | SM: GNN renorm examples |
| `fig:si:eq_lap` | SM: equilibrium Laplacian |
| `fig:si:ho_pf2` | SM: higher-order pf2 comparison |
| `fig:si:pf2d` | SM: pf2 harmonic degrees |
| `fig:si:pf3d` | SM: pf3 harmonic degrees |
| `fig:si:thiers13` | SM: Thiers13 |
