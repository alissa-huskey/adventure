import random
import time

from more_itertools import first
from console import fg, fx

from adventure.args import require, validate, extra_args
from adventure.items import COLORS, MOODS, get_item
from adventure.help import get_help
from adventure.player import adjust_health, current_place, state, get_health
from adventure.data.help import COMMANDS
from adventure.formatting import (
    info,
    error,
    NotFound,
    bar,
    mergelines,
    Grid,
    Table,
)
from adventure.inventory import (
    get_inventory,
    adjust_inventory,
    inventory_for_action,
    can_afford,
    get_all_inventory,
)
from adventure.places import (
    COMPASS,
    COMPASS_OPTIONS,
    PLACES,
    get_place,
    get_direction,
    current_position,
    current_place,
    goto,
    step,
    show,
)
from adventure import themes

ACTIONS = {}

def do_map(*args):
    grid = Grid()
    for place in PLACES:
        x, y = place.get("position")
        try:
            debug(f"place: {place['name']!r}, ({x=}, {y=})")
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
    # list help topics
    if not command:
        width = max(map(len, [x["name"] for x in COMMANDS])) + 2
        for cmd in COMMANDS:
            if cmd.get("listed", True):
                info(themes.cmd(cmd["name"].ljust(width)), cmd["description"])
        return

    # help for a specific command
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

    place = current_place()

    if not direction:
        show(place, long=True)
        return

    if direction.strip().lower() == "around":
        items = place["items"] or None
        if items:
            info("You see " + ", ".join([str(fx.bold(o)) for o in items]) + ".")
        return

    lookto = direction[0].upper()

    desc = place["look"][lookto] or "empty space"
    print()
    info(f"To the {get_direction(direction)} you see {desc}.")

def do_examine(name=None, *args):
    """Look at an item in the current place or in inventory."""

    require("examine", name, "item")
    extra_args("look", args)

    if name in ["self", "me"]:
        do_stats()
        return

    item = get_item(name)
    if not (name in current_place()["items"] or get_inventory(name)):
        error(f"There is no {name} in {current_place()['name']}.")

    if not item:
        error(f"Can't find details about: {name!r}")

    print()
    info(fx.bold(item.get("name", "Unnamed place").title()))
    print()
    info(mergelines(item["desc"]))

def do_jump(place=None, *args):
    """Jump straight to a place"""
    require("jump", place, "place")
    extra_args("jump", args)

    place = get_place(place)

    if goto(place["position"]):
        show(current_place())

def do_go(direction=None, steps=1, *args):
    """Move the player to a new position based on the direction they wish to
    travel."""
    direction = require("go", direction, "direction", choices=COMPASS.values(),
                        options=COMPASS_OPTIONS)
    steps = require("go", steps, "steps", klass=int)
    extra_args("go", args)

    pos = step(current_position(), direction, steps)
    if goto(pos):
        show(current_place())
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

def get_action(name):
    return ACTIONS.get(name)

def contextual_action(command, words, local=False):
    """Return command function, and args from actions available based on context or
       raise NotFound error. Either actions for a specific place if local, or actions for
       an item in inventory.
    """
    args = words[:]

    if local:
        place = current_place()
        items = place["actions"].get(command, set())

        # no such action at this place
        if command not in place["actions"]:
            raise NotFound()
    else:
        items = inventory_for_action(command)

        # no such inventory action
        if not items:
            raise NotFound()

    # item is required
    if items:

        item = first(items.intersection(args), None)
        state(item=item)

        # missing required item for action
        if not args:
            error(f'You need to say what you want to {command}.')

        # item not in inventory
        if not item:
            if local:
                error(f"({command}) There's no {args[0]} nearby.")
            else:
                error(f"({command}) You have no {args[0]} in your inventory.")

        # make sure item is the first arg
        if item != args[0]:
            args.remove(item)
            args.insert(0, item)

    return (get_action(command), args)

def do_pet(item=None, color=None, *args):
    """Pet one of the dragon heads."""
    color = require("pet", color, "color", choices=COLORS)

    random.shuffle(COLORS)
    dragons = dict(zip(COLORS, MOODS))
    mood = dragons[color]
    damage, amount = 0, 0

    if mood == "cheerful":
        amount = random.randint(3, 15)
        message = f"thinks you're adorable! He gives you {amount} gems!"

    elif mood == "cranky":
        damage = random.randint(-15, -3)
        message = ("wants to be left alone. The heat from his mighty sigh "
                   f"singes your hair, costing you {damage} in health.")

    elif mood == "lonely":
        amount = random.randint(8, 25)
        damage = random.randint(-25, -8)
        message = ("is just SO happy to see you! He gives you a whopping "
                   f"{amount} gems! Then he hugs you, squeezes you, and calls "
                   f"you George... costing you {damage} in health.")

    amount and adjust_inventory("gems", amount)
    damage and adjust_health(damage)

    print()
    info(f"The {mood} {color} dragon {message}")

def do_buy(name=None, *args):
    """Buy an item from the market."""
    require("buy", name, "item")
    place = current_place()
    item = get_item(name)

    if not name in current_place()["items"]:
        error(f"(buy) No {name} here.")

    if not item:
        error(f"Couldn't find details about: {name}", user=False)

    if not item.get("price"):
        error(f"(buy) {name} is not for sale.")

    if not can_afford(item["price"]):
        error(f"(buy) Sorry, you don't have {abs(item['price'])} gems.")

    adjust_inventory(name, 1)
    adjust_inventory("gems", item["price"])

    print()
    info(f"Bought a {name} for {abs(item['price'])} gems.")

def do_consume(name=None, *args):
    """Consume an item from inventory."""
    action = state()["command"]
    require(action, name, "item")

    item = get_item(name)

    if not item:
        error(f"({action}) Unable to find details about item: {item}",
                  user=False)

    if not get_inventory(name):
        info(f"Sorry, you don't have any {name} to {action}.")

    health_points = item.get("health")
    message = item.get("consume-msg", [])

    if not message:
        message.append(f"You {action} the {name}.")

    if health_points:
        adjust_health(health_points)
        message.append(f"\n You gain {health_points} health.")

    print()
    for text in message:
        info(text)
        print()
        time.sleep(1)

    adjust_inventory(name, -1)

def do_shop(*args):
    """Shop in the market."""
    market = current_place()
    if market["name"] != "market":
        error("Cannot shop unless in the market.", user=False)

    print()
    for item in (get_item(name) for name in market["items"]):
        info(
            item["icon"].ljust(4),
            item["name"].capitalize().ljust(30),
            abs(item["price"]),
        )


ACTIONS = {
    "buy": do_buy,
    "pet": do_pet,
    "drink": do_consume,
    "shop": do_shop,
    "stats": do_stats,
    "map": do_map,
    "inventory": do_inventory,
    "look": do_look,
    "examine": do_examine,
    "go": do_go,
    "jump": do_jump,
    "help": do_help,
    "quit": do_quit,
}

# alias -> command func
for cmd in COMMANDS:
    for alias in cmd["aliases"]:
        func = ACTIONS.get(cmd["name"])
        if not func:
            error(f"Missing action for {cmd['name']}")
        ACTIONS[alias] = func
