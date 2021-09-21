COMPASS = {
    "n": "north",
    "e": "east",
    "s": "south",
    "w": "west"
}

MOVEMENTS = {
    "N": (0, 1),
    "E": (1, 0),
    "S": (0, -1),
    "W": (-1, 0),
}

COMPASS_OPTIONS = list(COMPASS)  + list(COMPASS.values())

PLACES = [
    {
        "name": "home",
        "position": (0, 0),
        "visited": False,
        "short": "Your house.",
        "description": """
            The furniture in your one room stone cottage is made up of dark wood. A
            circular rug covers much of the cold stone floor and heat from a cast
            iron stove in the corner drives away the chill.

            Light streams in through the window against the north wall, around
            which a counter and shelves hold kitchen supplies. Against the opposite
            wall is a desk with a high backed chair. Built into a nook behind you
            is your bed, the bedding is slightly rumpled.

            Before you is the arched wooden front door, facing east.
        """,
        "look": {
            "N": None,
            "S": None,
            "E": "the front door",
            "W": None,
        },
        "enter": (
            "You find yourself in your simple one-room house."
        ),
        "items": ["bed", "desk", "chair", "counter", "stove", "door", "book"],
        "actions": {},
    },
    {
        "name": "courtyard",
        "position": (1, 0),
        "short": "The front courtyard of your cottage.",
        "description": """
            You are standing in in the front courtyard of your cottage. A stepping
            stone path leads through the small garden and past the open fence gate.

            A wooden bench sits under in the shade of the portico. Next to the
            front door a gnarled walking stick leans against the wall.
        """,
        "look": {
            "N": "",
            "E": "cobblestone path into town",
            "S": "",
            "W": "your house",
        },
        "items": ["bench", "stick", "walking stick", "gate"],
        "actions": {},
    },
    {
        "name": "path",
        "position": (2, 0),
        "short": "A cobblestone path into town.",
        "description": """
            A narrow cobblestone lane that winds through the village and under
            stone archways.

            Flower pots dot the steps leading to front doors and spots of color
            spill out of window planters. Above the steet laundry hangs from
            lines strung across high windows.

            A hand carved sign hangs over a door on the north side of the street
            that reads "Market".
        """,
        "look": {
            "N": "the door to the market",
            "E": "a road",
            "S": "",
            "W": "a courtyard",
        },
        "items": ["flower pots", "planters"],
        "actions": {},
    },
    {
        "name": "market",
        "position": (2, 1),
        "description": "",
        "look": {
            "N": None,
            "E": None,
            "S": "cobblestone path into town",
            "W": None,
        },
        "items": ["elixr", "cloak"],
        "actions": {
            "buy": {"elixr", "cloak"},
        },
    },
    {
        "name": "road",
        "position": (3, 0),
        "description": "",
        "look": {
            "N": "an impenetrable forest",
            "E": "",
            "S": "a cave",
            "W": "path",
        },
        "items": [],
        "actions": {},
    },
    {
        "name": "cave",
        "position": (3, -1),
        "description": "",
        "look": {
            "N": "the road",
            "S": "",
            "E": "",
            "W": "",
        },
        "items": ["dragon"],
        "actions": {
            "pet": {"dragon"},
        },
    },
]

BY_POS = {p["position"]: p for p in PLACES}
BY_NAME = {p["name"]: p for p in PLACES}

