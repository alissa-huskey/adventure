from adventure.data.player import player

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

def adjust_health(amount):
    player()["health"] += amount
    if player()["health"] < 0:
        player()["health"] = 0

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
