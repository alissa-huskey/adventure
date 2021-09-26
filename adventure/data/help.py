from adventure.places import COMPASS


COMMANDS = [
    {
        "name": "help",
        "description": "get information about actions",
        "examples": ["help", "help go"],
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
        "aliases": ["q", "exit"],
    },
    {
        "name": "stats",
        "description": "show your health and gems",
        "aliases": ["me", "self"],
    },
    {
        "name": "save",
        "description": "save your game",
    },
    {
        "name": "load",
        "description": "load a saved game",
    },
    {
        "name": "inventory",
        "description": "show your inventory",
        "aliases": ["i"],
    },
    {
        "name": "look",
        "description": "describe your location",
        "examples": ["look"],
        "aliases": ["l"],
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
        "description": "move in a direction",
        "examples": ["go east", "g w", "south", "go north 3"],
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
        "aliases": ["m"],
    },
    {
        "name": "jump",
        "listed": False,
        "description": "jump straight to a particular place",
        "examples": ["jump home", "j home"],
        "aliases": ["j"],
        "arguments": {
            "required": {
                "place": { "desc": "where to jump to", },
            },
        },
    },
    {
        "name": "intro",
        "description": "show the introduction",
        "examples": ["intro"],
    },
]

# name/alias -> command dict
TOPICS = {}
for cmd in COMMANDS:
    TOPICS[cmd["name"]] = cmd
    for alias in cmd.get("aliases", []):
        TOPICS[alias] = cmd
