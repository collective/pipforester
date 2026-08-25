from . import deptree

import click
import json


@click.command()
@click.option("--input", "-i", type=click.File("r"))
@click.option("--output", "-o")
@click.option("--cycles", is_flag=True)
@click.option("--check-cycles", is_flag=True)
@click.option(
    "--select",
    "-s",
    multiple=True,
    metavar="DIST",
    help=(
        "Only report cycles the given distribution takes part in. Repeatable. "
        "Cycles between other packages are still printed, but do not fail the run. "
        "Without it every cycle is reported and fatal."
    ),
)
def main(input, output, cycles, check_cycles, select):
    deptreedata = json.load(input)
    graph = deptree.graph_from_json(deptreedata)
    if check_cycles:
        bad_edges = deptree.detect_cyclic_edges(graph, selection=select)
        if bad_edges:
            print("Cyclic dependencies detected")
            exit(1)
    elif cycles:
        graph = deptree.extract_cyclic_graph(graph, selection=select)
    else:
        bad_edges = deptree.detect_cyclic_edges(graph)
        deptree.remove_cyclic_edges(graph, bad_edges)
        graph = deptree.remove_direct_edges(graph)
        deptree.add_cyclic_edges(graph, bad_edges)
    deptree.write_dotfile(graph, output)
