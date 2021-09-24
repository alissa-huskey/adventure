import pickle
from collections import defaultdict
import shelve

import pytest

from adventure.places import get_place
from adventure.player import (
    load_game,
    save_game,
    player,
    adjust_health,
)

@pytest.fixture
def game():
    """Fixture for a saved game"""
    return {
        "name": "test-save",
        "pos": (-1, 3),
        "place": get_place("cave"),
        "health": 80,
        "inventory": defaultdict(
            int,
            gems=12,
            dagger=1,
        ),
        "state": {
            "command": None,
            "args": None,
            "action": None,
            "item": None,
        },
    }

@pytest.fixture
def saved_game(tmp_path, game):
    """Save fixture file"""
    player(game)
    save_game(tmp_path)

def test_save_game(game, tmp_path):
    # set PLAYER
    player(game)

    path = save_game(tmp_path, name="test-save")
    data = shelve.open(str(path))

    assert data.get("name") == "test-save"
    assert not data.get("loaded_at")

def test_load_game(saved_game, tmp_path):
    data = load_game(tmp_path)

    assert data.get("player", {}).get("name") == "test-save"
    assert data.get("path")

    with shelve.open(str(data["path"])) as data:
        assert player().get("name") == "test-save"

@pytest.mark.parametrize("start, amount, result", [
    (90, 22, 100),
    (10, -12, 0),
    (50, 10, 60),
    (50, -10, 40),
])
def test_adjust_health(start, amount, result):
    player()["health"] = start
    adjust_health(amount)
    assert player()["health"] == result
