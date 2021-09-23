"""Text based adventure game"""

import shlex
from pprint import pprint

from adventure.places import COMPASS_OPTIONS
from adventure.formatting import (
    info,
    error,
    debug,
    print_error,
    hr,
)
from adventure.player import (
    is_alive,
    current_place,
    current_position,
    state,
)
from adventure.actions import (
    contextual_action,
    do_jump,
    do_go,
    ACTIONS
)
from adventure import (
    Error,
    NotFound,
    UserError,
    SilentError,
)

def parse(response):
    """Return a tuple containing the (command, args) parsed from response"""
    words = shlex.split(response.strip())
    if not words:
        error(silent=True)

    state(command=words[0], args=words[1:])

    command = words.pop(0).lower()
    func = ACTIONS.get(command)

    # special case for n/s/e/w shortcuts
    if not func and command in COMPASS_OPTIONS:
        func = do_go
        words.insert(0, command)

    # special local and inventory actions
    if not func:
        try:
            func, words = contextual_action(command, words)
        except NotFound:
            try:
                func, words = contextual_action(command, words, local=True)
            except NotFound:
                ...

    if not func:
        error(f"No such command: {command!r}")

    state(args=words)
    return (func, words)

def main():
    hr()
    print("Welcome to the adventure!\n")
    do_jump("home")
    print()
    hr(char="~")
    print()

    while True:
        debug(position=current_position(), place=current_place()["name"])

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
            print()
            quit()


if __name__ == "__main__":
    main()
