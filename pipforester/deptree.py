import json
import networkx as nx


def read_deptree(filepath):
    with open(filepath) as f:
        data = json.load(f)
    return data


def write_dotfile(G, filepath):
    nx.nx_agraph.write_dot(G, filepath)


def graph_from_json(data):
    G = nx.DiGraph()
    for pkgdef in data:
        pkg = pkgdef["package"]
        G.add_node(
            pkg["key"],
            installed_version=pkg["installed_version"],
            name=pkg["package_name"],
        )
        for dep in pkgdef["dependencies"]:
            G.add_edge(pkg["key"], dep["key"])
    return G


def detect_cyclic_edges(G):
    print("Detecting cyclic edges")
    bad_edges = set()
    cycles = nx.simple_cycles(G)
    for cycle in cycles:
        for idx in range(len(cycle) - 1):
            print(f"found edge {cycle[idx]} -> {cycle[idx + 1]}")
            bad_edges.add((cycle[idx], cycle[idx + 1]))
        bad_edges.add((cycle[-1], cycle[0]))
    return bad_edges


def extract_cyclic_graph(G):
    print("Extracting cyclic edges")
    CG = nx.DiGraph()
    bad_edges = set()
    for num, cycle in enumerate(nx.simple_cycles(G)):
        if (cycle[-1], cycle[0]) in bad_edges:
            continue
        for idx in range(len(cycle) - 1):
            CG.add_edge(f"{cycle[idx]} ({num})", f"{cycle[idx + 1]} ({num})")
        CG.add_edge(f"{cycle[-1]} ({num})", f"{cycle[0]} ({num})")
        bad_edges.add((cycle[-1], cycle[0]))
    return CG


def remove_cyclic_edges(G, bad_edges):
    print("Removing cyclic edges")
    for edge in bad_edges:
        G.remove_edge(edge[0], edge[1])


def add_cyclic_edges(G, bad_edges):
    print("Adding cyclic edges")
    for edge in bad_edges:
        G.add_edge(edge[0], edge[1])
        G.edges[edge[0], edge[1]]["color"] = "darkviolet"


def remove_direct_edges(G):
    return nx.transitive_reduction(G)
