from adventure.places import COMPASS


COMMANDS = [
    {
        "name": "help",
        "description": "get help on available commands",
        "examples": [],
        "aliases": ["?"],
        "arguments": {
            "required": {},
            "optional": {
                "command": {
                    "desc": "command to get help for",
                    "default": "None",
                },
            },
        },
    },
    {
        "name": "quit",
        "description": "leave the game",
        "examples": [],
        "aliases": ["q", "exit"],
        "arguments": {
            "required": {},
            "optional": {},
        },
    },
    {
        "name": "stats",
        "description": "show your health",
        "examples": [],
        "aliases": ["self", "me"],
        "arguments": {
            "required": {},
            "optional": {},
        },
    },
    {
        "name": "inventory",
        "description": "show your inventory",
        "examples": [],
        "aliases": ["i"],
        "arguments": {
            "required": {},
            "optional": {},
        }
    },
    {
        "name": "look",
        "description": "describe your location",
        "examples": [ "look", "look west", "look around" ],
        "aliases": ["l"],
        "arguments": {
            "required": {},
            "optional": {
                "direction": {
                    "desc": "which direction to look",
                    "options": ["around"]+list(COMPASS.values()),
                    "default": "None",
                }
            },
        }
    },
    {
        "name": "examine",
        "description": "take a closer look at something",
        "examples": ["examine bed", "x me"],
        "aliases": ["x", "ex", "exam", "examine"],
        "arguments": {
            "required": {
                "item": {
                    "desc": "what you want to examine",
                    "notes": "self or me redirects to stats command",
                }
            },
            "optional": {},
        }
    },
    {
        "name": "go",
        "description": "go somewhere",
        "examples": ["go east", "g e", "east"],
        "aliases": ["g"],
        "arguments": {
            "required": {
                "direction": {
                    "desc": "which way to go",
                    "options": COMPASS.values(),
                    "notes": "can be shortened to first letter",
                },
            },
            "optional": {
                "steps": {
                    "desc": "number of steps to take",
                    "default": 1,
                },
            },
        },
    },
    {
        "name": "map",
        "listed": False,
        "description": "show the map",
        "examples": [],
        "aliases": ["m"],
        "arguments": {
            "required": {},
            "optional": {},
        },
    },
    {
        "name": "jump",
        "listed": False,
        "description": "jump to a particular place",
        "examples": ["jump home", "j home"],
        "aliases": ["j"],
        "arguments": {
            "required": {
                "place": { "desc": "where to jump to", },
            },
            "optional": {},
        },
    },
]

# name/alias -> command dict
TOPICS = {}
for cmd in COMMANDS:
    TOPICS[cmd["name"]] = cmd
    for alias in cmd["aliases"]:
        TOPICS[alias] = cmd
