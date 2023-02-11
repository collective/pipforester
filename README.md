# pipforester

Forester tools for [pipdeptree](https://pypi.org/project/pipdeptree/) outputs to analyze the dependency graph of a pip package.

## Features

- clean up a graph to remove direct dependencies if a transitive dependency exists
- detect transitive cyclic dependencies (and color them in output)

## Usage

Important: *pipdeptree* **MUST** be installed in an environment together with the dependencies you want to check.  If you install *pipdeptree* in virtual environment 1 and then call it in the directory of virtual environment 2, it will only report on its own dependencies, which is not very useful.

First, call *pipdeptree* to create a JSON file of the installed dependencies,
and second call *pipforester* to create a cleaned-up dot file.

```shell
pipdeptree -j >forest.json
pipforester -i forest.json -o forest.dot
```

Finally use a Graphviz DOT-file visualizer, i.e. *xdot* on Linux, to view the graph.
Or use the *dot* command line program to generate an svg or png:

```
dot -Tsvg -o forest.svg forest.dot
dot -Tpng -o forest.png forest.dot
```

To generate a graph containing only cyclic transitive dependencies, use the `--cycles` option:

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

