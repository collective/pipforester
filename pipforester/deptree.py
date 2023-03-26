import json
import networkx as nx
import pygraphviz


def read_deptree(filepath):
    with open(filepath) as f:
        data = json.load(f)
    return data


_SUBGRAPHS = {
    "plone": "Plone",
    "zope": "Zope",
}


def find_subgraph(node) -> str | None:
    for subgraph in _SUBGRAPHS:
        if node.startswith(subgraph):
            return subgraph
    return None


def grouped_agraph(nxgraph):
    """Returns a pygraphviz graph."""
    agraph = nx.nx_agraph.to_agraph(nxgraph)
    agraph.subgraph(["plone", "plone.volto", "plone.app.upgrade"], name="plonetop", color="blue")

    # group nodes
    # nodes = {}
    # for subgraphname in _SUBGRAPHS:
    #     nodes[subgraphname] = []

    # for nodename, nodedata in nxgraph.nodes(data=True):
    #     subgraph_name = find_subgraph(nodename)
    #     if subgraph_name is not None:
    #         nodes[subgraph_name].append((nodename, nodedata))
    # for subgraphname in nodes:
    #     nodenames = [t[0] for t in nodes[subgraphname]]
    #     agraph.subgraph(
    #         nodenames,
    #         name=subgraphname,
    #         label=_SUBGRAPHS[subgraphname],
    #         color="blue",
    #         style="filled",
    #         fillcolor="lightblue",
    #     )
    agraph.layout(prog="dot")
    # agraph.draw('testree.png')
    return agraph


def write_dotfile(nxgraph, filepath):
    agraph = grouped_agraph(nxgraph)
    agraph.write(filepath)
    agraph.clear()


def graph_from_json(data):
    G = nx.DiGraph()
    for pkgdef in data:
        pkg = pkgdef["package"]
        deps = pkgdef["dependencies"]
        G.add_node(
            pkg["key"],
            installed_version=pkg["installed_version"],
            name=pkg["package_name"],
        )
        for dep in pkgdef["dependencies"]:
            G.add_edge(pkg["key"], dep["key"])
    return G


def detect_cyclic_edges(G, mark=False):
    bad_edges = set()
    for cycle in nx.simple_cycles(G):
        if mark:
            for idx in range(len(cycle) - 1):
                G.edges[cycle[idx], cycle[idx + 1]]["color"] = "darkviolet"
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
            CG.add_edge(cycle[idx], cycle[idx + 1])
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
        G.add_edge(edge[0], edge[1], color="darkviolet")


def remove_direct_edges(G, ignore=None):
    print("Removing direct edges")
    to_remove = []
    if ignore is None:
        ignore = []
    for node in G.nodes():
        # get all edges origin in node
        print(f"  Node: {node}")
        out_edges = list(G.out_edges(node))
        for out_edge in out_edges:
            if tuple(out_edge) in ignore:
                print(f"  Ignore cyclic: {node}")
                continue
            print(f"    Out edge to {out_edge[1]}")
            # speedup: remove edge, then check if there is a path, if not add edge
            G.remove_edge(out_edge[0], out_edge[1])
            if not nx.has_path(G, node, out_edge[1]):
                G.add_edge(out_edge[0], out_edge[1])
