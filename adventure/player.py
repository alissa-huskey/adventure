import shelve
import pickle
from pathlib import Path

from adventure.data.player import player, all_inventory_actions
from adventure.date import now


DATADIR = Path(__file__).parent.parent / "data"


def get_health():
    return player()["health"]

def state(**kwargs):
    """Get or set state details"""
    if kwargs:
        for key in ("args", "command", "action", "item"):
            val = kwargs.pop(key, None)
            if val:
                player()["state"][key] = val
    return player()["state"]

def load_game(datadir=DATADIR):
    path = datadir / "game"

    with shelve.open(str(path), writeback=True) as db:
        db["loaded_at"] = now()
        player(db["player"])
        all_inventory_actions(db["inventory_actions"])
        data = dict(db)

    return data

def save_game(datadir=DATADIR, name=None):
    path = datadir / "game"

    with shelve.open(str(path), writeback=True) as db:
        db["name"] = name
        db["path"] = path.absolute()
        db["saved_at"] = now()
        db["loaded_at"] = None
        db["player"] = player()
        db["inventory_actions"] = all_inventory_actions()

    return path

def adjust_health(amount):
    """Add the following (positive or negative) amount to health, but limit to 0-100"""
    player()["health"] += amount
    if player()["health"] < 0:
        player()["health"] = 0
    if player()["health"] > 100:
        player()["health"] = 100

def is_alive():
    return player()["health"] > 0

def current_place(val=None):
    if val:
        player()["place"] = val
    return player()["place"]

def current_position(val=None):
    if val:
        player()["position"] = val
    return player()["position"]
