"""Smoke tests: imports and basic wiring."""


def test_version_is_string():
    from harmonic_morphisms import __version__
    assert isinstance(__version__, str)
    assert "." in __version__


def test_core_imports():
    from harmonic_morphisms import (
        H_CF_cluster,
        H_CF_curves,
        simple_renorm,
        renorm_graph_harmonic,
        renorm_graph_plot,
        clust_plot,
        iter_g,
        iter_narrow_g,
        h_v,
        g_len,
    )


def test_higher_order_imports():
    from harmonic_morphisms import (
        higher_order_renormalization,
        higher_order_renormalization_series,
        higher_order_H_CF_curves,
        iter_g_higher_order,
        iter_narrow_g_higher_order,
        fbc,
    )


def test_simplicial_submodule_imports():
    from harmonic_morphisms.simplicial import (
        import_network_data,
        NGF,
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
        make_dict_ext,
        plot_complex,
    )


def test_higher_order_submodule_imports():
    from harmonic_morphisms.higher_order import (
        fbc,
        higher_order_renormalization,
        higher_order_renormalization_series,
        higher_order_H_CF_curves,
        iter_g_higher_order,
        iter_narrow_g_higher_order,
    )
