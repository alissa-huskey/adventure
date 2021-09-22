from .data.player import PLAYER, INVENTORY_ACTIONS

def get_health():
    return PLAYER["health"]

def state(**kwargs):
    """Get or set state details"""
    if kwargs:
        for key in ("args", "command", "action", "item"):
            val = kwargs.pop(key, None)
            if val:
                PLAYER["state"][key] = val
    return PLAYER["state"]

def adjust_health(amount):
    PLAYER["health"] += amount
    if PLAYER["health"] < 0:
        PLAYER["health"] = 0

def is_alive():
    return PLAYER["health"] > 0

def current_place(val=None):
    if val:
        PLAYER["place"] = val
    return PLAYER["place"]

def current_position(val=None):
    if val:
        PLAYER["position"] = val
    return PLAYER["position"]
