from click.testing import CliRunner
from pipforester import main

import json
import pytest


# mine depends on a cycle it is not part of.
OUTSIDE = [
    {
        "package": {"key": key, "package_name": key, "installed_version": "1.0"},
        "dependencies": [{"key": dependency} for dependency in dependencies],
    }
    for key, dependencies in (
        ("mine", ["alpha"]),
        ("alpha", ["beta"]),
        ("beta", ["alpha"]),
    )
]


@pytest.fixture
def check_cycles(tmp_path):
    forest = tmp_path / "forest.json"
    forest.write_text(json.dumps(OUTSIDE))

    def run(*args, env=None):
        command = [
            "-i",
            str(forest),
            "-o",
            str(tmp_path / "out.dot"),
            "--check-cycles",
            *args,
        ]
        return CliRunner().invoke(main, command, env=env)

    return run


def test_every_cycle_fails_without_a_selection(check_cycles):
    assert check_cycles().exit_code == 1


def test_select_option_ignores_cycles_outside_the_selection(check_cycles):
    assert check_cycles("-s", "mine").exit_code == 0


def test_select_is_read_from_the_environment(check_cycles):
    assert check_cycles(env={"PIPFORESTER_SELECT": "mine"}).exit_code == 0


def test_the_environment_takes_several_whitespace_separated_names(check_cycles):
    assert check_cycles(env={"PIPFORESTER_SELECT": "other  mine"}).exit_code == 0
    assert check_cycles(env={"PIPFORESTER_SELECT": "other beta"}).exit_code == 1


def test_an_empty_environment_variable_selects_nothing(check_cycles):
    assert check_cycles(env={"PIPFORESTER_SELECT": ""}).exit_code == 1


def test_the_option_wins_over_the_environment(check_cycles):
    assert check_cycles("-s", "beta", env={"PIPFORESTER_SELECT": "mine"}).exit_code == 1
