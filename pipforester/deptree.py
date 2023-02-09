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
    bad_edges = set()
    for cycle in nx.simple_cycles(G):
        bad_edges.add((cycle[-1], cycle[0]))
    return bad_edges


def remove_cyclic_edges(G, bad_edges):
    for edge in bad_edges:
        G.remove_edge(edge[0], edge[1])


def add_cyclic_edges(G, bad_edges):
    for edge in bad_edges:
        G.add_edge(edge[0], edge[1], color="red")


def remove_direct_edges(G):
    to_remove = []
    for node in G.nodes():
        # get all edges origin in node
        print(f"Node: {node}")
        for out_edge in G.out_edges(node):
            print(f"Out edge: {out_edge}")
            for path in nx.all_simple_paths(G, node, out_edge[1]):
                # if there is a path from node to out_edge[1] that is longer than 1, then
                # remove the edge
                if len(path) > 1:
                    to_remove.append(out_edge)
                    break

    for edge in to_remove:
        G.remove_edge(edge[0], edge[1])
