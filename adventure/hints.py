from more_itertools import first, always_iterable

from adventure.formatting import info
from adventure import themes

HINTS = {}
EVENTS = {}
ACTIVE_HINTS = []

def register_hint(name, message, add, remove, commands=[], items=[], place=None, limit=1):
    """Add hint and register related events."""

    HINTS[name] = {
        "name": name,
        "hint": message,
        "seen": 0,
        "place": place,
        "limit": limit,
        "commands": commands,
        "items": items,
    }

    for event in always_iterable(add):
        if name not in EVENTS.setdefault(event, {}).setdefault("add", []):
            EVENTS[event]["add"].append(name)

    for event in always_iterable(remove):
        if name not in EVENTS.setdefault(event, {}).setdefault("remove", []):
            EVENTS[event]["remove"].append(name)


def trigger_event(action):
    """Update ACTIVE_HINTS based on triggered event"""

    event = EVENTS.get(action, {})

    for name in event.get("add", []):
        if not HINTS[name]["seen"]:
            ACTIVE_HINTS.insert(0, name)

    for name in event.get("remove", []):
        try:
            ACTIVE_HINTS.remove(name)
        except ValueError:
            ...

def active_hints(place):
    """Return a list of active and not seen hints"""
    active = [HINTS[x] for x in ACTIVE_HINTS]
    fresh = [x for x in active if not x["limit"] or x["seen"] < x["limit"]]
    hints = [x for x in fresh if not x["place"] or x["place"] == place]
    return hints

def get_hint(place):
    """Return the first active hint."""
    hint = first(active_hints(place), {})
    if hint:
        hint["seen"] += 1
        trigger_event(f"finished-{hint['name']}")
    return hint

def show_hint(place):
    """Display a hint."""
    hint = get_hint(place["name"])

    if hint:
        info(
            themes.hint(f'Hint: {hint["hint"]}'),
            alignment="right",
            styles={
                themes.items: hint["items"],
                themes.cmd: hint["commands"],
            },
            indent=0,
        )

def init():
    register_hint(
        "first-look",
        "Try taking a look around.",
        add="do_intro",
        remove="do_look",
        place="home",
        limit=None,
        commands=["look"],
    )

    register_hint(
        "examine-desk",
        "Is there anything of interest on the desk?",
        add="do_look",
        remove="examine_desk",
        place="home",
        limit=None,
        items=["desk"],
    )

    register_hint(
        "examine-book",
        "I wonder what the book has to say.",
        add="examine_desk",
        remove="examine_book",
        place="home",
        limit=None,
        items=["book"],
    )

    register_hint(
        "go",
        "Maybe it's time to go.",
        add="examine_book",
        remove="do_go",
        place="home",
        commands=["go"],
    )

    register_hint(
        "check-stats",
        "It might be a good time to check your stats.",
        add="do_pet",
        remove="do_stats",
        commands=["stats"],
    )

    register_hint(
        "check-inventory",
        "Have you looked at your inventory lately?",
        add="do_buy",
        remove="do_inventory",
        commands=["inventory"],
    )

    register_hint(
        "dragon-sleep",
        "I bet he'll stay awake until you go away.",
        place="cave",
        remove="leave_cave",
        add="do_pet",
        commands=["go"],
    )

    register_hint(
        "examine",
        "Is there something you could examine more closely?",
        add="finished-look-around",
        remove="do_examine",
        commands=["examine"],
    )

    register_hint(
        "help-command",
        "Try help ?",
        add=["do_help"],
        remove=["help_action"],
        limit=None,
        commands=["help"],
    )

    register_hint(
        "help",
        "Perhaps you would like to peruse the help.",
        add=["finished-examine-desk"],
        remove="do_help",
        limit=None,
        commands=["help"],
    )

    register_hint(
        "spend-gems",
        "I wonder where you could go to spend some gems.",
        add="get_gems",
        remove="enter_market",
        commands=["go"],
    )

    register_hint(
        "find-clue",
        "Don't you have a book that mentions dragons?",
        add="enter_cave",
        remove=["examine_book", "do_pet"],
        place="cave",
        items=["book"],
    )

    register_hint(
        "look-around",
        "You could always take another look around.",
        add="leave_home",
        remove="do_look",
        commands=["look"],
    )
