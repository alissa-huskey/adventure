from collections import defaultdict

PLAYER = {
    "pos": None,
    "place": None,
    "health": 100,
    "inventory": defaultdict(int,
        gems=10,
    ),
    "state": {
        "command": None,
        "args": None,
        "action": None,
        "item": None,
    },
}

INVENTORY_ACTIONS = defaultdict(set)

