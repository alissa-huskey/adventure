import random
import time

from more_itertools import first

from adventure.args import require, validate, extra_args
from adventure.items import COLORS, MOODS, ITEMS, get_item
from adventure.help import get_help
from adventure.player import (
    adjust_health,
    current_place,
    state,
    get_health,
    save_game,
    load_game,
    player,
    get_state,
    set_state,
)
from adventure.hints import get_hint, active_hints, trigger_event
from adventure.data.help import COMMANDS
from adventure.formatting import (
    info,
    debug,
    error,
    NotFound,
    bar,
    merge,
    Grid,
    Table,
    MAX,
    print_gems,
    apply_state,
    hr,
    TERM,
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
    highlight,
)
from adventure import themes

ACTIONS = {}

## functions ####################################

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
                error(f"There's no {args[0]} nearby.")
            else:
                error(f"You have no {args[0]} in your inventory.")

        # make sure item is the first arg
        if item != args[0]:
            args.remove(item)
            args.insert(0, item)

    return (get_action(command), args)

def get_action(name):
    """Return the command function for a particular name or alias"""
    action = ACTIONS.get(name)
    if action:
        return action.get("func")

## action functions #############################

def do_buy(name=None, *args):
    """Buy an item from the market."""
    require("buy", name, "item")
    extra_args("buy", args)

    place = current_place()
    item = get_item(name)

    if not name in current_place()["items"]:
        error(f"No {name} here.")

    if not item:
        error(f"Couldn't find details about: {name}", user=False)

    if not item.get("price"):
        error(f"{name} is not for sale.")

    if not can_afford(item["price"]):
        error(f"Sorry, you don't have {abs(item['price'])} gems.")

    adjust_inventory(name, 1)
    adjust_inventory("gems", item["price"])

    info(f"Bought a {name} for {abs(item['price'])} gems.", before=1)

def do_consume(name=None, delay=1, *args):
    """Consume an item from inventory."""
    action = state()["command"]

    require(action, name, "item")
    extra_args(action, args)

    item = get_item(name)

    if not item:
        error(f"I don't know what a {name!r} is.")

    if not get_inventory(name):
        error(f"Sorry, you don't have any {name} to {action}.")

    health_points = item.get("health")

    if health_points and player()["health"] >= 100:
        error(f"Don't {action} the {name} when you're healthy!")

    adjust_inventory(name, -1)

    message = item.get("consume-msg", [])

    if not message:
        message.append(f"You {action} the {name}.")

    if health_points:
        adjust_health(health_points)
        message.append(f"\n You gain {health_points} health.")

    print()
    for text in message:
        info(text, after=1)
        time.sleep(delay)

def do_examine(name=None, *args):
    """Look at an item in the current place or in inventory."""

    require("examine", name, "item")
    extra_args("examine", args)

    if name in ["self", "me"]:
        do_stats()
        return

    item = get_item(name)
    qty = get_inventory(name)

    if not item:
        error(f"I don't know what a {name!r} is")

    if not (name in current_place()["items"] or qty):
        error(f"There is no {name!r} in {current_place()['name']}.")

    price = item.get("price")
    details = ""
    if price and current_place()["name"] == "market":
        details = f"{abs(price)} gems"

    icon = item.get("icon", "")
    if icon:
        icon = icon.ljust(4)

    title = item.get("name", "Unnamed place")

    info(
        icon,
        themes.header(title.title()) + \
        details.rjust(MAX-len(title)-len(icon)),
        before=1,
        after=1,
        sep="",
    )

    desc = apply_state(item["desc"], get_state("items", item))
    desc = highlight(desc, {themes.items: item.get("items")})
    merge(desc)

    if qty:
        info(
            " "*4,
            f"Inventory: (x {qty:>2})".rjust(MAX-4),
            before=1,
            sep=""
        )
    trigger_event(f"examine_{name}")

def do_go(direction=None, steps=1, *args):
    """Move the player to a new position based on the direction they wish to
    travel."""
    direction = require("go", direction, "direction", choices=COMPASS.values(),
                        options=COMPASS_OPTIONS)
    steps = require("go", steps, "steps", klass=int)
    extra_args("go", args)

    pos = step(current_position(), direction, steps)
    try:
        goto(pos)
    except NotFound:
        error("You can't go that way.")

    show(current_place())

def do_tutorial():
    """Tutorial"""
    commands = [x["name"] for x in COMMANDS]
    fmt = lambda text, items=[]: info(text, styles={themes.cmd: commands,
                                                   themes.items: items})

    info("""
            To interact with the world around you, type what you want to do. Most often
            in the form of a verb, sometimes followed by a noun.
         """,
         styles={themes.cmd: ["verb"], themes.items: ["noun"]},
         should_merge=True,
         before=1,
    )

    info("For example...", after=1)

    fmt('...you can look around.')
    fmt('...if you see something you can examine it.', ["it"])
    fmt('...to move go direction.', ["direction"])

    info("Most actions have shortcuts like l for look or x for examine.",
         styles={themes.cmd: ["l", "look", "x", "examine"]},
         before=1,
         after=1,
    )

    info("""
            Special actions are usually highlighted, but sometimes you'll have only your
            wit to guide you.
         """,
         should_merge=True,
         styles={themes.cmd: ["highlighted"]},
    )

    info(f"""You can get a list of commands by typing help. Or get details about a
         particular command with help {themes.items('action')}.""",
        styles={themes.cmd: ["help"]},
         should_merge=True,
        after=1,
    )


def do_hints(switch_to=None, *args):
    """Turn hints on or off."""
    toggle = ("off", "on", None)
    validate("hints", switch_to, "switch_to", options=toggle, klass=str)

    if switch_to:
        current = player().get("hints")
        player()["hints"] = bool(toggle.index(switch_to))

    current = player().get("hints")
    info(f"Hints mode is: {toggle[current]}", before=1)


def do_intro():
    """Welcome message"""
    trigger_event("do_intro")

    hr(after=1)

    info(themes.header("Welcome to the adventure!"), after=1)

    info("Explore the land and discover great wonders and treasure! Just try not to get dead.", after=1)

    info(
        themes.hint(
            f"Hint: For a how-to guide type: " + \
            themes.cmd('tutorial') + \
            themes.hint(".")
        ),
        should_wrap=False,
        after=1,
    )

    info("""
            You are an explorer seeking fortune and fun.
            Your story beings in your very own cottage.
         """,
         should_merge=True,
    )


def do_inventory(*args):
    """Show inventory"""
    inventory = get_all_inventory().copy()
    inventory.pop("gems")

    info(themes.header("Inventory"), before=1, after=1)

    if not inventory:
        info("Empty.")

    for name, amount in inventory.items():
        item = get_item(name)

        info(
            item.get("icon", "").ljust(4),
            name.capitalize().ljust(30),
            f"(x {amount:>2})"
        )

def do_help(command=None, *args):
    extra_args("help", args)

    # list help topics
    if not command:
        width = max(map(len, [x["name"] for x in COMMANDS])) + 2
        for cmd in COMMANDS:
            if cmd.get("listed", True):
                sep = "  "
                alias = first(cmd.setdefault("aliases", []), "")
                name = cmd["name"]
                if alias:
                    sep = themes.normal(", ")

                info(
                    themes.cmd(alias.rjust(3)) + sep,
                    themes.cmd(name.ljust(width)),
                    cmd["description"]
                )
        return

    # help for a specific command
    cmd = get_help(command)
    if not cmd:
        error(f"No such command: {command!r}")

    trigger_event("help_action")
    titles = ["arguments", "examples", "titles", "usage", "aliases"]
    options = dict(
        align={0: "rjust"},
        sizes={0: (max(map(len, titles)) + 1)},
        padding=2,
    )

    tables = [Table(**options)]
    usage = [themes.cmd(cmd["name"])] + \
            [themes.usage_arg(arg) for arg in cmd.setdefault("arguments", {}).setdefault("required", {})] + \
            [f"[{themes.usage_arg(arg)}]" for arg in cmd["arguments"].setdefault("optional", {})]

    tables[-1].append([themes.help_title("Usage:"), " ".join(usage)])
    tables[-1].append(["", cmd["description"]])
    tables[-1].append()

    if cmd.setdefault("aliases", []):
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

    if cmd.get("examples", []):
        tables.append(Table(**options))
        examples = [f"> {e}" for e in cmd["examples"]]
        tables[-1].append([themes.help_title("Examples:"), examples.pop(0)])
        for e in examples:
            tables[-1].append(["", e])

    print()
    for t in tables:
        print(t.text)

def do_jump(name=None, *args, should_show=True):
    """Jump straight to a place"""
    require("jump", name, "place")
    extra_args("jump", args)

    try:
        place = get_place(name)
    except NotFound:
        error(f"I don't know where {name!r} is.")

    try:
        goto(place["position"])
    except NotFound:
        error("Failed to jump to: {name!r} at {place['position']}", user=False)

    if should_show:
        show(current_place())

def do_look(*args):
    """Describe the scenery in the direction the player looks."""
    extra_args("look", args)

    show(current_place(), long=True)

def do_map(*args):
    """Show a map"""
    extra_args("map", args)

    grid = Grid()
    for place in PLACES:
        x, y = place.get("position")
        name = place.get("name", "")

        if current_place() == place:
            name = themes.header(name)
        try:
            debug(f"place: {place['name']!r}, ({x=}, {y=})")
            grid.set(y, x, name)
        except IndexError:
            error(f"Couldn't map location: {place['name']!r}, ({x=}, {y=})", user=False)

    info(themes.header("Map"), before=2, after=1)
    print(grid.render(), "\n")

def do_pet(item=None, color=None, *args):
    """Pet one of the dragon heads."""
    item_choices = ["dragon", "head"]
    if item and (item not in item_choices) and (not color):
        item, color = "dragon", item

    if item and color and color in item_choices:
        item, color = color, item

    color = require("pet", color, "color", choices=COLORS)
    require("pet", item, "item", choices=item_choices)
    extra_args("pet", args)

    current = get_state("items", get_item("dragon"), "state")
    if current != "sleeping":
        info("The dragon eyes you askance.", before=1, after=1)
        info("You back away slowly.", after=1)
        return

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

    set_state("items", "dragon", {"state": "awake"})

    info(f"The {mood} {color} dragon {message}", before=1)
    return amount, damage

def do_quit(*args):
    quit()

def do_menu(*args):
    """Shop in the market."""
    market = current_place()
    if market["name"] != "market":
        error("Cannot shop unless in the market.", user=False)

    info(themes.header("Menu"), after=1, before=1)
    for item in (get_item(name) for name in market["items"]):
        info(
            item["icon"].ljust(4),
            item["name"].capitalize().ljust(30),
            abs(item["price"]),
        )

def do_stats(*args):
    """Show player stats"""
    print()
    bar("health ❤️", get_health())
    print_gems(get_inventory("gems"))

def do_save(*args):
    """Save your game"""
    path = save_game()

    print()
    debug(path=path)
    info("Game saved.")

def do_load(*args):
    """Load a saved game"""
    data = load_game()

    print()
    debug(data=data)
    title = "Loaded Game"
    info(
        themes.header(title),
        data.get("saved_at").strftime("%b %-d, %Y %-I:%M %p").rjust(MAX-len(title)),
        after=1,
    )
    do_stats()
    do_inventory()
    do_look()

def do_hint(show_all=False, *args):
    """Give a hint."""
    commands = [x["name"] for x in COMMANDS]
    items = [x["name"] for x in ITEMS.values()]
    styles = {themes.items: items, themes.cmd: commands}
    place = current_place()
    if show_all == "all":
        data = [(x["name"], highlight(x["hint"], styles)) for x in active_hints(place["name"])]
        table = Table(table=data, padding=2)
        print()
        print(table.text)
    else:
        hint = get_hint(place["name"])
        info(hint["hint"], styles={themes.items: items, themes.cmd: commands}, before=1)


## ACTIONS #######################################

ACTIONS = {
    "buy": {"name": "buy", "func": do_buy, "place": "market"},
    "drink": {"name": "drink", "func": do_consume, "item": "elixir"},
    "examine": {"name": "examine", "func": do_examine},
    "go": {"name": "go", "func": do_go},
    "help": {"name": "help", "func": do_help},
    "intro": {"name": "intro", "func": do_intro},
    "inventory": {"name": "inventory", "func": do_inventory},
    "jump": {"name": "jump", "func": do_jump},
    "load": {"name": "load", "func": do_load},
    "look": {"name": "look", "func": do_look},
    "map": {"name": "map", "func": do_map},
    "pet": {"name": "pet", "func": do_pet, "place": "cave"},
    "save": {"name": "save", "func": do_save},
    "menu": {"name": "menu", "func": do_menu, "place": "market"},
    "stats": {"name": "stats", "func": do_stats},
    "quit": {"name": "quit", "func": do_quit},
    "hints": {"name": "hints", "func": do_hints},
    "tutorial": {"name": "tutorial", "func": do_tutorial},
}

# alias -> command func
for cmd in COMMANDS:
    for alias in cmd.get("aliases", []):
        func = ACTIONS.get(cmd["name"])
        if not func:
            error(f"Missing action for {cmd['name']}")
        ACTIONS[alias] = func
