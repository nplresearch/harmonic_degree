"""Unit tests for harmonic_morphisms.higher_order."""

import numpy as np
import pytest

from harmonic_morphisms.higher_order import fbc, higher_order_renormalization
from harmonic_morphisms.simplicial import pseudofractal_d2, laplacians, XO_laplacian


# ---------------------------------------------------------------------------
# Forman-Bochner decomposition
# ---------------------------------------------------------------------------

class TestFBC:

    def test_decomposition_sums_to_original(self, pf2_small):
        """B + F = L (Bochner + curvature = original Laplacian)."""
        _, L1, *_ = laplacians(pf2_small)
        B, F = fbc(L1)
        np.testing.assert_array_equal(B + F, L1)

    def test_bochner_positive_semidefinite(self, pf2_small):
        """The Bochner part B should be positive semi-definite."""
        _, L1, *_ = laplacians(pf2_small)
        B, F = fbc(L1)
        eigvals = np.linalg.eigvalsh(B.astype(float))
        assert np.all(eigvals >= -1e-10), f"Negative eigenvalue: {eigvals.min()}"

    def test_bochner_diagonal_is_row_abs_sum(self, pf2_small):
        """By construction, B[i,i] = sum(|L[i,:]|) - |L[i,i]|."""
        _, L1, *_ = laplacians(pf2_small)
        B, F = fbc(L1)
        for i in range(L1.shape[0]):
            expected = np.sum(np.abs(L1[i, :])) - np.abs(L1[i, i])
            assert B[i, i] == pytest.approx(expected)

    def test_curvature_diagonal_only(self, pf2_small):
        """F = L - B should only have nonzero entries on the diagonal."""
        _, L1, *_ = laplacians(pf2_small)
        B, F = fbc(L1)
        off_diag = F.copy()
        np.fill_diagonal(off_diag, 0)
        np.testing.assert_array_equal(off_diag, 0)

    def test_works_on_L2(self, pf2_small):
        """FBC should also work on L2."""
        _, _, L2, *_ = laplacians(pf2_small)
        B, F = fbc(L2)
        np.testing.assert_array_equal(B + F, L2)


# ---------------------------------------------------------------------------
# Higher-order renormalization
# ---------------------------------------------------------------------------

class TestHigherOrderRenormalization:

    def test_t_zero_no_merging(self, pf2_small):
        """At t=0, no diffusion → no merging → same number of faces."""
        sc = pf2_small
        _, _, L2, *_ = laplacians(sc)
        result = higher_order_renormalization(sc, t=0.0, dim=2, Lap=L2, tresh=0)
        # result[0] = Ag (adjacency graph of faces), result[1] = G (coarse graph)
        Ag = result[0]
        G_coarse = result[1]
        assert G_coarse.number_of_nodes() == sc["n2"]

    def test_large_t_collapses(self, pf2_small):
        """Large t should merge some faces."""
        sc = pf2_small
        _, _, L2, *_ = laplacians(sc)
        result = higher_order_renormalization(sc, t=50.0, dim=2, Lap=L2, tresh=0)
        G_coarse = result[1]
        assert G_coarse.number_of_nodes() < sc["n2"]

    def test_returns_17_values(self, pf2_small):
        sc = pf2_small
        _, _, L2, *_ = laplacians(sc)
        result = higher_order_renormalization(sc, t=1.0, dim=2, Lap=L2, tresh=0)
        assert len(result) == 17

    def test_harmonic_degrees_in_range(self, pf2_small):
        """Harmonic/conformal degrees should be in [0, 1]."""
        sc = pf2_small
        _, _, L2, *_ = laplacians(sc)
        result = higher_order_renormalization(sc, t=1.0, dim=2, Lap=L2, tresh=0)
        # result indices: 2=deg_h, 3=M_deg_h, 8=deg_cf, 9=M_deg_cf
        deg_h, M_deg_h = result[2], result[3]
        deg_cf, M_deg_cf = result[8], result[9]
        for val in [deg_h, M_deg_h, deg_cf, M_deg_cf]:
            assert 0.0 <= val <= 1.0

    def test_works_with_xo_laplacian(self, pf2_small):
        """Should also work with cross-order Laplacian."""
        sc = pf2_small
        X2 = XO_laplacian(sc, k=2, l=1)
        result = higher_order_renormalization(sc, t=1.0, dim=2, Lap=X2, tresh=0)
        assert len(result) == 17
