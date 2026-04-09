# Network Dataset Manifest

This document catalogs all 50 real networks used in the paper. Networks span six
domains and were used in two experimental contexts: a clustering benchmark across
all 50 networks and a three-way renormalization comparison on a 16-network subset.

---

## Summary by Category

| Category | Count |
|---|---|
| Biological | 16 |
| Social | 11 |
| Tech/Web | 10 |
| Infrastructure | 7 |
| Collaboration | 4 |
| Animal | 2 |
| **Total** | **50** |

---

## Full Network List

All graph sizes refer to the largest connected component (LCC) after removing
self-loops, which is the version used in the analysis.

| Network name (paper) | Category | Source | Pickle group | In renorm. subset? | Data file(s) |
|---|---|---|---|---|---|
| E-road | Infrastructure | KONECT | df_1 | yes (`Euroroad_results.pkl`) | `out.subelj_euroroad_euroroad` |
| NetSci Collab | Collaboration | KONECT | df_1 | yes (`Ns_results.pkl`) | `out.dimacs10-netscience` |
| C. Elegans | Biological | KONECT | df_1 | yes (`Cel_results.pkl`) | `out.dimacs10-celegans_metabolic` |
| Song of Ice and Fire | Social | KONECT | df_1 | yes (`Sif_results.pkl`) | `out.asoiaf` |
| Emails | Social | KONECT | df_1 | yes (`em_results.pkl`) | `out.arenas-email` |
| Facebook | Social | KONECT | df_1 | no | `out.ego-facebook` |
| basophil | Biological | OhmNet/BioSNAP | df_2 | yes (`bf_results.pkl`) | `PPT-Ohmnet_tissues-combined.edgelist` |
| brain | Biological | OhmNet/BioSNAP | df_2 | no | `PPT-Ohmnet_tissues-combined.edgelist` |
| cardiac_muscle | Biological | OhmNet/BioSNAP | df_2 | no | `PPT-Ohmnet_tissues-combined.edgelist` |
| cornea | Biological | OhmNet/BioSNAP | df_2 | no | `PPT-Ohmnet_tissues-combined.edgelist` |
| epidermis | Biological | OhmNet/BioSNAP | df_2 | no | `PPT-Ohmnet_tissues-combined.edgelist` |
| jejunum | Biological | OhmNet/BioSNAP | df_2 | no | `PPT-Ohmnet_tissues-combined.edgelist` |
| locus_ceruleus | Biological | OhmNet/BioSNAP | df_2 | yes (`lc_results.pkl`) | `PPT-Ohmnet_tissues-combined.edgelist` |
| lung | Biological | OhmNet/BioSNAP | df_2 | no | `PPT-Ohmnet_tissues-combined.edgelist` |
| natural_killer_cell | Biological | OhmNet/BioSNAP | df_2 | no | `PPT-Ohmnet_tissues-combined.edgelist` |
| neuron | Biological | OhmNet/BioSNAP | df_2 | no | `PPT-Ohmnet_tissues-combined.edgelist` |
| ovarian_follicle | Biological | OhmNet/BioSNAP | df_2 | no | `PPT-Ohmnet_tissues-combined.edgelist` |
| t_lymphocyte | Biological | OhmNet/BioSNAP | df_2 | no | `PPT-Ohmnet_tissues-combined.edgelist` |
| Relativity collab | Collaboration | SNAP | df_3 | no | `ca-GrQc.txt/CA-GrQc.txt` |
| Oregon route-views | Tech/Web | SNAP | df_3 | no | `Oregon_graph/oregon1_010331.txt` |
| Lastfm Asia | Social | SNAP | df_3 | no | `lasftm_asia/lastfm_asia_edges.csv` |
| Power: US Grid | Infrastructure | NetworkRepository | df_4 | no | `power-US-Grid/power-US-Grid.mtx` |
| Power: Eris | Infrastructure | NetworkRepository | df_4 | yes (`pw_results.pkl`) | `power-eris1176/power-eris1176.mtx` |
| Animal net: Weaver | Animal | NetworkRepository | df_4 | yes (`we_results.pkl`) | `aves-weaver-social/aves-weaver-social.edges` |
| Animal net: Tortoise | Animal | NetworkRepository | df_4 | yes (`tort_results.pkl`) | `reptilia-tortoise-network-fi/reptilia-tortoise-network-fi.edges` |
| Bio: plant | Biological | NetworkRepository | df_4 | yes (`pl_results.pkl`) | `bio-grid-plant/bio-grid-plant.edges` |
| Bio: worm | Biological | NetworkRepository | df_4 | no | `bio-grid-worm/bio-grid-worm.edges` |
| Bio: yeast | Biological | NetworkRepository | df_4 | yes (`yeast_results.pkl`) | `bio-yeast/bio-yeast.mtx` |
| Tech: PGP | Tech/Web | NetworkRepository | df_4 | no | `tech-pgp/tech-pgp.edges` |
| Flights | Infrastructure | NetworkRepository | df_5 | no | `inf-openflights/inf-openflights.edges` |
| Power: bcspwr09 | Infrastructure | NetworkRepository | df_5 | yes (`b9_results.pkl`) | `power-bcspwr09/power-bcspwr09.mtx` |
| Power: bcspwr10 | Infrastructure | NetworkRepository | df_5 | no | `power-bcspwr10/power-bcspwr10.mtx` |
| Minnesota Road | Infrastructure | NetworkRepository | df_5 | no | `road-minnesota/road-minnesota.mtx` |
| Tech: Routers rf | Tech/Web | NetworkRepository | df_5 | no | `tech-routers-rf/tech-routers-rf.mtx` |
| Tech: WHOIS | Tech/Web | NetworkRepository | df_5 | no | `tech-WHOIS/tech-WHOIS.mtx` |
| Web: edu | Tech/Web | NetworkRepository | df_5 | no | `web-edu/web-edu.mtx` |
| Web: polblogs | Tech/Web | NetworkRepository | df_5 | yes (`wpl_results.pkl`) | `web-polblogs/web-polblogs.mtx` |
| FB: Gov. | Social | NetworkRepository | df_6 | no | `fb-pages-government/fb-pages-government.edges` |
| Hamsterster | Social | NetworkRepository | df_6 | yes (`er_results.pkl`) | `soc-hamsterster/soc-hamsterster.edges` |
| FB: USFCA72 | Social | NetworkRepository | df_6 | no | `socfb-USFCA72/socfb-USFCA72.mtx` |
| FB: UC64 | Social | NetworkRepository | df_6 | no | `socfb-UC64/socfb-UC64.mtx` |
| FB: Haverford76 | Social | NetworkRepository | df_6 | yes (`hf_results.pkl`) | `socfb-Haverford76/socfb-Haverford76.mtx` |
| FB: Colgate88 | Social | NetworkRepository | df_6 | no | `socfb-Colgate88/socfb-Colgate88.mtx` |
| FB: American75 | Social | NetworkRepository | df_6 | no | `socfb-American75/socfb-American75.mtx` |
| Anybeat | Social | NetworkRepository | df_6 | no | `soc-anybeat/soc-anybeat.edges` |
| Erdos Collab | Collaboration | NetworkRepository | df_6 | no | `ca-Erdos992/ca-Erdos992.mtx` |
| CS Collab | Collaboration | NetworkRepository | df_6 | no | `ca-CSphd/ca-CSphd.mtx` |
| Web: Indochina | Tech/Web | NetworkRepository | df_7 | no | `web-indochina-2004/web-indochina-2004.mtx` |
| Web: EPA | Tech/Web | NetworkRepository | df_7 | no | `web-EPA/web-EPA.edges` |
| Web: spam | Tech/Web | NetworkRepository | df_7 | no | `web-spam/web-spam.mtx` |

---

## Renormalization Subset (16 networks)

The 16 networks in `pre_computed_measures/` were selected to span diverse domains
and sizes while being tractable for all three renormalization methods (Laplacian,
Geometric, and GNN). The filename abbreviations used are:

| File | Network |
|---|---|
| `b9_results.pkl` | Power: bcspwr09 |
| `bf_results.pkl` | basophil |
| `Cel_results.pkl` | C. Elegans |
| `em_results.pkl` | Emails |
| `er_results.pkl` | Hamsterster |
| `Euroroad_results.pkl` | E-road |
| `hf_results.pkl` | FB: Haverford76 |
| `lc_results.pkl` | locus_ceruleus |
| `Ns_results.pkl` | NetSci Collab |
| `pl_results.pkl` | Bio: plant |
| `pw_results.pkl` | Power: Eris |
| `Sif_results.pkl` | Song of Ice and Fire |
| `tort_results.pkl` | Animal net: Tortoise |
| `we_results.pkl` | Animal net: Weaver |
| `wpl_results.pkl` | Web: polblogs |
| `yeast_results.pkl` | Bio: yeast |

Each pickle stores a dict with keys `Graph`, `length original Graph`,
`Laplacian Harmonic Modified`, `Laplacian Conformal Modified`, `Laplacian H Dev`,
`Geometric Harmonic Modified`, `Geometric Conformal Modified`, `Geometric H Dev`,
`GNN DATA`, and associated compression/iteration metadata for all three methods.

---

## Analysis Scope

### Clustering benchmark
- **Networks**: all 50 (organized in 7 groups, `df_1` through `df_7`)
- **Methods**: Label Propagation, Greedy Modularity, Louvain, Infomap, SBM (5 total)
- **Metric**: harmonic degree H, modified harmonic degree Mod. H, Std. H
- **Results**: `Clustering/Final_outputs/df_1.pkl` — `df_7.pkl`
  (the `_ext` variants contain extended results with additional metrics)

### Renormalization comparison
- **Networks**: 16-network subset (see table above)
- **Methods**: Laplacian renormalization, Geometric (S1/H2) renormalization, GNN renormalization
- **Results**: `pre_computed_measures/` (one pickle per network)
- **Aggregated plots**: `plot_average.ipynb` / `harmonic_morphisms/notebooks/02_average_curves.ipynb`

---

## Data Sources

| Source | URL | Networks |
|---|---|---|
| KONECT (Koblenz Network Collection) | http://konect.cc | E-road, NetSci Collab, C. Elegans, Song of Ice and Fire, Emails, Facebook |
| NetworkRepository | https://networkrepository.com | All 30 networks with `readme.html` in `Data/` subdirectory |
| SNAP (Stanford Network Analysis Project) | https://snap.stanford.edu | Relativity collab (CA-GrQc), Oregon route-views, Lastfm Asia |
| OhmNet / BioSNAP | https://snap.stanford.edu/biodata/datasets/10013/10013-PPT-Ohmnet.html | 12 tissue PPI networks (basophil through t_lymphocyte) |
