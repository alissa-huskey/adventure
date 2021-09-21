from .formatting import info, error
from .data.places import (
    COMPASS,
    MOVEMENTS,
    COMPASS_OPTIONS,
    PLACES,
    BY_POS,
    BY_NAME,
)

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
        error(f'No such place: {key!r}')

    return place

def get_direction(direction):
    direction = str(direction).lower()
    if not direction:
        return
    return COMPASS.get(direction[0])
