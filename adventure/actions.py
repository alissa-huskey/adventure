import random

from more_itertools import first

from .formatting import info, error, NotFound
from .args import require
from .objects import COLORS, MOODS, get_object
from .player import (
    get_inventory,
    adjust_health,
    adjust_inventory,
    current_location,
    inventory_for_action,
    can_afford,
    state,
)


ACTIONS = {}


def get_action(name):
    return ACTIONS[name]

def inventory_action(command, words):
    args = words[:]
    objects = inventory_for_action(command)
    thing = first(objects.intersection(args), None)
    state(thing=thing)

    # no such inventory action
    if not objects:
        raise NotFound()

    # missing required object for action
    if not args:
        error(f'You need to say what you want to {command}.')

    # thing not in inventory
    if not thing:
        error(f"({command}) You have no {args[0]} in your inventory.")

    # make sure thing is the first arg
    if thing and thing != args[0]:
        args.remove(thing)
        args.insert(0, thing)

    return (get_action(command), args)

def local_action(command, words):
    """Return command function, object, and args based on the players current
    location, or raise user error.
    """

    args = words[:]
    location = current_location()
    objects = location["actions"].get(command, set())
    thing = first(objects.intersection(args), None)
    state(thing=thing)

    # no such action at this location
    if command not in location["actions"]:
        raise NotFound()

    # missing required object for action
    if objects and not args:
        error(f'You need to say what you want to {command}.')

    # no valid object for this action
    if objects and not thing:
        error(f"({command}) There's no {args[0]} nearby.")

    # make sure thing is the first arg
    if thing and thing != args[0]:
        args.remove(thing)
        args.insert(0, thing)

    return (get_action(command), args)

def do_pet(item=None, color=None, *args):
    """."""
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

def do_buy(thing=None, *args):
    """."""
    require("buy", thing, "thing")
    location = current_location()
    item = get_object(thing)

    if not thing in current_location()["objects"]:
        error(f"(buy) No {thing} here.")

    if not item:
        error(f"Couldn't find details about: {thing}", user=False)

    if not item.get("price"):
        error(f"(buy) {thing} is not for sale.")

    if not can_afford(item["price"]):
        error(f"(buy) Sorry, you don't have {abs(item['price'])} gems.")

    adjust_inventory(thing, 1)
    adjust_inventory("gems", item["price"])
    print()
    info(f"Bought a {thing} for {abs(item['price'])} gems.")

def do_consume(name=None, *args):
    action = state()["command"]
    require(action, name, "object")

    thing = get_object(name)

    if not thing:
        error(f"({action}) Unable to find details about object: {thing}",
                  user=False)

    if not get_inventory(name):
        info(f"Sorry, you don't have any {name} to {action}.")

    health_points = thing.get("health")
    message = f"You {action} the {name}"

    adjust_inventory(name, -1)

    if health_points:
        adjust_health(health_points)
        message += f" and gain {health_points} health"

    print()
    info(f"{message}.")


ACTIONS = {
    "buy": do_buy,
    "pet": do_pet,
    "drink": do_consume,
}
