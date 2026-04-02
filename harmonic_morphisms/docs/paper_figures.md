# Paper Figure to Notebook Map

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

These require external tools not in the core dependencies:

| Figure | Reason |
|--------|--------|
| 2b-c | Geometric and GNN panels require d-mercator and torch_geometric |
| 5 | Clustering comparisons require graph_tool for SBM |
| 6 | UMAP embeddings require umap-learn and graph_tool |
| 9-11 | Geometric renormalization requires d-mercator |
| 15 | GNN renormalization requires torch_geometric |
