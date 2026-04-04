"""Shared fixtures for harmonic_morphisms tests."""

import networkx as nx
import numpy as np
import pytest
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@pytest.fixture
def path_graph_10():
    """P_10 path graph with Laplacian."""
    G = nx.path_graph(10)
    L = np.array(nx.laplacian_matrix(G).todense(), dtype=float)
    return G, L


@pytest.fixture
def karate_graph():
    """Karate club graph with Laplacian."""
    G = nx.karate_club_graph()
    L = np.array(nx.laplacian_matrix(G, nodelist=sorted(G.nodes())).todense(), dtype=float)
    return G, L


@pytest.fixture
def k33_harmonic():
    """K_{3,3} with 2-partition clustering — a known exact harmonic morphism.

    Collapsing each partition of K_{3,3} to a single supernode gives K_2.
    Every node sees exactly 3 neighbors in the other partition and 0 in its own,
    so the cardinality list is uniform → perfect harmonic morphism.
    """
    G = nx.complete_bipartite_graph(3, 3)
    clusters = {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1}
    return G, clusters


@pytest.fixture
def pf2_small():
    """Pseudofractal d=2, 2 iterations (small, fast)."""
    from harmonic_morphisms.simplicial import pseudofractal_d2
    return pseudofractal_d2(2)


@pytest.fixture
def data_dir():
    return DATA_DIR
