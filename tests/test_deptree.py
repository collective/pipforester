from pipforester import deptree

import pytest


def forest(*packages):
    """Build a `pipdeptree --json` style forest out of (key, [dependency, ...]) pairs."""
    return [
        {
            "package": {
                "key": key,
                "package_name": key,
                "installed_version": "1.0",
            },
            "dependencies": [{"key": dependency} for dependency in dependencies],
        }
        for key, dependencies in packages
    ]


def graph(*packages):
    return deptree.graph_from_json(forest(*packages))


# mine depends on a cycle it is not part of, the way a distribution depends on
# a third party stack with a cycle of its own.
OUTSIDE = (
    ("mine", ["alpha"]),
    ("alpha", ["beta"]),
    ("beta", ["alpha"]),
)

# mine is part of the cycle itself.
INSIDE = (
    ("mine", ["alpha"]),
    ("alpha", ["mine"]),
)


def test_without_a_selection_every_cycle_is_reported():
    assert deptree.detect_cyclic_edges(graph(*OUTSIDE)) == {
        ("alpha", "beta"),
        ("beta", "alpha"),
    }


def test_a_cycle_outside_the_selection_is_not_reported():
    assert deptree.detect_cyclic_edges(graph(*OUTSIDE), selection=["mine"]) == set()


def test_a_cycle_outside_the_selection_is_still_printed(capsys):
    deptree.detect_cyclic_edges(graph(*OUTSIDE), selection=["mine"])
    printed = capsys.readouterr().out
    # the edge closing a cycle is not printed, and which node simple_cycles starts
    # from is arbitrary, so only one of the two edges shows up here
    assert "ignored edge" in printed
    assert "alpha" in printed
    assert "beta" in printed


def test_a_cycle_inside_the_selection_is_reported():
    assert deptree.detect_cyclic_edges(graph(*INSIDE), selection=["mine"]) == {
        ("mine", "alpha"),
        ("alpha", "mine"),
    }


def test_any_of_several_selected_distributions_counts():
    assert deptree.detect_cyclic_edges(graph(*OUTSIDE), selection=["mine", "beta"])


@pytest.mark.parametrize("selected", ["My.Dist", "my-dist", "my_dist", " MY.DIST "])
def test_the_selection_is_normalized_like_a_pipdeptree_key(selected):
    cyclic = (("my-dist", ["alpha"]), ("alpha", ["my-dist"]))
    assert deptree.detect_cyclic_edges(graph(*cyclic), selection=[selected])


def test_extract_cyclic_graph_keeps_only_selected_cycles():
    assert not deptree.extract_cyclic_graph(graph(*OUTSIDE), selection=["mine"]).edges
    assert deptree.extract_cyclic_graph(graph(*OUTSIDE)).edges
