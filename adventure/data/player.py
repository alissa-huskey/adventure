from copy import deepcopy
from collections import defaultdict

def init():
    global PLAYER, INVENTORY_ACTIONS
    PLAYER = deepcopy(DEFAULTS)
    INVENTORY_ACTIONS = {}

    return PLAYER, INVENTORY_ACTIONS

def player(data=None):
    global PLAYER
    if data: PLAYER = data
    return PLAYER

def all_inventory_actions(data=None):
    global INVENTORY_ACTIONS
    if data: INVENTORY_ACTIONS = data
    return INVENTORY_ACTIONS

HINTS = [
    "You could always take another look around.",
    "Is there something you could examine more closely?",
    "Maybe it's time to go.",
    "Try taking a look at the help.",
]

DEFAULTS = {
    "pos": None,
    "place": None,
    "health": 100,
    "inventory": dict(
        gems=0,
    ),
    "state": {
        "command": None,
        "args": None,
        "action": None,
        "item": None,
    },
    "items": {},
    "places": {},
    "hints": HINTS[:],
}

PLAYER, INVENTORY_ACTIONS = deepcopy(DEFAULTS), {}
