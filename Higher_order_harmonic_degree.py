import networkx as nx
import numpy as np
import scipy.linalg
import matplotlib.colors as mcolors
from  HOLR_functions import adjacency_of_order
from Harmonic_degree import H_CF_cluster

# Forman Bochner Decomposition
def fbc(L):
    l=L.shape[0]
    B=np.dot(np.eye(l),L)
    for i in range(l):
        B[i,i]=np.sum(np.abs(L[i,:]))-np.abs(L[i,i])
    B=B.astype(int)
    F=L-B
    return B , F

# Higher Order Renormalization
def higher_order_renormalization(sc,t,dim,Lap, tresh=0):
    # sc is the simplicial complex
    # t is the time I want the clustering
    # dim is the dimension I want the clustering
    ### I am modifying the merging criteria, since rho_.J is exp(-tL) e_j , now I am doing exp(-tL) Proj_{Orthogonal of the Kernel}(e_j)
    # then I consider the average in absolute values between rho_ij and rho_ji
    
    A=adjacency_of_order(sc,k=dim,l=dim-1)
    # making the adj graph
    Ag=nx.Graph()
    Ag.add_nodes_from([i for i in range(sc[f"n{dim}"])])
    for i in range(A.shape[0]):
        for j in range(A.shape[0]):
            if (i !=j and A[i,j]!=0):
                Ag.add_edge(i,j)

    if dim==0:
        title = "nodes"
    if dim == 1:
        title = "edges"
    if dim == 2:
        title = "faces"
    if dim ==3:
        title = "tetrahedra"
    if dim ==4:
        title = "4-simplices"

    eigvals, eigvecs = np.linalg.eigh(Lap)

    kernel_threshold = 1e-7
    ker_indices = np.where(np.abs(eigvals) < kernel_threshold)[0]
    ker_basis = eigvecs[:, ker_indices]

    # Projection into orthogonal of kernel
    P_perp = np.eye(Lap.shape[0]) - ker_basis @ ker_basis.T

    # Diffusing the non harmonic component
    rho = np.zeros_like(Lap, dtype=float)
    for j in range(Lap.shape[1]):
        e_j = np.zeros(Lap.shape[1])
        e_j[j] = 1.0
        v = P_perp @ e_j                
        u = scipy.linalg.expm(-t * Lap) @ v   
        rho[:, j] = u                         
    # In this setting the density is useless and has not the interpretation anymore as density matrix
    #density = rho / np.trace(rho)  

    Gv = nx.Graph()
    labels = {}
    n_nodes = sc[f"n{dim}"]
    Gv.add_nodes_from(range(n_nodes))

    for i in range(n_nodes):
        for j in range(i+1, n_nodes):
            avg_val = (np.abs(rho[i, j]) + np.abs(rho[j, i])) / 2
            if avg_val >= min(np.abs(rho[i, i]), np.abs(rho[j, j])) - tresh:
                Gv.add_edge(i, j)
        ob_i = sc[title][i]
        labels[i] = f"{ob_i}".replace("[", "").replace("]", "")

    # Compute connected components and store in clusters dictionary
    idx_components = {u: i for i, node_set in enumerate(nx.connected_components(Gv)) for u in node_set}
    clusters = {node: idx_components[node] for node in Gv.nodes()}  # Ensure clusters use Ag node labels
    #print(clusters)

    clist = list(mcolors.CSS4_COLORS.values()) * 10
    np.random.shuffle(clist)

    # Assign colors to clusters correctly
    cluster_ids = sorted(set(clusters.values()))  # Unique cluster IDs
    cluster_to_color = {cid: clist[i] for i, cid in enumerate(cluster_ids)}
    # Extract unique colors for clusters
    sing_col = [cluster_to_color[cid] for cid in cluster_ids]
    colors = {node: cluster_to_color[clusters[node]] for node in clusters}

    G, deg_h, M_deg_h, std_h, av_h, std_v_h, Not_h, deg_cf, M_deg_cf, std_cf, av_cf, std_v_cf, Not_cf = H_CF_cluster(Ag,clusters)
    return Ag,G, deg_h, M_deg_h, std_h, av_h, std_v_h, Not_h, deg_cf, M_deg_cf, std_cf, av_cf, std_v_cf, Not_cf, Gv, sing_col, colors
            



# Higher Order Renormalization Series
def higher_order_renormalization_series(sc,t_span,dim,Lap,tresh=0):
    g=[]
    DEG_H = []
    M_DEG_H = []
    STD_H = []
    AV_H = []
    STD_V_H = []
    NOT_H = []
    DEG_CF = []
    M_DEG_CF = []
    STD_CF = []
    AV_CF = []
    STD_V_CF = []
    NOT_CF = []
    gV = []
    
    for t in t_span:
        Ag,G, deg_h, M_deg_h, std_h, av_h, std_v_h, Not_h, deg_cf, M_deg_cf, std_cf, av_cf, std_v_cf, Not_cf, Gv, sing_col, colors=higher_order_renormalization(sc,t,dim,Lap,tresh)
        g.append(G)
        DEG_H.append(deg_h)
        M_DEG_H.append(M_deg_h)
        STD_H.append(std_h)
        AV_H.append(av_h)
        STD_V_H.append(std_v_h)
        NOT_H.append(Not_h)
        DEG_CF.append(deg_cf)
        M_DEG_CF.append(M_deg_cf)
        STD_CF.append(std_cf)
        AV_CF.append(av_cf)
        STD_V_CF.append(std_v_cf)
        NOT_CF.append(Not_cf)
        gV.append(Gv)
        
        
    return Ag, g, DEG_H, M_DEG_H, STD_H, AV_H, STD_V_H, NOT_H, DEG_CF, M_DEG_CF, STD_CF, AV_CF, STD_V_CF, NOT_CF, gV


# Function to find the t where the renormalized graph has 1 nodes
def iter_g_higher_order(sc,dim,Lap,tresh=0):
    A=adjacency_of_order(sc,k=dim,l=dim-1)
    # making the adj graph
    Ag=nx.Graph()
    Ag.add_nodes_from([i for i in range(sc[f"n{dim}"])])
    for i in range(A.shape[0]):
        for j in range(A.shape[0]):
            if (i !=j and A[i,j]!=0):
                Ag.add_edge(i,j)
    N=nx.number_connected_components(Ag)
    t=0.0
    l=0
    while((t<500) and (l!= N)):
        t=t+1.0
        G = higher_order_renormalization(sc,t,dim,Lap,tresh)[1]
        l=len(G.nodes())
    return t

# Function to find the narrowest t where the renormalized graph has 1 nodes
def iter_narrow_g_higher_order(sc,dim,Lap,tresh=0):
    A=adjacency_of_order(sc,k=dim,l=dim-1)
    # making the adj graph
    Ag=nx.Graph()
    Ag.add_nodes_from([i for i in range(sc[f"n{dim}"])])
    for i in range(A.shape[0]):
        for j in range(A.shape[0]):
            if (i !=j and A[i,j]!=0):
                Ag.add_edge(i,j)
    N = nx.number_connected_components(Ag)
    t_i=iter_g_higher_order(sc,dim,Lap,tresh)
    t=t_i-1.0
    l=0
    while((t<= t_i) and (l!=N)):
        t=t+0.1
        G= higher_order_renormalization(sc,t,dim,Lap,tresh)[1]
        l=len(G.nodes())
    return round(t,1)


# Main function to compute higher order harmonicity and conformality curves
def higher_order_H_CF_curves(sc,dim,Lap,n,tresh=0):
    t_f=iter_narrow_g_higher_order(sc,dim,Lap,tresh)
    t_i=0
    t_span=np.linspace(t_i,t_f,n)
    Ag, g, DEG_H, M_DEG_H, STD_H, AV_H, STD_V_H, NOT_H, DEG_CF, M_DEG_CF, STD_CF, AV_CF, STD_V_CF, NOT_CF, gV = higher_order_renormalization_series(sc,t_span,dim,Lap,tresh=0)
    return Ag, g, DEG_H, M_DEG_H, STD_H, AV_H, STD_V_H, NOT_H, DEG_CF, M_DEG_CF, STD_CF, AV_CF, STD_V_CF, NOT_CF, gV, t_span






