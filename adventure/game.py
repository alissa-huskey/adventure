"""Text based adventure game"""

import shlex
from pprint import pprint
import sys
from contextlib import contextmanager
from console import fx


from adventure.data.help import COMMANDS
from adventure.player import state
from adventure.places import COMPASS_OPTIONS
from adventure.inventory import get_inventory
from adventure.formatting import (
    info,
    error,
    debug,
    print_error,
    hr,
    highlight,
    merge,
)
from adventure.player import (
    is_alive,
    current_place,
    current_position,
    state,
)
from adventure.actions import (
    contextual_action,
    do_intro,
    do_jump,
    do_go,
    ACTIONS
)
from adventure import (
    UnexpectedError,
    NotFound,
    UserError,
    SilentError,
    themes,
)

def func_from_compass(command, words, *args):
    """Return func, args for commands that match COMPASS_OPTIONS or raise NotFound"""
    if command not in COMPASS_OPTIONS:
        raise NotFound()

    func = do_go
    words.insert(0, command)

    return func, words

def func_from_place(command, words, action):
    """Return func, args for for commands in current place or raise NotFound"""
    if not action:
        raise NotFound()

    place = action.get("place")
    if not (place and place == current_place()["name"]):
        raise NotFound()

    return contextual_action(command, words, local=True)

def func_from_item(command, words, action):
    """Return func, args for for current inventory commands or raise NotFound"""
    if not action:
        raise NotFound()

    item = action.get("item")
    if not (item and get_inventory(item)):
        raise NotFound()

    return contextual_action(command, words)

def func_from_action(command, words, action):
    """Return func, args for for global commands or raise NotFound"""
    if not action or action.get("item") or action.get("place"):
        raise NotFound()

    return action["func"], words

def parse(response):
    """Return a tuple containing the (command, args) parsed from response"""
    words = shlex.split(response.strip())
    if not words:
        error(silent=True)

    state(command=words[0], args=words[1:], action=None)

    getters = [
        func_from_compass,
        func_from_place,
        func_from_item,
        func_from_action,
    ]

    command = words.pop(0).lower()
    func = None

    action = ACTIONS.get(command)

    for func_getter in getters:
        try:
            func, words = func_getter(command, words, action)
        except NotFound:
            ...
        if func:
            break

    if not func:
        error(f"No such command: {command!r}")

    state(args=words)

    if action:
        state(action=action["name"])

    return (func, words)


@contextmanager
def catcher():
    """Catch and handle exceptions."""
    try:
        yield
    except (EOFError, KeyboardInterrupt):
        quit()
    except SilentError:
        ...
    except (UnexpectedError, UserError) as err:
        print_error(err)

@contextmanager
def doer():
    """Do an action."""
    with catcher():
        debug(position=current_position(), place=current_place()["name"])
        yield

    hr(char="~", before=1, after=1)

    if not is_alive():
        info("Oh no, you're dead!", after=1)
        quit()

def main():

    do_jump("home", should_show=False)

    with doer():
        hr()
        info(themes.header("Welcome to the adventure!"), before=1)
        #  info(fx.italic("Explore the lands. Find treasure. Buy cool stuff."))

        do_intro()

    while True:

        with doer():
            cmd, args = None, None
            with catcher():
                cmd, args = parse(input("> "))

            if cmd:
                cmd(*args)


if __name__ == "__main__":
    main()
