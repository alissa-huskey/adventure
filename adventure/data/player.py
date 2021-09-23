from copy import deepcopy
from collections import defaultdict

def init():
    global PLAYER, INVENTORY_ACTIONS
    PLAYER = deepcopy(DEFAULTS)
    INVENTORY_ACTIONS = defaultdict(set)

    return PLAYER, INVENTORY_ACTIONS

def player():
    return PLAYER

def all_inventory_actions():
    return INVENTORY_ACTIONS

DEFAULTS = {
    "pos": None,
    "place": None,
    "health": 100,
    "inventory": defaultdict(int,
        gems=0,
    ),
    "state": {
        "command": None,
        "args": None,
        "action": None,
        "item": None,
    },
}

PLAYER, INVENTORY_ACTIONS = deepcopy(DEFAULTS), defaultdict(set)
