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
        deps = pkgdef["dependencies"]
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
    for cycle in nx.simple_cycles(G):
        bad_edges.add((cycle[-1], cycle[0]))
    return bad_edges


def remove_cyclic_edges(G, bad_edges):
    print("Removing cyclic edges")
    for edge in bad_edges:
        G.remove_edge(edge[0], edge[1])


def add_cyclic_edges(G, bad_edges):
    print("Adding cyclic edges")
    for edge in bad_edges:
        G.add_edge(edge[0], edge[1], color="red")


def remove_direct_edges(G):
    print("Removing direct edges")
    to_remove = []
    for node in G.nodes():
        # get all edges origin in node
        print(f"  Node: {node}")
        out_edges = list(G.out_edges(node))
        for out_edge in out_edges:
            print(f"    Out edge to {out_edge[1]}")
            for path in nx.all_simple_paths(G, node, out_edge[1]):
                # if there is a path from node to out_edge[1] that is longer than 1, then
                # remove the edge
                if len(path) > 2:
                    print(f"    -> remove")
                    G.remove_edge(out_edge[0], out_edge[1])
                    break
