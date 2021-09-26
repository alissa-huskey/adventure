import re

from adventure.formatting import info, merge, highlight
from adventure.player import (
    current_position,
    current_place,
    get_state,
    set_state,
)
from adventure.data.places import (
    COMPASS,
    MOVEMENTS,
    COMPASS_OPTIONS,
    PLACES,
    BY_POS,
    BY_NAME,
    trigger_hook,
)
from adventure import themes, NotFound

def show(place, long=False):
    """Print stylized place description

    Print long description if long is present or this place has not been visited.
    Otherwise print short description if it exists. Set visited to True.

    Args:
        long (bool, default=False): print the long description
    """

    info(themes.header(place.get("name", "Unnamed location").title()), before=1, after=1)

    if long or not get_state("places", place, "visited"):
        desc = place.get("description")
    else:
        desc = place.get("short") or place.get("description")

    if desc:
        desc = highlight(desc, place.get("items"), themes.items)
        desc = highlight(desc, place.get("actions"), themes.cmd)
        merge(desc, after=1)

    for letter, desc in place["look"].items():
        if not desc: continue
        direction = get_direction(letter)
        info(f"To the {themes.compass(direction)} is {desc}.")
    print()
    set_state("places", place["name"], {"visited": True})

def get_place(key):
    """Return the place associated with either its name or position key.

    >>> get_place((0, 0))["name"]
    'home'

    >>> get_place("home")["position"]
    (0, 0)
    """
    if isinstance(key, str):
        place = BY_NAME.get(key)
    else:
        place = BY_POS.get(key)

    if not place:
        raise NotFound()

    return place

def get_direction(direction):
    direction = str(direction).lower()
    if not direction:
        return
    return COMPASS.get(direction[0])

def goto(pos):
    """Update the players pos(ition) and place, or return False if no such
    position exists."""
    prev = current_place() or {}
    place = get_place(pos)
    if not place:
        return False


    trigger_hook("leave", prev.get("name"))

    current_position(pos)
    current_place(place)

    trigger_hook("enter", place.get("name"))

    return place

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

