from . import deptree

import click
import json


@click.command()
@click.option("--input", "-i", type=click.File("r"))
@click.option("--output", "-o")
def main(input, output):
    deptreedata = json.load(input)
    G = deptree.graph_from_json(deptreedata)
    bad_edges = deptree.detect_cyclic_edges(G)
    deptree.remove_cyclic_edges(G, bad_edges)
    deptree.remove_direct_edges(G)
    deptree.add_cyclic_edges(G, bad_edges)
    deptree.write_dotfile(G, output)
