from . import deptree

import click
import json


@click.command()
@click.option("--input", "-i", type=click.File("r"))
@click.option("--output", "-o")
@click.option("--cycles", is_flag=True)
@click.option("--check-cycles", is_flag=True)
def main(input, output, cycles, check_cycles):
    deptreedata = json.load(input)
    graph = deptree.graph_from_json(deptreedata)
    if check_cycles:
        bad_edges = deptree.detect_cyclic_edges(graph)
        if bad_edges:
            print("Cyclic dependencies detected")
            exit(1)
    elif cycles:
        graph = deptree.extract_cyclic_graph(graph)
    else:
        bad_edges = deptree.detect_cyclic_edges(graph)
        deptree.remove_cyclic_edges(graph, bad_edges)
        deptree.remove_direct_edges(graph, ignore=bad_edges)
        deptree.add_cyclic_edges(graph, bad_edges)
    deptree.write_dotfile(graph, output)
