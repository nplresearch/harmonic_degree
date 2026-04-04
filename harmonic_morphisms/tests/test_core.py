"""Unit tests for harmonic_morphisms.core."""

import networkx as nx
import numpy as np
import pytest

from harmonic_morphisms import H_CF_cluster, simple_renorm, g_len, h_v, renorm_graph_harmonic


# ---------------------------------------------------------------------------
# H_CF_cluster
# ---------------------------------------------------------------------------

class TestHCFCluster:
    """Tests for the central harmonic/conformal degree function."""

    def test_known_harmonic_morphism_k33(self, k33_harmonic):
        """K_{3,3} → K_2 is an exact harmonic morphism: M_deg_h = 1, std_h = 0."""
        G, clusters = k33_harmonic
        (G_coarse, deg_h, M_deg_h, std_h, av_h, std_v_h, Not_h,
         deg_cf, M_deg_cf, std_cf, av_cf, std_v_cf, Not_cf) = H_CF_cluster(G, clusters)

        assert G_coarse.number_of_nodes() == 2
        assert G_coarse.number_of_edges() == 1
        assert M_deg_h == pytest.approx(1.0)
        assert deg_h == pytest.approx(1.0)
        assert std_h == pytest.approx(0.0)
        assert len(Not_h) == 0

    def test_k33_is_harmonic_but_not_conformal(self, k33_harmonic):
        """K_{3,3} → K_2 is harmonic but NOT conformal.

        Each node sees 3 neighbors in the other partition (horizontal) but the
        vertical space (same-cluster neighbors + self) adds card_i = 1, giving
        c_list = [3, 1] → std ≠ 0 → not conformal.
        """
        G, clusters = k33_harmonic
        (_, _, _, _, _, _, _, deg_cf, M_deg_cf, std_cf, _, _, Not_cf) = H_CF_cluster(G, clusters)

        assert M_deg_cf == pytest.approx(0.0)
        assert len(Not_cf) == 6  # all nodes are non-conformal

    def test_non_harmonic_clustering(self):
        """Star with unbalanced clustering: center sees 2 neighbors in one
        cluster and 3 in another → c_list = [2, 3] → not harmonic."""
        G = nx.star_graph(5)  # center=0, leaves=1..5
        clusters = {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 2}
        (G_coarse, deg_h, M_deg_h, std_h, av_h, std_v_h, Not_h,
         deg_cf, M_deg_cf, std_cf, av_cf, std_v_cf, Not_cf) = H_CF_cluster(G, clusters)

        assert G_coarse.number_of_nodes() == 3
        assert M_deg_h < 1.0
        assert 0 in Not_h  # center node is non-harmonic

    def test_identity_clustering(self):
        """Each node in its own cluster → trivially harmonic (no merging)."""
        G = nx.cycle_graph(5)
        clusters = {n: n for n in G.nodes()}
        (G_coarse, deg_h, M_deg_h, std_h, av_h, std_v_h, Not_h,
         deg_cf, M_deg_cf, std_cf, av_cf, std_v_cf, Not_cf) = H_CF_cluster(G, clusters)

        assert G_coarse.number_of_nodes() == 5
        assert deg_h == pytest.approx(1.0)
        assert std_h == pytest.approx(0.0)

    def test_single_cluster(self):
        """All nodes in one cluster → coarse graph has 1 node, 0 edges."""
        G = nx.complete_graph(4)
        clusters = {n: 0 for n in G.nodes()}
        (G_coarse, deg_h, M_deg_h, std_h, av_h, std_v_h, Not_h,
         deg_cf, M_deg_cf, std_cf, av_cf, std_v_cf, Not_cf) = H_CF_cluster(G, clusters)

        assert G_coarse.number_of_nodes() == 1
        assert G_coarse.number_of_edges() == 0

    def test_return_types(self, k33_harmonic):
        """Check that return types are correct."""
        G, clusters = k33_harmonic
        result = H_CF_cluster(G, clusters)
        assert len(result) == 13
        G_coarse, deg_h, M_deg_h, std_h, av_h, std_v_h, Not_h, \
            deg_cf, M_deg_cf, std_cf, av_cf, std_v_cf, Not_cf = result

        assert isinstance(G_coarse, nx.Graph)
        assert isinstance(deg_h, float)
        assert isinstance(M_deg_h, (float, np.floating))
        assert isinstance(av_h, list)
        assert isinstance(Not_h, list)

    def test_degrees_in_unit_interval(self):
        """For any valid input, degrees should be in [0, 1]."""
        G = nx.barabasi_albert_graph(30, 2, seed=42)
        clusters = {n: n % 5 for n in G.nodes()}
        (_, deg_h, M_deg_h, _, _, _, _, deg_cf, M_deg_cf, _, _, _, _) = H_CF_cluster(G, clusters)

        assert 0.0 <= deg_h <= 1.0
        assert 0.0 <= M_deg_h <= 1.0
        assert 0.0 <= deg_cf <= 1.0
        assert 0.0 <= M_deg_cf <= 1.0

    def test_deviation_nonnegative(self):
        """Standard deviations should never be negative."""
        G = nx.barabasi_albert_graph(30, 2, seed=42)
        clusters = {n: n % 3 for n in G.nodes()}
        (_, _, _, std_h, _, _, _, _, _, std_cf, _, _, _) = H_CF_cluster(G, clusters)

        assert std_h >= 0.0
        assert std_cf >= 0.0


# ---------------------------------------------------------------------------
# simple_renorm
# ---------------------------------------------------------------------------

class TestSimpleRenorm:
    """Tests for Laplacian renormalization."""

    def test_t_zero_no_merging(self, path_graph_10):
        """At t=0, exp(-0*L) = I, no off-diagonal exceeds diagonal → no merging."""
        G, L = path_graph_10
        G_coarse = simple_renorm(G, 0.0, L, tresh=0)
        assert G_coarse.number_of_nodes() == G.number_of_nodes()

    def test_large_t_collapses(self, path_graph_10):
        """Large t should merge nodes, reducing count."""
        G, L = path_graph_10
        G_coarse = simple_renorm(G, 50.0, L, tresh=0)
        assert G_coarse.number_of_nodes() < G.number_of_nodes()

    def test_threshold_effect(self, path_graph_10):
        """Larger threshold → more merging → fewer nodes."""
        G, L = path_graph_10
        t = 1.0
        G_strict = simple_renorm(G, t, L, tresh=0)
        G_loose = simple_renorm(G, t, L, tresh=0.1)
        assert G_loose.number_of_nodes() <= G_strict.number_of_nodes()


# ---------------------------------------------------------------------------
# renorm_graph_harmonic
# ---------------------------------------------------------------------------

class TestRenormGraphHarmonic:
    """Tests for renormalization with harmonic degree computation."""

    def test_returns_14_values(self, path_graph_10):
        G, L = path_graph_10
        result = renorm_graph_harmonic(G, 1.0, L, tresh=0)
        assert len(result) == 14  # 13 from H_CF_cluster + Gv

    def test_metagraph_same_nodes(self, path_graph_10):
        """The metagraph Gv should have the same nodes as the original graph."""
        G, L = path_graph_10
        *_, Gv = renorm_graph_harmonic(G, 1.0, L, tresh=0)
        assert set(Gv.nodes()) == set(G.nodes())


# ---------------------------------------------------------------------------
# g_len
# ---------------------------------------------------------------------------

class TestGLen:

    def test_basic(self):
        graphs = [nx.complete_graph(n) for n in [5, 3, 1]]
        assert g_len(graphs) == [5, 3, 1]

    def test_empty_list(self):
        assert g_len([]) == []


# ---------------------------------------------------------------------------
# h_v (sweep over t values)
# ---------------------------------------------------------------------------

class TestHV:

    def test_output_lengths_match_t_span(self, path_graph_10):
        G, L = path_graph_10
        t_span = np.linspace(0, 2, 5)
        result = h_v(G, t_span, L, tresh=0)
        # Returns 14 lists: g, DEG_H, ..., gV
        assert len(result) == 14
        # Each list should have len(t_span) elements
        for lst in result:
            assert len(lst) == len(t_span)

    def test_compression_monotonic(self, path_graph_10):
        """Node count should be non-increasing as t grows."""
        G, L = path_graph_10
        t_span = np.linspace(0, 5, 10)
        graphs = h_v(G, t_span, L, tresh=0)[0]
        node_counts = g_len(graphs)
        for i in range(len(node_counts) - 1):
            assert node_counts[i] >= node_counts[i + 1]
