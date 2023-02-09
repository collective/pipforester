# pipforester

Forester tools for [pipdeptree](https://pypi.org/project/pipdeptree/) outputs to analyze the dependency graph of a pip package.

## Features

- clean up a graph to remove direct dependencies if a transitive dependency exists
- detect transitive cyclic dependencies (and color them in output)

## Usage

First call *pipdeptree* to create a JSON file of the installed dependecies,
second call pipforester to create cleaned up dot file.
Finally use a Graphviz DOT-file visualizer, i.e. *xdot* on Linux, to view the graph.

```shell
pipdeptree -j >forest.json
pipforester -i forest.json -o forest.dot
```

To only generate a graph containing only cyclic transitive dependencies, use the `--cycles` option:

```shell
pipdeptree -j >forest.json
pipforester -i forest.json -o forest.dot --cycles
```

To detect cyclic transitive dependencies and exit with `1` if there is at least one, use the `--check-cycles` option.
It does not generate an output graph and is meant for usage in CI.

```shell
pipdeptree -j >forest.json
pipforester -i forest.json --check-cycles
```

See `pipforester --help` for details.

