from collections import defaultdict

from .objects import get_object

PLAYER = {
    "pos": None,
    "location": None,
    "health": 100,
    "inventory": defaultdict(int,
        gems=0,
    ),
    "state": {
        "command": None,
        "args": None,
        "action": None,
        "thing": None,
    }
}

INVENTORY_ACTIONS = defaultdict(set)

def get_health():
    return PLAYER["health"]

def get_all_inventory():
    return PLAYER["inventory"]

def get_inventory(name):
    return PLAYER["inventory"][name]

def add_inventory_action(name):
    thing = get_object(name)
    if not thing:
        return
    for action in thing.get("actions", []):
        INVENTORY_ACTIONS[action].add(name)

def remove_inventory_action(name):
    thing = get_object(name)
    if not thing:
        return
    for action in thing.get("actions", []):
        INVENTORY_ACTIONS[action].remove(name)

def adjust_inventory(name, amount):
    if amount > 0 and not PLAYER["inventory"][name]:
        add_inventory_action(name)

    PLAYER["inventory"][name] += amount

    if not PLAYER["inventory"]:
        remove_inventory_actions(name)

def state(**kwargs):
    if kwargs:
        for key in ("args", "command", "action", "thing"):
            val = kwargs.pop(key, None)
            if val:
                PLAYER["state"][key] = val
    return PLAYER["state"]

def adjust_health(amount):
    PLAYER["health"] += amount
    if PLAYER["health"] < 0:
        PLAYER["health"] = 0

def inventory_for_action(name):
    return INVENTORY_ACTIONS[name]

def is_alive():
    return PLAYER["health"] > 0

def can_afford(price):
    return get_inventory("gems") >= abs(price)

def current_location(val=None):
    if val:
        PLAYER["location"] = val
    return PLAYER["location"]

def current_position(val=None):
    if val:
        PLAYER["position"] = val
    return PLAYER["position"]
