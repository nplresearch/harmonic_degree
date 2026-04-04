"""Integration and regression tests using shipped data."""

import pickle
from pathlib import Path

import networkx as nx
import numpy as np
import pytest

from harmonic_morphisms import H_CF_curves, g_len
from harmonic_morphisms.simplicial import import_network_data


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


# ---------------------------------------------------------------------------
# Round-trip on Euroroad
# ---------------------------------------------------------------------------

class TestEuroroadRoundTrip:
    """Load the actual Euroroad edgelist and run a short Laplacian RG sweep."""

    @pytest.fixture
    def euroroad(self):
        f = open(DATA_DIR / "networks" / "out.subelj_euroroad_euroroad")
        G = import_network_data(f)
        L = np.array(nx.laplacian_matrix(G, nodelist=sorted(G.nodes())).todense(), dtype=float)
        return G, L

    def test_euroroad_loads(self, euroroad):
        G, L = euroroad
        assert G.number_of_nodes() > 500
        assert nx.is_connected(G)

    @pytest.mark.slow
    def test_euroroad_h_cf_curves(self, euroroad):
        """Run H_CF_curves with few points — check output shapes and value ranges."""
        G, L = euroroad
        result = H_CF_curves(G, L, n=10, tresh=1e-3)
        graphs, DEG_H, M_DEG_H, STD_H, AV_H, STD_V_H, NOT_H, \
            DEG_CF, M_DEG_CF, STD_CF, AV_CF, STD_V_CF, NOT_CF, gV, t_span = result

        assert len(graphs) == 10
        assert len(t_span) == 10

        # Compression monotonically increasing
        node_counts = g_len(graphs)
        for i in range(len(node_counts) - 1):
            assert node_counts[i] >= node_counts[i + 1]

        # Degrees in valid range
        for deg in M_DEG_H:
            assert 0.0 <= deg <= 1.0
        for deg in M_DEG_CF:
            assert 0.0 <= deg <= 1.0

        # First graph ≈ original size, last should be small
        assert node_counts[0] == G.number_of_nodes()
        assert node_counts[-1] <= 2  # at t_f, should collapse to 1


# ---------------------------------------------------------------------------
# Pickle compatibility
# ---------------------------------------------------------------------------

class TestPickleCompatibility:
    """Verify that precomputed pickle files have the expected structure."""

    @pytest.fixture(params=[
        "Euroroad_results.pkl", "Ns_results.pkl", "Cel_results.pkl",
    ])
    def results_pickle(self, request):
        pkl_path = DATA_DIR / "precomputed" / request.param
        if not pkl_path.exists():
            pytest.skip(f"{request.param} not found")
        with open(pkl_path, "rb") as f:
            return pickle.load(f)

    def test_has_laplacian_keys(self, results_pickle):
        """Each pickle should have Laplacian harmonic/conformal results."""
        results = results_pickle
        assert "Laplacian Harmonic Modified" in results
        assert "Laplacian Conformal Modified" in results

    def test_laplacian_values_are_arrays(self, results_pickle):
        h_mod = results_pickle["Laplacian Harmonic Modified"]
        assert hasattr(h_mod, "__len__")
        assert len(h_mod) > 0

    def test_gnn_data_key_exists(self, results_pickle):
        """Precomputed pickles should contain GNN results for notebook 02."""
        assert "GNN DATA" in results_pickle


# ---------------------------------------------------------------------------
# All precomputed pickles loadable
# ---------------------------------------------------------------------------

class TestAllPicklesLoadable:

    def test_all_16_pickles_load(self):
        pkl_dir = DATA_DIR / "precomputed"
        if not pkl_dir.exists():
            pytest.skip("precomputed directory not found")
        pkl_files = list(pkl_dir.glob("*.pkl"))
        assert len(pkl_files) == 16, f"Expected 16 pickles, found {len(pkl_files)}"
        for pkl_path in pkl_files:
            with open(pkl_path, "rb") as f:
                data = pickle.load(f)
            assert isinstance(data, dict), f"{pkl_path.name} is not a dict"


# ---------------------------------------------------------------------------
# Network data files exist
# ---------------------------------------------------------------------------

class TestDataFilesExist:

    @pytest.mark.parametrize("filename", [
        "out.subelj_euroroad_euroroad",
        "out.dimacs10-netscience",
        "out.ego-facebook",
        "out.dimacs10-celegans_metabolic",
        "reptilia-tortoise-network-fi.edges",
        "random_10_0.85min_cliques_Thiers13.json",
    ])
    def test_network_file_exists(self, filename):
        path = DATA_DIR / "networks" / filename
        assert path.exists(), f"Missing data file: {filename}"
