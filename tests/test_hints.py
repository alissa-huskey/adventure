import pytest
from more_itertools import always_iterable

from adventure import hints
from adventure.hints import (
    register_hint,
    trigger_event,
    active_hints,
    get_hint,
)

@pytest.mark.parametrize("name, message, add, remove, place", [
    ("bye", "Off you go.", ["do_intro", "do_restore"], ["do_goodbye", "do_dead"], "cave"),
    ("oh-hai", "Well hello there young sir.", "do_intro", "do_hello", None),
    ("bye", "Off you go.", "do_intro", "do_goodbye", "cave"),
])
def test_register_hint(name, message, add, remove, place):
    register_hint(
        name,
        message,
        add=add,
        remove=remove,
        place=place,
    )

    assert hints.HINTS[name]
    assert hints.HINTS[name]["hint"] == message
    assert hints.HINTS[name]["place"] == place

    for event in always_iterable(add):
        assert name in hints.EVENTS[event]["add"]

    for event in always_iterable(remove):
        assert name in hints.EVENTS[event]["remove"]

def test_trigger_event():
    hints.HINTS = {
        "get-clue": {
            "name": "get-clue",
            "hint": "Get a clue",
            "seen": 0,
            "place": None,
            "limit": 1,
        }
    }

    hints.EVENTS = {
        "do_thing": {
            "add": ["get-clue"],
        },
        "leave_place": {
            "remove": ["get-clue"],
        }
    }

    trigger_event("do_thing")

    assert "get-clue" in hints.ACTIVE_HINTS

    trigger_event("leave_place")

    assert "get-clue" not in hints.ACTIVE_HINTS

#
@pytest.mark.parametrize("place, active, included, excluded", [
    (
        "home",
        ["call-mom", "waste-time", "take-nap", "read-book"],
        ("call-mom", "take-nap"),
        ("waste-time", "read-book"),
    ),
])
def test_active_hints(place, active, included, excluded):
    hints.HINTS = {
        "call-mom": {
            "hint": "Have you called your mother lately?",
            "seen": 0,
            "place": None,
            "limit": 1,
        },
        "waste-time": {
            "hint": "Have you considered killing time?",
            "seen": 1,
            "place": None,
            "limit": 1,
        },
        "take-nap": {
            "hint": "You should probably take a nap.",
            "seen": 0,
            "limit": 1,
            "place": "home",
        },
        "read-book": {
            "hint": "How about reading a book?",
            "seen": 1,
            "limit": 1,
            "place": "home",
        }
    }
    hints.ACTIVE_HINTS = active

    available = active_hints("home")
    for name in included:
        assert hints.HINTS[name] in available

    for name in excluded:
        assert hints.HINTS[name] not in available

def test_get_hint():
    hints.HINTS = {
        "call-mom": {
            "name": "call-mom",
            "hint": "Have you called your mother lately?",
            "seen": 0,
            "place": None,
            "limit": 1,
        },
        "waste-time": {
            "name": "waste-time",
            "hint": "Have you considered killing time?",
            "seen": 1,
            "place": None,
            "limit": 1,
        },
        "take-nap": {
            "name": "take-nap",
            "hint": "You should probably take a nap.",
            "seen": 0,
            "limit": 1,
            "place": "home",
        },
        "read-book": {
            "name": "read-book",
            "hint": "How about reading a book?",
            "seen": 1,
            "limit": 1,
            "place": "home",
        }
    }
    hints.ACTIVE_HINTS = ["call-mom", "waste-time", "take-nap", "read-book"]

    hint = get_hint("home")
    assert hint
    assert hints.HINTS[hint["name"]]["seen"]

