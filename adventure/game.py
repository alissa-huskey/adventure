"""Text based adventure game"""

import shlex
import re
from pprint import pprint

from console import fx, fg

from .items import get_item
from .args import require, validate, extra_args
from .actions import local_action, inventory_action
from .help import get_help, COMMANDS
from .places import (
    COMPASS,
    COMPASS_OPTIONS,
    MOVEMENTS,
    PLACES,
    get_place,
    get_direction,
)
from .formatting import (
    info,
    error,
    debug,
    print_error,
    hr,
    mergelines,
    bar,
    Grid,
    Table,
)
from .player import (
    is_alive,
    current_location,
    current_position,
    get_all_inventory,
    get_inventory,
    get_health,
    state,
)
from . import (
    Error,
    NotFound,
    UserError,
    SilentError,
    themes,
)

def show(location, long=False):
    """."""
    print()
    info(themes.title(location.get("name", "Unnamed location").title()))
    print()

    items = location.get("items", [])
    if long or not location.get("visited"):
        desc = location.get("description")
    else:
        desc = location.get("short") or location.get("description")

    if desc:
        if items:
            desc = re.sub(
                rf'\b({"|".join(items)})\b',
                rf'{themes.items}\1{fg.default}',
                desc,
                flags=re.IGNORECASE,
            )
        info(mergelines(desc))
        print()

    for letter, desc in location["look"].items():
        if not desc: continue
        direction = get_direction(letter)
        info(f"To the {themes.compass(direction)} is {desc}.")
    print()
    location["visited"] = True

def parse(response):
    """Return a tuple containing the (command, args) parsed from response"""
    words = shlex.split(response.strip())
    if not words:
        error(silent=True)

    state(command=words[0], args=words[1:])

    command = words.pop(0).lower()
    func = None

    if command in ["self", "me", "stats"]:
        func = do_stats

    elif command in ["m", "map"]:
        func = do_map

    elif command in ["i", "inventory"]:
        func = do_inventory

    elif command in ["l", "look"]:
        func = do_look

    elif command in ["x", "ex", "exam", "examine"]:
        func = do_examine

    elif command in ["g", "go"]:
        func = do_go

    elif command in COMPASS_OPTIONS:
        func = do_go
        words.insert(0, command)

    elif command in ["j", "jump"]:
        func = do_jump

    elif command in ["?", "help"]:
        func = do_help

    elif command in ["q", "quit", "exit"]:
        func = do_quit

    else:
        try:
            func, words = inventory_action(command, words)
        except NotFound:
            try:
                func, words = local_action(command, words)
            except NotFound:
                ...

        if not func:
            error(f"No such command: {command!r}")

    state(args=words)
    return (func, words)

def goto(pos):
    """Update the players pos(ition) and location, or return False if no such
    position exists."""
    location = get_place(pos)
    if not location:
        return False

    current_position(pos)
    current_location(location)
    return location

def step(pos, direction, times=1):
    """Return a positon modified after going in direction a number of times.
    >>> step((0, 0), "N")
    (0, 1)

    >>> step((0, 0), "E")
    (0, 1)

    """
    assert pos and isinstance(pos, tuple), \
        f"Non-empty tuple pos expected but got: ({type(pos)}) '{pos}'"

    assert direction and isinstance(direction, str), \
        f"Non-empty direction (str) expected but got: ({type(direction)}) '{direction}'"

    mod = MOVEMENTS[direction[0].upper()]
    return tuple([pos[i] + mod[i]*times for i in range(2)])

def do_map(*args):
    grid = Grid()
    for place in PLACES:
        x, y = place.get("position")
        try:
            debug(f"location: {place['name']!r}, ({x=}, {y=})")
            grid.set(y, x, place.get("name", ""))
        except IndexError:
            error(f"Couldn't map location: {place['name']!r}, ({x=}, {y=})")

    print("\n")
    info(fx.bold("Map"))
    print()
    print(grid.render())
    print()

def do_quit(*args):
    quit()

def do_help(command=None, *args):
    # help for a specific command
    if not command:
        width = max(map(len, [x["name"] for x in COMMANDS])) + 2
        for cmd in COMMANDS:
            info(themes.cmd(cmd["name"].ljust(width)), cmd["description"])
        return

    cmd = get_help(command)
    if not cmd:
        error(f"No such command: {command!r}")

    titles = ["arguments", "examples", "titles", "usage", "aliases"]
    options = dict(
        align={0: "rjust"},
        sizes={0: (max(map(len, titles)) + 1)},
        padding=2,
    )

    tables = [Table(**options)]
    usage = [themes.cmd(cmd["name"])] + \
            [themes.usage_arg(arg) for arg in cmd["arguments"]["required"]] + \
            [f"[{themes.usage_arg(arg)}]" for arg in cmd["arguments"]["optional"]]

    tables[-1].append([themes.help_title("Usage:"), " ".join(usage)])
    tables[-1].append(["", cmd["description"]])
    tables[-1].append()

    if cmd["aliases"]:
        tables[-1].append([themes.help_title("Aliases:"), ", ".join(cmd["aliases"])])
        tables[-1].append()

    args = cmd["arguments"]["required"].copy()
    args.update(cmd["arguments"]["optional"])
    if args:
        tables.append(Table(**options))
        for i, (name, arg) in enumerate(args.items()):
            title = (themes.help_title("Arguments:"), "")[bool(i)]
            desc = arg["desc"]
            if arg.get("default"): desc += f" (default={themes.arg_default(str(arg['default']))})"

            tables[-1].append([title, themes.arg(name), desc])

            if arg.get("notes"): tables[-1].append(["", "", f'({arg["notes"]})'])
            if arg.get("options"): tables[-1].append(["", "", "options: " + ", ".join(arg["options"])])
        tables[-1].append()

    if cmd["examples"]:
        tables.append(Table(**options))
        examples = [f"> {e}" for e in cmd["examples"]]
        tables[-1].append([themes.help_title("Examples:"), examples.pop(0)])
        for e in examples:
            tables[-1].append(["", e])

    print()
    for t in tables:
        print(t.text)

def do_look(direction=None, *args):
    """Describe the scenery in the direction the player looks."""
    validate("look", direction, "direction", choices=["around"]+list(COMPASS.values()),
            options=["a"]+COMPASS_OPTIONS)
    extra_args("look", args)

    location = current_location()

    if not direction:
        show(location, long=True)
        return

    if direction.strip().lower() == "around":
        items = location["items"] or None
        if items:
            info("You see " + ", ".join([str(fx.bold(o)) for o in items]) + ".")
        return

    lookto = direction[0].upper()

    desc = location["look"][lookto] or "empty space"
    print()
    info(f"To the {get_direction(direction)} you see {desc}.")

def do_examine(name=None, *args):
    """."""
    require("examine", name, "item")
    extra_args("look", args)

    if name in ["self", "me"]:
        do_stats()
        return

    item = get_item(name)
    if not name in current_location()["items"]:
        error(f"There is no {name} in {current_location()['name']}.")
    if not item:
        error(f"Can't find details about: {name!r}")

    print()
    info(fx.bold(item.get("name", "Unnamed location").title()))
    print()
    info(mergelines(item["desc"]))

def do_jump(place=None, *args):
    """Jump straight to a place"""
    require("jump", place, "place")
    extra_args("jump", args)

    location = get_place(place)

    if goto(location["position"]):
        show(current_location())

def do_go(direction=None, steps=1, *args):
    """Move the player to a new position based on the direction they wish to
    travel."""
    direction = require("go", direction, "direction", choices=COMPASS.values(),
                        options=COMPASS_OPTIONS)
    steps = require("go", steps, "steps", klass=int)
    extra_args("go", args)

    pos = step(current_position(), direction, steps)
    if goto(pos):
        show(current_location())
    else:
        error("You can't go that way.")

def do_inventory(*args):
    """Show inventory"""
    print()
    for item, amount in get_all_inventory().items():
        info(f"({amount: >3}) {item}")

def do_stats(*args):
    """Show player stats"""
    print()
    bar("health", get_health())

def main():
    hr()
    print("Welcome to the adventure!\n")
    do_jump("home")
    print()
    hr(char="~")
    print()

    while True:
        debug(position=current_position(), location=current_location()["name"])

        try:
            cmd, args = parse(input("> "))
            cmd(*args)
        except SilentError:
            continue
        except Error as err:
            msg = err.args[0]
            print_error(f"Something went wrong: {msg}")
        except UserError as err:
            print_error(err.args[0])
        finally:
            print()
            hr(char="~")
            print()

        if not is_alive():
            info("Oh no, you're dead!")
            do_mirror()
            print()
            quit()


if __name__ == "__main__":
    main()
