**Harmonic Morphisms and dynamical invariants in network renormalization**

Hi, this repository provides the code to calulcate the Harmonic degree (and realted measures) to network coarse-grainings. 
The main functions is **Harmonic_degree.py**, which implements the harmonic degree computation of a given clustering.
Other functions are:
- Higher_order_harmonic_degree.py: implements generalized higher-order Laplacian renormalization and harmonic degree for higher-order networks.
- HOLR_functions.py: used for Laplacian Renormalization and Higher Order. Taken from https://github.com/nplresearch/higher_order_LRG.


The folders are:
- Data: Contains data used in the experiments 
- Clustering: Experiments with clustering methods
- Euroroad_results: contains the full renormalization group analysis done over a network, in this case the Euroroad network. We perform all the three renormalization methods and calculate the harmonic degree curves. Reproducing part of the plots shown in the paper. 
- Geometric\1: contains further experiments with Geometric Renormalization. Please note that to use it is essential to use also https://github.com/networkgeometry/d-mercator and https://github.com/zhmh163/Geometric-renormalization-of-weighted-network. 
- Laplacian: contains further experiments with Laplacian Renormalization + Equilibrium Laplacian. 
- GNN_partition_function: contains futher experiments with GNN-based Renormalization, it contains also some code taken from https://www.nature.com/articles/s41467-025-56034-2.
- Higher_Order: Generalized Laplacian Renormalization Scheme + analysis of the harmonic morphisms on adjacency and parallel adjacency graphs + Equilibrium Higher-Order Laplacian
- Finding_harmonic_Morph: codes with techniques we tried to find harmonic morphisms

**Please note that the preprocessing of data is done in Clustering->GT_Tools_producing_data->Preprocessing_and_SBM_creations.ipynb".**
Processed data are then stored in **Intermediate_outputs** folders, stored in 7 groups for readibility. Then processed data are directly used in all the jupyter of the notebooks. 
More specifically, the Clustering folder is organized as follows: 
- **GT_Tools_producing_data** described above
- **Visualizations_UMAP** that contains the codes to produce the plots regarding the UMAP described in the supplementary. In particular **Visualize_NetSci_Embeddings.ipynb** produces data stored in **Classical Summaries**.
- **Clustering_examples.ipynb** contains the clustering plots shown in the paper. 
- **Producing_Harmonic_degree_clustering.ipynb** produces the harmonic degree tables that are stored in **Final_outputs** and then visualized in the UMAP codes. 


Very specific functions and methods (i.e. Harmonic degree on parallel adjacency graph and Equilibrium diffusion) are implemented in the realted jupyter notebooks, and they will be outlined. 

Data are taken from https://networkrepository.com/ , https://snap.stanford.edu/ and https://snap.stanford.edu/biodata/. We stored them in Clustering/GT_Tools_producing_data/Data

For any question please write to francesco.guadagnuolo@epfl.ch


