"""Unit tests for harmonic_morphisms.simplicial."""

import networkx as nx
import numpy as np
import pytest

from harmonic_morphisms.simplicial import (
    pseudofractal_d2,
    pseudofractal_d3,
    apollonian_d2,
    convert_graph_to_sc,
    boundary_matrices_ext,
    laplacians,
    adjacency_of_order,
    XO_laplacian,
    compute_entropic_C,
    compute_spectral_d,
)


# ---------------------------------------------------------------------------
# Simplicial complex generators
# ---------------------------------------------------------------------------

class TestPseudofractalD2:
    """Pseudofractal d=2: starts with triangle, each step adds node per edge."""

    def test_step0_is_triangle(self):
        sc = pseudofractal_d2(0)
        assert sc["n0"] == 3
        assert sc["n1"] == 3
        assert sc["n2"] == 1  # one triangular face

    def test_step1_counts(self):
        sc = pseudofractal_d2(1)
        # Step 0: 3 nodes, 3 edges. Step 1: add 3 nodes (one per edge) → 6 nodes.
        # Edges: original 3 + 2 new per original edge = 3 + 6 = 9
        assert sc["n0"] == 6
        assert sc["n1"] == 9

    def test_step2_counts(self):
        sc = pseudofractal_d2(2)
        # Step 2: 9 new edges at step 1, each gets a new node → 6 + 9 = 15 nodes
        assert sc["n0"] == 15

    def test_step3_counts(self):
        sc = pseudofractal_d2(3)
        # n_0(s) = 3 + 3 + 9 + 27 = 3*(3^0 + 3^1 + 3^2) + 3 = ...
        # Actually: n_0(0)=3, n_1(0)=3. n_0(s) = n_0(s-1) + n_1(s-1)
        # n_1(s) = n_1(s-1) + 2*n_1(s-1) = 3*n_1(s-1)
        # n_0: 3, 6, 15, 42. n_1: 3, 9, 27, 81
        assert sc["n0"] == 42
        assert sc["n1"] == 81

    def test_sc_dict_keys(self):
        sc = pseudofractal_d2(1)
        for key in ["nodes", "edges", "faces", "tetrahedra", "4-simplices",
                     "n0", "n1", "n2", "n3", "n4"]:
            assert key in sc


class TestPseudofractalD3:

    def test_step0_is_tetrahedron(self):
        sc = pseudofractal_d3(0)
        assert sc["n0"] == 4
        assert sc["n1"] == 6
        assert sc["n2"] == 4
        assert sc["n3"] == 1

    def test_step1_counts(self):
        sc = pseudofractal_d3(1)
        # Each of 4 faces gets a new node → 4 + 4 = 8 nodes
        assert sc["n0"] == 8


class TestApollonianD2:

    def test_step0_is_triangle(self):
        sc = apollonian_d2(0)
        assert sc["n0"] == 3
        assert sc["n1"] == 3

    def test_step1_counts(self):
        sc = apollonian_d2(1)
        # Each of 3 edges gets a new node, but only boundary edges are subdivided
        assert sc["n0"] == 6


# ---------------------------------------------------------------------------
# Boundary matrices: ∂_{k-1} ∘ ∂_k = 0
# ---------------------------------------------------------------------------

class TestBoundaryMatrices:
    """The fundamental property of boundary operators: ∂∂ = 0."""

    def test_boundary_composition_d1_d2(self, pf2_small):
        """B1 @ B2 = 0 for pseudofractal d=2."""
        B1, B2, B3, B4, *_ = boundary_matrices_ext(pf2_small)
        product = (B1.toarray() @ B2.toarray())
        np.testing.assert_array_equal(product, 0)

    def test_boundary_composition_d2_d3_on_d3(self):
        """B2 @ B3 = 0 for pseudofractal d=3 (has tetrahedra)."""
        sc = pseudofractal_d3(1)
        B1, B2, B3, B4, *_ = boundary_matrices_ext(sc)
        product = (B2.toarray() @ B3.toarray())
        np.testing.assert_array_equal(product, 0)

    def test_boundary_shapes(self, pf2_small):
        sc = pf2_small
        B1, B2, B3, B4, *_ = boundary_matrices_ext(sc)
        assert B1.shape == (sc["n0"], sc["n1"])
        assert B2.shape == (sc["n1"], sc["n2"])
        assert B3.shape == (sc["n2"], sc["n3"])


# ---------------------------------------------------------------------------
# Hodge Laplacians
# ---------------------------------------------------------------------------

class TestLaplacians:

    def test_L0_matches_networkx(self, pf2_small):
        """L0 = B1 @ B1.T should equal the graph Laplacian from NetworkX."""
        sc = pf2_small
        L0, L1, L2, L3, L4, *_ = laplacians(sc)

        G = nx.Graph()
        G.add_nodes_from(range(sc["n0"]))
        G.add_edges_from(sc["edges"])
        L_nx = np.array(nx.laplacian_matrix(G, nodelist=range(sc["n0"])).todense())

        np.testing.assert_array_equal(L0, L_nx)

    def test_hodge_decomposition_L1(self, pf2_small):
        """L1 = B1^T B1 + B2 B2^T (Hodge decomposition)."""
        sc = pf2_small
        B1, B2, B3, B4, *_ = boundary_matrices_ext(sc)
        B1d, B2d = B1.toarray(), B2.toarray()
        L1_expected = B1d.T @ B1d + B2d @ B2d.T

        L0, L1, *_ = laplacians(sc)
        np.testing.assert_array_equal(L1, L1_expected)

    def test_laplacians_are_symmetric(self, pf2_small):
        L0, L1, L2, L3, L4, *_ = laplacians(pf2_small)
        for L in [L0, L1, L2]:
            np.testing.assert_array_almost_equal(L, L.T)

    def test_laplacians_positive_semidefinite(self, pf2_small):
        """All eigenvalues of Hodge Laplacians should be >= 0."""
        L0, L1, L2, L3, L4, *_ = laplacians(pf2_small)
        for L in [L0, L1, L2]:
            eigvals = np.linalg.eigvalsh(L)
            assert np.all(eigvals >= -1e-10), f"Negative eigenvalue found: {eigvals.min()}"

    def test_L0_has_one_zero_eigenvalue_connected(self, pf2_small):
        """For a connected simplicial complex, L0 has exactly one zero eigenvalue."""
        L0, *_ = laplacians(pf2_small)
        eigvals = np.linalg.eigvalsh(L0)
        n_zero = np.sum(np.abs(eigvals) < 1e-10)
        assert n_zero == 1


# ---------------------------------------------------------------------------
# Adjacency of order
# ---------------------------------------------------------------------------

class TestAdjacencyOfOrder:

    def test_symmetric(self, pf2_small):
        A = adjacency_of_order(pf2_small, k=1, l=0)
        np.testing.assert_array_equal(A, A.T)

    def test_zero_diagonal(self, pf2_small):
        A = adjacency_of_order(pf2_small, k=1, l=0)
        np.testing.assert_array_equal(np.diag(A), 0)

    def test_shape(self, pf2_small):
        sc = pf2_small
        A = adjacency_of_order(sc, k=1, l=0)
        assert A.shape == (sc["n1"], sc["n1"])

    def test_k_equals_l_raises(self, pf2_small):
        with pytest.raises(AssertionError):
            adjacency_of_order(pf2_small, k=1, l=1)


# ---------------------------------------------------------------------------
# XO Laplacian
# ---------------------------------------------------------------------------

class TestXOLaplacian:

    def test_symmetric(self, pf2_small):
        L = XO_laplacian(pf2_small, k=1, l=0)
        np.testing.assert_array_equal(L, L.T)

    def test_positive_semidefinite(self, pf2_small):
        L = XO_laplacian(pf2_small, k=1, l=0)
        eigvals = np.linalg.eigvalsh(L)
        assert np.all(eigvals >= -1e-10)


# ---------------------------------------------------------------------------
# Spectral functions
# ---------------------------------------------------------------------------

class TestSpectralFunctions:

    def test_compute_spectral_d_returns_correct_shape(self):
        """Output length should be n_t - 1 (finite differences)."""
        D = np.array([0.0, 1.0, 2.5, 4.0, 6.0])
        dS, tau = compute_spectral_d(D, -1, 1, 50)
        assert len(dS) == 49
        assert len(tau) == 49

    def test_compute_spectral_d_complete_graph(self):
        """For K_n, spectral dimension should approach 0 at large times (finite graph)."""
        n = 10
        G = nx.complete_graph(n)
        L = np.array(nx.laplacian_matrix(G).todense(), dtype=float)
        D = np.linalg.eigvalsh(L)
        dS, tau = compute_spectral_d(D, -2, 2, 100)
        # At large tau, dS → 0 for finite graphs
        assert dS[-1] < 0.5

    def test_compute_entropic_C_returns_correct_shape(self):
        D = np.array([0.0, 1.0, 2.5, 4.0])
        C, tau, S = compute_entropic_C(D, -1, 1, 50)
        assert len(C) == 49
        assert len(tau) == 49
        assert len(S) == 50

    def test_entropy_nonnegative(self):
        """Von Neumann entropy should be non-negative."""
        D = np.array([0.0, 1.0, 3.0, 5.0])
        _, _, S = compute_entropic_C(D, -1, 1, 30)
        assert np.all(S >= -1e-10)


# ---------------------------------------------------------------------------
# convert_graph_to_sc
# ---------------------------------------------------------------------------

class TestConvertGraphToSC:

    def test_triangle(self):
        G = nx.cycle_graph(3)
        G.add_edge(0, 2)  # already exists in cycle_graph(3)
        sc = convert_graph_to_sc(G, dim=2)
        assert sc["n0"] == 3
        assert sc["n1"] == 3
        assert sc["n2"] == 1  # one triangle

    def test_complete_graph_4(self):
        """K_4 has 4 triangular faces and 1 tetrahedron as its 3-clique complex."""
        G = nx.complete_graph(4)
        sc = convert_graph_to_sc(G, dim=3)
        assert sc["n0"] == 4
        assert sc["n1"] == 6
        assert sc["n2"] == 4
        assert sc["n3"] == 1
