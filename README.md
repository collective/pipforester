# pipforester

Forester tools for [pipdeptree](https://pypi.org/project/pipdeptree/) outputs to analyze and cleanup the dependency graph of installed pip packages.

## Features

- clean up a graph to remove direct dependencies if a transitive dependency exists and output it as dot-file.
- detect transitive cyclic dependencies
  - color them in the graph
  - show them as separate graphs in one dot-file
  - exit *pipforester* with exit code 1 if there are cycles detected

### Installation:

- Create an empty virtual environment, separate from the environment to work on.
- `pip install pipdeptree pipforester`

Dependent on your operation system you
- want to install a program to view dot-files, like [xdot](https://pypi.org/project/xdot/) i.e. with `apt install xdot` on Debian/Ubuntu-based systems.
- or use [graphviz](https://www.graphviz.org/) to convert dot-files to PNG/SVG.


## Usage

First, call *pipdeptree* on a virtual environment to create a JSON file of the installed dependencies,
and second call *pipforester* to create a cleaned-up dot file.

```shell
pipdeptree --python  path/to/venv/bin/python -j >forest.json
pipforester -i forest.json -o forest.dot
```

Finally use a Graphviz DOT-file visualizer, i.e. *xdot* on Linux, to view the graph.

```
xdot forest.dot
```

Or use the *dot* command line program to generate an SVG or PNG:

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

# Generate the dependencies graph by one click
Currenly implemented for MacOS and Debian

## Usage
Just run the `make` command in the project folder

## REQUIREMENTS

By default is being used the `Plone -c https://dist.plone.org/release/6.0-dev/constraints.txt` requirements to analyze the dependencies,
but you can change it by passing the `REQUIREMENTS` variable to make es: `make REQUIREMENTS=myrequirements.txt`
