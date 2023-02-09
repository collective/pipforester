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

See `pipforester --help` for details.

