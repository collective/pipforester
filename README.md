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

When checking a single distribution in CI, a cycle between third party packages is accurate
but out of your hands: no change to your own code can break it.
Pass `--select` (`-s`) with the name of the distribution under test to only fail on cycles it
takes part in.
Other cycles are still printed, prefixed with `ignored edge`, but do not change the exit code.

```shell
pipdeptree -j >forest.json
pipforester -i forest.json --check-cycles -s plone.app.testing
```

The option is repeatable, and the name is normalized the way *pipdeptree* keys its nodes, so
`plone.app.testing`, `plone-app-testing` and `Plone.App.Testing` are all the same distribution.
Without `--select` every cycle is fatal, so a central package can keep watching the whole stack.
`--select` applies to `--cycles` as well, which then graphs only the cycles you selected.

See `pipforester --help` for details.

