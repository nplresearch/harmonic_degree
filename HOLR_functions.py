import networkx as nx
import numpy as np
import scipy.sparse as sp
from scipy.sparse import csr_matrix, lil_matrix, spdiags
from itertools import combinations
import matplotlib.pyplot as plt


def import_network_data(f):
    edges = []
    for i, line in enumerate(f):
        if i == 0:
            continue  # Skip the first line
        words = line.split()
        edges.append((words[0], words[1]))
    
    f.close()
    
    # Create an undirected graph from edge list
    G = nx.Graph()
    G.add_edges_from(edges)
    
    # Remove self-loops
    G.remove_edges_from(nx.selfloop_edges(G))
    
    # Extract the largest connected component
    largest_cc = max(nx.connected_components(G), key=len)
    G = G.subgraph(largest_cc).copy()
    
    # Relabel nodes in ascending order starting from 0
    G = nx.convert_node_labels_to_integers(G, ordering="sorted")
    
    return G



def NGF(d, N, s, beta, M = 1):
    # Generate a d-dimensional NGF simplicial complex
    # 
    # 
    if d > 4:
        print("Dimension out of bounds. NGF implemented only for d=1,2,3,4")

    kappa = 1
    epsilon = np.random.rand(N) ** (1 / (kappa + 1))
    a = sp.lil_matrix((N, N))
    at = np.array([])
    a_occ = np.array([])
    node = np.zeros(((d + 1) + (N - (d + 1)) * d, d), dtype=int)

    # Initial condition: at time t=1 a single d-dimensional simplex (1,2,3,4)
    for i in range(d + 1):
        for j in range(i + 1, d + 1):
            a[i, j] = 1
            a[j, i] = 1

    for nt in range(d + 1):
        at = np.append(at, 1)
        a_occ = np.append(a_occ, 1)
        j = -1
        for i in range(d + 1):
            if i != nt:
                j += 1
                node[nt, j] = i
                at[nt] = at[nt] * np.exp(-beta * epsilon[i])

    it = d  # + 1

    while it < N - 1:
        it += 1
        for m in range(M):
            mat = at * a_occ
            J = mat.nonzero()[0]
            V = np.squeeze(mat[mat.nonzero()])
            norm = np.sum(V)
            x = np.random.rand() * norm
            for nj1 in range(len(V)):
                x -= V[nj1]
                if x < 0:
                    nj = J[nj1] # Index of the d-1 simplex where the next simplex is attached
                    break

            a_occ[nj] = a_occ[nj] + s

            # Attach the next simplex
            for n1 in range(d): 
                j = node[nj, n1]
                a[it, j] = 1
                a[j, it] = 1

        for n1 in range(d): # d (d-1)-simplices are added
            nt += 1
            at = np.append(at, 1)
            a_occ = np.append(a_occ, 1)
            node[nt, 0] = it
            j = 0
            for n2 in range(d):
                if n2 != n1:
                    j += 1
                    node[nt, j] = node[nj, n2]
                    at[nt] = at[nt] * np.exp(-beta * epsilon[node[nj, n2]])
                    a[it, node[nj, n2]] = 1
                    a[node[nj, n2], it] = 1

    a = a > 0
    G = nx.from_numpy_array(a)
    cliques = list(nx.enumerate_all_cliques(G))
    faces = []
    tetrahedra = []
    four_simplexes = []
    for c in cliques:
        l = len(c)
        if l == 3:
            faces.append(c)
        elif l == 4:
            tetrahedra.append(c)
        elif l == 5:
            four_simplexes.append(c)

    sc = {
        "nodes": np.reshape(np.arange(0, N), (N, 1)),
        "edges": np.unique(
            np.sort(np.array(list(G.edges()), dtype=int), axis=1), axis=0
        ),
        "faces": np.unique(
            np.sort(np.reshape(np.array(faces, dtype=int), (-1, 3)), axis=1), axis=0
        ),
        "tetrahedra": np.unique(
            np.sort(np.reshape(np.array(tetrahedra, dtype=int), (-1, 4)), axis=1),
            axis=0,
        ),
        "4-simplices": np.unique(
            np.sort(np.reshape(np.array(four_simplexes, dtype=int), (-1, 5)), axis=1),
            axis=0,
        ),
    }
    sc["n0"] = N
    sc["n1"] = sc["edges"].shape[0]
    sc["n2"] = sc["faces"].shape[0]
    sc["n3"] = sc["tetrahedra"].shape[0]
    sc["n4"] = sc["4-simplices"].shape[0]

    return sc






# modified from HORL, to get directly a graph
def pseudofractal_d2_graph(steps):
    edges = [(0,1),(1,2),(0,2)]
    n = 3
    for s in range(steps):
        boundary = edges.copy()
        for ed in boundary:
            edges.append((ed[0],n))
            edges.append((ed[1],n))
            n += 1

    G = nx.from_edgelist(edges)
    return G


# Modified from HORL, to get directly a graph
def apollonian_d2_graph(steps):
    edges = [(0,1),(1,2),(0,2)]
    new_boundary = edges.copy()
    n = 3
    for s in range(steps):
        boundary = new_boundary
        new_boundary = []
        for ed in boundary:
            edges.append((ed[0],n))
            edges.append((ed[1],n))
            new_boundary.append((ed[0],n))
            new_boundary.append((ed[1],n))
            n += 1

    G = nx.from_edgelist(edges)
    return G

def convert_graph_to_sc(G, dim = 2, type = 'clique'):
    # Converts a graph G to its clique complex of dimension dim 
    # type: 'clique', 'inference'
    G = nx.convert_node_labels_to_integers(G)
    N = len(G.nodes)
    sc = {
        "nodes": np.reshape(np.array(G.nodes), (-1, 1)),
        "n0": N,
        "edges": np.sort(np.array(G.edges), 1),
    }
    all_cliques = list(nx.enumerate_all_cliques(nx.from_edgelist(sc["edges"])))
    sc["n1"] = len(sc["edges"])
    if type == 'clique':
        cliques = all_cliques
    # elif type == 'inference':
    #     g = gt.Graph(directed=False)
    #     g.add_edge_list(G.edges())
    #     state = gt.CliqueState(g)
    #     state.mcmc_sweep(niter=10000)
    #     cliques = []
    #     for v in state.f.vertices():      
    #         if state.is_fac[v]:
    #             continue          
    #         if state.x[v] > 0:
    #             cliques.append(list(state.c[v]))
    if dim >= 2:
        sc["faces"] = np.array([x for x in cliques if len(x) == 3])
    else:
        sc["faces"] = np.zeros((0, 3))
    if dim >= 3:
        sc["tetrahedra"] = np.array([x for x in cliques if len(x) == 4])
    else:
        sc["tetrahedra"] = np.zeros((0, 4))

    sc["4-simplices"] = np.zeros((0, 5))
    sc["n2"] = sc["faces"].shape[0]
    if sc["n2"] > 0:
        sc["faces"] = np.sort(sc["faces"], 1)
    sc["n3"] = sc["tetrahedra"].shape[0]
    if sc["n3"] > 0:
        sc["tetrahedra"] = np.sort(sc["tetrahedra"], 1)
    sc["n4"] = 0
    return sc


def pseudofractal_d3(steps):
    edges = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    faces = [(0,1,2),(0,1,3),(0,2,3),(1,2,3)]
    n = 4
    for s in range(steps):
        boundary = faces.copy()
        for fa in boundary:
            edges.append((fa[0],n))
            edges.append((fa[1],n))
            edges.append((fa[2],n))
            faces.append((fa[0],fa[1],n))
            faces.append((fa[0],fa[2],n))
            faces.append((fa[1],fa[2],n))
            n += 1

    G = nx.from_edgelist(edges)
    sc = convert_graph_to_sc(G,dim = 3)

    return sc

# Note, this is different from the one I wrote earlier, because it produces a sc
def apollonian_d2(steps):
    edges = [(0,1),(1,2),(0,2)]
    new_boundary = edges.copy()
    n = 3
    for s in range(steps):
        boundary = new_boundary
        new_boundary = []
        for ed in boundary:
            edges.append((ed[0],n))
            edges.append((ed[1],n))
            new_boundary.append((ed[0],n))
            new_boundary.append((ed[1],n))
            n += 1

    G = nx.from_edgelist(edges)
    sc = convert_graph_to_sc(G, dim = 2)

    return sc

# same of apollonian
def pseudofractal_d2(steps):
    edges = [(0,1),(1,2),(0,2)]
    n = 3
    for s in range(steps):
        boundary = edges.copy()
        for ed in boundary:
            edges.append((ed[0],n))
            edges.append((ed[1],n))
            n += 1

    G = nx.from_edgelist(edges)
    sc = convert_graph_to_sc(G,dim = 2)
    return sc



def compute_entropic_C(D, exm, exM, n_t):
    # Computes the Von Neumann entropy and Entropic susceptibility of a given Laplacian
    # INPUTS
    # D: list of eigenvalues of the Laplacian matrix considered
    # exm, exM, n_t: computes the quantities in n_t logarithmically spaced time points
    #  in the interval [10**exm,10**exM] 

    # OUTPUTS
    # specific_heat: numpy array containing the entropic susceptibility values
    # tau_space: numpy array containing n_t - 1 logarithmically spaced time points
    # S: numpy array containing the Von Neumann entropy

    N = len(D)
    D = np.abs(D)
    tau_space = np.logspace(exm, exM, num=n_t)
    S = np.zeros(n_t)
    for t in range(n_t):
        tau = tau_space[t]
        mu = np.zeros(N)
        for i in range(N):
            mu[i] = 1 / np.sum(np.exp(-tau * (D - D[i])))

        mu = mu[mu > 0]
        S[t] = -np.sum(mu * np.log(mu))
    entropic_susceptibility = -(np.diff(S) / np.diff(np.log(tau_space)))
    tau_space = tau_space[: n_t - 1]
    return entropic_susceptibility, tau_space, S

def compute_spectral_d(D,exm,exM,n_t):
    # Computes the spectral dimension associated to a diffusion process
    # INPUTS
    # D: eigenvalues of the Laplacian matrix considered
    # exm, exM, n_t: computes the spectral dimension in n_t logarithmically spaced time points
    #  in the interval [10**exm,10**exM] 

    # OUTPUTS
    # dS: numpy array containing the spectral dimension values
    # tau_space: numpy array containing n_t - 1 logarithmically spaced time points

    tau_space = np.logspace(exm, exM, num=n_t)
    Z = np.zeros(n_t)
    for t in range(n_t):
        Z[t] = np.sum(np.exp(- tau_space[t]*D))

    dS = -2*np.diff(np.log(Z))/np.diff(np.log(tau_space))

    return dS, tau_space[1:]


def make_dict_ext(sc):
    edge_dict = {}
    for i, edge in enumerate(sc["edges"]):
        # Create a tuple to represent the edge (order doesn't matter)
        edge_key = tuple(sorted(edge))
        # Store the edge index in the dictionary
        edge_dict[edge_key] = i

    face_dict = {}
    for i, face in enumerate(sc["faces"]):
        # Create a tuple to represent the face (order doesn't matter)
        face_key = tuple(sorted(face))
        # Store the edge index in the dictionary
        face_dict[face_key] = i

    tet_dict = {}
    for i, tetrahedron in enumerate(sc["tetrahedra"]):
        # Create a tuple to represent the tetrahedron (order doesn't matter)
        tet_key = tuple(sorted(tetrahedron))
        # Store the edge index in the dictionary
        tet_dict[tet_key] = i
        
    
    node_dict=tuple(sc["nodes"].tolist())

    return node_dict, edge_dict, face_dict, tet_dict



def boundary_matrices_ext(sc):
    # Compute bounadry matrices up to the 4-th order
    n0 = sc["n0"]
    n1 = sc["n1"]
    n2 = sc["n2"]
    n3 = sc["n3"]
    n4 = sc["n4"]
    
    B1 = lil_matrix((n0, n1), dtype=np.int8)
    B2 = lil_matrix((n1, n2), dtype=np.int8)
    B3 = lil_matrix((n2, n3), dtype=np.int8)
    B4 = lil_matrix((n3, n4), dtype=np.int8)

    node_dict, edge_dict, face_dict, tet_dict = make_dict_ext(sc)

    for e in range(n1):
        nodes = sc["edges"][e, :]
        B1[nodes[0], e] = -1
        B1[nodes[1], e] = 1

    for face_idx, face in enumerate(sc["faces"]):
        # Iterate over the three edges of the face
        for i in range(3):
            # Determine the start and end nodes of the edge
            edge = face[np.arange(3) != i]

            # Find the corresponding edge index in the edges list
            edge_idx = edge_dict[tuple(sorted(edge))]
            # Set the appropriate entry in `boundary_2`
            B2[edge_idx, face_idx] = (-1) ** i

    for tetra_idx, tetrahedron in enumerate(sc["tetrahedra"]):
        # Iterate over the four faces of the tetrahedron
        for i in range(4):
            # Determine the three nodes of the face
            face = tetrahedron[np.arange(4) != i]

            # Find the corresponding face index in the faces list
            face_idx = face_dict[tuple(sorted(face))]

            # Set the appropriate entry in `boundary_3`
            B3[face_idx, tetra_idx] = (-1) ** i

    for four_simp_idx, four_simplex in enumerate(sc["4-simplices"]):
        # Iterate over the four tetrahedra of the 4-simplex
        for i in range(5):
            # Determine the four nodes of the tetrahedron
            tetrahedron = four_simplex[np.arange(5) != i]

            # Find the corresponding tetrahedron index in the tetrahedra list
            tet_idx = tet_dict[tuple(sorted(tetrahedron))]

            # Set the appropriate entry in `boundary_3`
            B4[tet_idx, four_simp_idx] = (-1) ** i

    B1 = B1.tocsc()
    B2 = B2.tocsc()
    B3 = B3.tocsc()
    B4 = B4.tocsc()

    return B1, B2, B3, B4, node_dict, edge_dict, face_dict, tet_dict


def laplacians(sc):
    B1, B2, B3, B4, node_dict, edge_dict, face_dict, tet_dict=boundary_matrices_ext(sc)
    B1=B1.toarray()
    B2=B2.toarray()
    B3=B3.toarray()
    B4=B4.toarray()
    L0=np.dot(B1,B1.T)
    L1=np.dot(B1.T,B1)+np.dot(B2,B2.T)
    L2=np.dot(B2.T,B2)+np.dot(B3,B3.T)
    L3=np.dot(B3.T,B3)+np.dot(B4,B4.T)
    L4=np.dot(B4.T,B4)
    return L0, L1, L2, L3, L4, node_dict, edge_dict, face_dict, tet_dict



def adjacency_of_order(sc,k,l, sparse = False):
    # sc: simplicial complex object
    # k: order of the diffusing simplices
    # l: order of the interaction simplices

    keys = ["nodes", "edges", "faces", "tetrahedra", "4-simplices"]
    nk = sc[f"n{k}"]
    if sparse:
        adj = lil_matrix((nk,nk), dtype = int)
    else:
        adj = np.zeros((nk,nk),dtype = int)
    
    assert l != k, "The interaction order should be different from the order of the diffusing simplices"
    assert l >= 0, "The interaction order should be greater or equal than 0"
    assert k >= 0, "The order of the diffusing simplices should be greater or equal than 0"
    assert (l <= 4) and (k <= 4), "Simplices of order greater than 4 are not supported"


    if l < k: 
        diff_units = sc[keys[k]]
        for i in range(nk):
            for j in range(i+1,nk):
                intersection = (set(diff_units[i,:]) & set(diff_units[j,:]))
                if len(intersection) == l + 1:
                    adj[i,j] += 1

    elif l > k:
        edge_dict, face_dict, tet_dict = make_dict_ext(sc)
        dicts = [{(i,):i for i in range(sc["n0"])},edge_dict,face_dict,tet_dict]
        int_simplices = sc[keys[l]]

        for i in range(sc[f"n{l}"]):
            simp = int_simplices[i,:]
            combs = list(combinations(simp, k+1))
            ncombs = len(combs)
            combs_ids = np.zeros(ncombs,dtype=int)
            for n in range(ncombs):
                combs_ids[n] = dicts[k][combs[n]]
            combs_ids = np.sort(combs_ids)
            for n in range(ncombs):
                for m in range(n+1,ncombs):
                    adj[combs_ids[n],combs_ids[m]] += 1

    if sparse:
        adj = csr_matrix(adj)

    return adj + adj.T

def XO_laplacian(sc,k,l, sparse = False):
    A = adjacency_of_order(sc,k,l,sparse)
    K = np.sum(A, 0)
    if sparse:
        lenK = K.shape[1]
        L = spdiags(K,0,lenK,lenK) - A
    else:
        L = np.diag(K) - A
    return L



SMALL_SIZE = 10
MEDIUM_SIZE = 12
BIGGER_SIZE = 13

plt.rc("font", size=SMALL_SIZE)  # controls default text sizes
plt.rc("axes", titlesize=SMALL_SIZE)  # fontsize of the axes title
plt.rc("axes", labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
plt.rc("xtick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc("ytick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc("legend", fontsize=SMALL_SIZE)  # legend fontsize
plt.rc("figure", titlesize=BIGGER_SIZE)  # fontsize of the figure title


def plot_complex(
    sc,
    ax,
    node_color=["black"],
    edge_color=["black"],
    face_color=["black"],
    face_alpha=0.2,
    edge_alpha=1,
    edge_width=1,
    with_labels=False,
    layout="spring",
    pos = None,
    node_size=10,
    iterations=1000,
):
    # Plots a simplicial complex
    # INPUTS
    # sc: simplicial complex object
    # ax: axis where to plot
    # node_color: list of the node colors
    # edge_color: list of the edge colors
    # face_color: list of the face colors
    # face_alpha: opacity of the faces
    # edge_alpha: opacity of the edges
    # edge_width: width of the edges
    # layout: the layout of the underlying graph. Can be "spring", "circle", "spectral" or "kamada_kawai"
    # pos: pre-computed node positions layout
    # node_size: size of the nodes
    # itrations: the number of iterations with which the "spring" layout is computed

    if sc["n1"] == 0:
        G = nx.Graph()
        G.add_nodes_from(range(sc["n0"]))
        nx.draw_networkx(
            G,
            pos=nx.spring_layout(G),
            node_color=node_color,
            alpha=edge_alpha,
            node_size=200,
            with_labels=False,
            edge_color="k",
            linewidths=1,
            ax=ax,
        )
        ax.axis("off")
    else:
        if len(face_color) == 1:
            face_color = [face_color[0] for i in range(sc["n2"])]

        G = nx.Graph()
        G.add_nodes_from([i for i in range(sc["n0"])])
        G.add_edges_from(sc["edges"])
        
        if pos == None:
            if layout == "spring":
                pos = nx.spring_layout(G, iterations=iterations)
            elif layout == "circle":
                pos = nx.circular_layout(G)
            elif layout == "spectral":
                pos = nx.spectral_layout(G)
            elif layout == "kamada_kawai":
                pos = nx.kamada_kawai_layout(G)
                    
        for i in range(sc["n2"]):
            f = sc["faces"][i, :]
            pf0 = pos[f[0]]
            pf1 = pos[f[1]]
            pf2 = pos[f[2]]
            x = [pf0[0], pf1[0], pf2[0]]
            y = [pf0[1], pf1[1], pf2[1]]
            ax.fill(x, y, color=face_color[i], alpha=face_alpha)

        nx.draw_networkx(
            G,
            pos=pos,
            node_color=node_color,
            alpha=edge_alpha,
            node_size=node_size,
            with_labels=with_labels,
            width=edge_width,
            edge_color=edge_color,
            linewidths=1,
            ax=ax,
        )
        # plt.hold(True)
        ax.axis("off")
        # ax.draw()




