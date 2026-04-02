import networkx as nx
import numpy as np
import scipy.linalg
import matplotlib.colors as mcolors


# Function to compute harmonicity and conformality measures for a given clustering of the graph
def H_CF_cluster(Ag,clusters):

    """
    Computes harmonic and conformal degrees for a given clustering of the graph.

    This function evaluates how well a coarse-graining preserves harmonicity and conformality
    by analyzing the map between the original graph and the coarse-grained graph.

    Parameters
    ----------
    Ag : networkx.Graph
        The original graph.
    clusters : dict
        A dictionary mapping each node in Ag to its cluster ID.

    Returns
    -------
    G : networkx.Graph
        The coarse-grained graph derived from the clustering.
    deg_h : float
        Mean harmonic degree across all nodes.
    M_deg_h : float
        Modified harmonic degree, mean of average harmonic degrees per cluster.
    std_h : float
        Harmonic deviation, mean standard deviation of cardinalities in horizontal spaces.
    av_h : list of float
        List of average harmonic degrees for each cluster.
    std_v_h : list of float
        List of standard deviations of cardinalities in horizontal spaces per node.
    Not_h : list of int
        List of nodes in the original graph that are not harmonic.
    deg_cf : float
        Mean conformal degree across all nodes.
    M_deg_cf : float
        Modified conformal degree, mean of average conformal degrees per cluster.
    std_cf : float
        Conformal deviation, mean standard deviation of cardinalities in horizontal and vertical spaces.
    av_cf : list of float
        List of average conformal degrees for each cluster.
    std_v_cf : list of float
        List of standard deviations of cardinalities in combined spaces per node.
    Not_cf : list of int
        List of nodes in the original graph that are not conformal.
"""
    

    # create the graph from the correspondence as if in the coarse-graining procedure
    G=nx.Graph()
    G.add_nodes_from([h for h in set(clusters.values())])
    for o in Ag.nodes():
        for p in Ag.nodes():
            if(Ag.has_edge(o,p) and clusters[o]!=clusters[p]):
                G.add_edge(clusters[o],clusters[p]) 

    # Not_h = list of non harmonic elements
    Not_h=[]
    # initializing number of harmonic elements
    num_h=0
    # list of harmonic degree averages per node in the counterimage
    av_h=[]
    # list of variance per node in the counterimage
    std_v_h=[]

    # Doing the same for conformal
    Not_cf=[]
    num_cf = 0
    av_cf= []
    std_v_cf=[]

    # now we are considering harmonicity, horizontal conformality
    # for every i in G
    for i in G.nodes():

        # num_i_h measures the harmonic nodes of the counter image of i
        num_i_h = 0

        # same for conformal 
        num_i_cf = 0
        
        # inv_im is the number of nodes in the counter image
        inv_im=0
        # for every j in phi^{-1}(i)
        for j in Ag.nodes():
            if(clusters[j]==i):
                inv_im=inv_im+1
                c_list=[]
                # for every k in the nieghbors of i
                for k in G.neighbors(i):
                    card=0
                    # counting nodes in the counterimage of the k that are linked to i, this is the horizontal conformality definition
                    for l in Ag.nodes():
                        if(clusters[l]==k and Ag.has_edge(j,l) and l!=j):
                            card=card+1
                    c_list.append(card)

                # variance of the list of cardinalities, we have only horizontal space here
                if (len(c_list)==0):
                    std_j_h=0
                else:
                    std_j_h= np.std(c_list)
                                   
                # variance for node j, horizontal space
                std_v_h.append(std_j_h)

                # harmonic degree
                # the condition len(set(c_list))==0) is never encountered here
                if(len(set(c_list))==1 or len(set(c_list))==0):
                    num_h=num_h+1
                    num_i_h=num_i_h+1
                else:
                    Not_h.append(j)
                    
                # Now we consider vertical space, fixing i and the node of the counterimage j
                # we simply add the cardinality of the vertical space on the existing c_list, that collects cardinalities
                # we update c_list by adding vertical space
                card_i=1
                for y in Ag.neighbors(j):
                    if (clusters[y]==i):
                        card_i=card_i+1
                c_list.append(card_i)
            
                if(np.std(c_list)==0):
                    num_cf=num_cf+1
                    num_i_cf=num_i_cf+1
                else:
                    Not_cf.append(j)
                

                # variance of the list of cardinalities, we have also added vertical space here
                if (len(c_list)==0):
                    std_j_cf=0
                else:
                    std_j_cf= np.std(c_list)
                std_v_cf.append(std_j_cf)


        
         # calculating the harmonic degree for single node i of the image and collecting it in av_h
        deg_i_h=num_i_h/inv_im
        av_h.append(deg_i_h)

        # calculating the conformal degree for single node i of the image and collectin it in av_cf
        deg_cf_mod=num_i_cf/inv_im
        av_cf.append(deg_cf_mod)
                   
    # calculating mean harmonic degree                    
    deg_h=num_h/len(Ag.nodes())

    # calculating std of cardinalities of horizontal space
    std_h=np.mean(std_v_h)

    # Modified harmonic degree
    M_deg_h = np.mean(av_h)

    # calculating mean conformal degree                    
    deg_cf=num_cf/len(Ag.nodes())

    # calculating std of cardinalities of both horizontal and vertical spaces
    std_cf=np.mean(std_v_cf)

    # Modified harmonic degree
    M_deg_cf = np.mean(av_cf)


    
    return G, deg_h, M_deg_h, std_h, av_h, std_v_h, Not_h, deg_cf, M_deg_cf, std_cf, av_cf, std_v_cf,  Not_cf

# Function to plot clusters
def clust_plot(Ag,clusters):
    """
    Generates a coarse-grained graph and color mappings for visualizing clusters.
    Parameters
    ----------
    Ag : networkx.Graph
        The original graph.
    clusters : dict
        A dictionary mapping each node in Ag to its cluster ID.

    Returns
    -------
    G : networkx.Graph
        The coarse-grained graph where nodes represent clusters.
    colors : dict
        A dictionary mapping each original node to its assigned color based on cluster.
    sing_col : list
        A list of unique colors corresponding to each cluster ID, hence nodes in the coarse-grained graph.
    """

    clist = list(mcolors.CSS4_COLORS.values()) * 10
    np.random.shuffle(clist)

    # Assign colors to clusters correctly
    cluster_ids = sorted(set(clusters.values()))  # Unique cluster IDs
    cluster_to_color = {cid: clist[i] for i, cid in enumerate(cluster_ids)}


    G=nx.Graph()
    G.add_nodes_from([h for h in cluster_ids])
    for o in Ag.nodes():
        for p in Ag.nodes():
            if(Ag.has_edge(o,p) and clusters[o]!=clusters[p]):
                G.add_edge(clusters[o],clusters[p])   
 

    # Extract unique colors for clusters
    sing_col = [cluster_to_color[cid] for cid in cluster_ids]
    colors = {node: cluster_to_color[clusters[node]] for node in clusters}

    return G, colors, sing_col



# Simple renormalization function that returns the renormalized graph
def simple_renorm(Ag,t,Lap,tresh = 0):
    """
    Performs Laplacian graph renormalization at a time t.

    Parameters
    ----------
    Ag : networkx.Graph
        The original graph.
    t : float
        The time parameter for the renormalization process.
    Lap : numpy.ndarray
        The Laplacian matrix of the graph.
    tresh : float, optional
        Threshold for edge creation in the metagraph (default is 0).

    Returns
    -------
    G : networkx.Graph
        The renormalized coarse-grained graph.
    """
    rho= scipy.linalg.expm(-t*Lap)
    # Compute metagraph
    Gv = nx.Graph()
    Gv.add_nodes_from(Ag.nodes())
    for i in range(len(Ag.nodes())):
        for j in range(i+1,len(Ag.nodes)):
            if np.abs(rho[i,j]) >= min(np.abs(rho[i,i]),np.abs(rho[j,j]))-tresh:
                Gv.add_edge(list(Ag.nodes())[i],list(Ag.nodes())[j])
    # Compute connected components and store in clusters dictionary
    idx_components = {u: i for i, node_set in enumerate(nx.connected_components(Gv)) for u in node_set}
    clusters = {node: idx_components[node] for node in Gv.nodes()}  # Ensure clusters use Ag node labels
    cluster_ids = sorted(set(clusters.values()))  # Unique cluster IDs
    G=nx.Graph()
    G.add_nodes_from([h for h in cluster_ids])
    for o in Ag.nodes():
        for p in Ag.nodes():
            if(Ag.has_edge(o,p) and clusters[o]!=clusters[p]):
                G.add_edge(clusters[o],clusters[p])   
    return G

# Renormalization function that also returns the plot of the renormalized graph
def renorm_graph_plot(Ag,t,Lap,tresh=0):
    """
    Performs graph renormalization and prepares data for plotting the result.

    This function renormalizes the graph and generates color mappings for visualizing
    the coarse-grained structure.

    Parameters
    ----------
    Ag : networkx.Graph
        The original graph.
    t : float
        The time parameter for the renormalization process.
    Lap : numpy.ndarray
        The Laplacian matrix of the graph.
    tresh : float, optional
        Threshold for edge creation in the metagraph (default is 0).
    Returns
    -------
    G : networkx.Graph
        The renormalized coarse-grained graph.
    colors : dict
        A dictionary mapping each original node to its assigned color based on cluster.
    sing_col : list
        A list of unique colors corresponding to each cluster ID.
    """
    rho= scipy.linalg.expm(-t*Lap)
    # Compute metagraph
    Gv = nx.Graph()
    Gv.add_nodes_from(Ag.nodes())
    for i in range(len(Ag.nodes())):
        for j in range(i+1,len(Ag.nodes)):
            if np.abs(rho[i,j]) >= min(np.abs(rho[i,i]),np.abs(rho[j,j]))-tresh:
                Gv.add_edge(list(Ag.nodes())[i],list(Ag.nodes())[j])
    # Compute connected components and store in clusters dictionary
    idx_components = {u: i for i, node_set in enumerate(nx.connected_components(Gv)) for u in node_set}
    clusters = {node: idx_components[node] for node in Gv.nodes()}  # Ensure clusters use Ag node labels
    # Plot
    G, colors, sing_col = clust_plot(Ag,clusters)
    return G, colors, sing_col


# Renormalization function that also computes harmonicity and conformality measures
def renorm_graph_harmonic(Ag,t,Lap,tresh=0):
    """
    Performs Laplacian graph renormalization and computes harmonicity and conformality measures.

    This function applies renormalization and evaluates the harmonic and conformal
    degrees of the resulting clustering.

    Parameters
    ----------
    Ag : networkx.Graph
        The original graph.
    t : float
        The time parameter for the exponential decay.
    Lap : numpy.ndarray
        The Laplacian matrix of the graph.
    tresh : float, optional
        Threshold for edge creation in the metagraph (default is 0).
    Returns
    -------
    G : networkx.Graph
        The coarse-grained graph derived from the clustering.
    deg_h : float
        Mean harmonic degree.
    M_deg_h : float
        Modified harmonic degree.
    std_h : float
        Harmonic deviation.
    av_h : list of float
        List of average harmonic degrees for each cluster.
    std_v_h : list of float
        List of standard deviations of cardinalities for horizontal spaces per node.
    Not_h : list of int
        List of nodes in the original graph that are not harmonic.
    deg_cf : float
        Mean conformal degree across all nodes.
    M_deg_cf : float
        Modified conformal degree, mean of average conformal degrees per cluster.
    std_cf : float
        Conformal deviation.
    av_cf : list of float
        List of average conformal degrees for each cluster.
    std_v_cf : list of float
        List of standard deviations of cardinalities for combined spaces per node.
    Not_cf : list of int
        List of nodes in the original graph that are not conformal.
    Gv : networkx.Graph
        The metagraph associated to the transformation.
    """

    rho= scipy.linalg.expm(-t*Lap)
    # Compute metagraph
    Gv = nx.Graph()
    Gv.add_nodes_from(Ag.nodes())
    for i in range(len(Ag.nodes())):
        for j in range(i+1,len(Ag.nodes)):
            if np.abs(rho[i,j]) >= min(np.abs(rho[i,i]),np.abs(rho[j,j]))-tresh:
                Gv.add_edge(list(Ag.nodes())[i],list(Ag.nodes())[j])
    # Compute connected components and store in clusters dictionary
    idx_components = {u: i for i, node_set in enumerate(nx.connected_components(Gv)) for u in node_set}
    clusters = {node: idx_components[node] for node in Gv.nodes()}  # Ensure clusters use Ag node labels
    # Compute harmonicity and conformality measures
    G, deg_h, M_deg_h, std_h, av_h, std_v_h, Not_h, deg_cf, M_deg_cf, std_cf, av_cf, std_v_cf, Not_cf = H_CF_cluster(Ag,clusters)
    return G, deg_h, M_deg_h, std_h, av_h, std_v_h, Not_h, deg_cf, M_deg_cf, std_cf, av_cf, std_v_cf, Not_cf, Gv


# Function to find the smallest t where the renormalized graph has 1 node
def iter_g(Ag,Lap,tresh=0):
    """
    Finds the minimum time t where Laplacian renormalization collapses the graph to a single node.

    Parameters
    ----------
    Ag : networkx.Graph
        The original graph.
    Lap : numpy.ndarray 
        The Laplacian matrix of the graph.
    tresh : float, optional
        Threshold for edge creation in the metagraph (default is 0).
    Returns
    -------
    t : float
        The minimum t value where the renormalized graph has one node.
    """
    t=0.0
    l=0
    while((t<500) and (l!=1)):
        t=t+1.0
        G = simple_renorm(Ag,t,Lap,tresh)
        l=len(G.nodes())
    return t


# Function to find the smallest t where the renormalized graph has 1 node, with 0.1 precision
def iter_narrow_g(Ag,Lap,tresh=0):
    """
    Finds the precise time t where Laplacian renormalization first collapses the graph to a single node.

    Parameters
    ----------
    Ag : networkx.Graph
        The original graph.
    Lap : numpy.ndarray
        The Laplacian matrix of the graph.
    tresh : float, optional
        Threshold for edge creation in the metagraph (default is 0).
    Returns
    -------
    t : float
        The precise t value (rounded to 1 decimal) where the renormalized graph has one node.
    """
    # first find the integer t where the graph collapses
    t_i=iter_g(Ag,Lap,tresh)
    t=t_i-1.0
    l=0
    # then refine the search with 0.1 steps
    while((t<= t_i) and (l!=1)):
        t=t+0.1
        G= simple_renorm(Ag,t,Lap,tresh)
        l=len(G.nodes())
    return round(t,1)


# Function to compute harmonicity and conformality measures over a range of t values
def h_v(Ag,t_span,Lap,tresh=0):
    """
    Computes harmonic and conformal degrees over a range of t values.

    Parameters
    ----------
    Ag : networkx.Graph
        The original graph.
    t_span : array-like
        A sequence of t values to evaluate.
    Lap : numpy.ndarray
        The Laplacian matrix of the graph.
    tresh : float, optional
        Threshold for edge creation in the metagraph (default is 0).
    Returns
    -------
    g : list of networkx.Graph
        List of coarse-grained graphs for each t.
    DEG_H : list of float
        Mean harmonic degrees for each t.
    M_DEG_H : list of float
        Modified harmonic degrees for each t.
    STD_H : list of float
        Harmonic deviations for each t.
    AV_H : list of list of float
        Average harmonic degrees per cluster for each t.
    STD_V_H : list of list of float
        Standard deviations per node for horizontal spaces for each t.
    NOT_H : list of list of int
        Non-harmonic nodes in the original graph for each t.
    DEG_CF : list of float
        Mean conformal degrees for each t.
    M_DEG_CF : list of float
        Modified conformal degrees for each t.
    STD_CF : list of float
        Conformal deviations for each t.
    AV_CF : list of list of float
        Average conformal degrees per cluster for each t.
    STD_V_CF : list of list of float
        Standard deviations per node for combined spaces for each t.
    NOT_CF : list of list of int
        Non-conformal nodes in the original graph for each t.
    gV : list of networkx.Graph
        List of metagraphs for each t.
    """
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
        G, deg_h, M_deg_h, std_h, av_h, std_v_h, Not_h, deg_cf, M_deg_cf, std_cf, av_cf, std_v_cf, Not_cf, Gv = renorm_graph_harmonic(Ag,t,Lap,tresh)
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

    return g, DEG_H, M_DEG_H, STD_H, AV_H, STD_V_H, NOT_H, DEG_CF, M_DEG_CF, STD_CF, AV_CF, STD_V_CF, NOT_CF, gV

# Main function to compute harmonicity and conformality curves, it finds the appropriate t range automatically
# and computes the measures over n points in that range
def H_CF_curves(Ag,Lap,n,tresh=0):
    """
    Computes the curves of harmonic and conformal degrees by first finding the collapse time t_f
    where Laplacian renormalization reduces the graph to a single node, 
    then evaluating over n equally spaced points from 0 to t_f.

    Parameters
    ----------
    Ag : networkx.Graph
        The original graph.
    Lap : numpy.ndarray
        The Laplacian matrix of the graph.
    n : int
        Number of points in the t range.
    tresh : float, optional
        Threshold for edge creation in the metagraph (default is 0).

    Returns
    -------
    g : list of networkx.Graph
        List of coarse-grained graphs for each t.
    DEG_H : list of float
        Mean harmonic degrees for each t.
    M_DEG_H : list of float
        Modified harmonic degrees for each t.
    STD_H : list of float
        Harmonic deviations for each t.
    AV_H : list of list of float
        Average harmonic degrees per cluster for each t.
    STD_V_H : list of list of float
        Standard deviations per node for horizontal spaces for each t.
    NOT_H : list of list of int
        Non-harmonic nodes in the original graph for each t.
    DEG_CF : list of float
        Mean conformal degrees for each t.
    M_DEG_CF : list of float
        Modified conformal degrees for each t.
    STD_CF : list of float
        Conformal deviations for each t.
    AV_CF : list of list of float
        Average conformal degrees per cluster for each t.
    STD_V_CF : list of list of float
        Standard deviations per node for combined spaces for each t.
    NOT_CF : list of list of int
        Non-conformal nodes in the original graph for each t.
    gV : list of networkx.Graph
        List of metagraphs for each t.
    t_span : numpy.ndarray
        The array of t values used.
    """
    # find the final t where the graph collapses to a single node
    t_f=iter_narrow_g(Ag,Lap,tresh)
    t_i=0
    # consider n points in the range [t_i,t_f]
    t_span=np.linspace(t_i,t_f,n)
    # compute harmonicity and conformality degrees over that range
    g, DEG_H, M_DEG_H, STD_H, AV_H, STD_V_H, NOT_H, DEG_CF, M_DEG_CF, STD_CF, AV_CF, STD_V_CF, NOT_CF, gV = h_v(Ag,t_span,Lap, tresh)
    return g, DEG_H, M_DEG_H, STD_H, AV_H, STD_V_H, NOT_H, DEG_CF, M_DEG_CF, STD_CF, AV_CF, STD_V_CF, NOT_CF, gV, t_span


# Calculate lenght of the graph in a list of graphs
def g_len(g):
    """
    Calculates the number of nodes in each graph in a list of graphs.

    Parameters
    ----------
    g : list of networkx.Graph
        A list of graphs.

    Returns
    -------
    lung : list of int
        A list containing the number of nodes for each graph in g.
    """
    lung=[]
    l=len(g)
    for i in range(l):
        el=len(g[i].nodes())
        lung.append(el)
    return lung




