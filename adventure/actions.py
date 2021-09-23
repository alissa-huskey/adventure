import random
import time

from more_itertools import first

from .formatting import info, error, NotFound
from .args import require
from .items import COLORS, MOODS, get_item
from .player import adjust_health, current_place, state
from .inventory import (
    get_inventory,
    adjust_inventory,
    inventory_for_action,
    can_afford,
)


ACTIONS = {}


def get_action(name):
    return ACTIONS.get(name)

def inventory_action(command, words):
    """Return command function, and args from actions available on inventory items
    associated with the current command, or raise NotFound error.
    """
    args = words[:]
    items = inventory_for_action(command)
    item = first(items.intersection(args), None)
    state(item=item)

    # no such inventory action
    if not items:
        raise NotFound()

    # item is required
    if items:

        # missing required item for action
        if not args:
            error(f'You need to say what you want to {command}.')

        # item not in inventory
        if not item:
            error(f"({command}) You have no {args[0]} in your inventory.")

        # make sure item is the first arg
        if item and item != args[0]:
            args.remove(item)
            args.insert(0, item)

    return (get_action(command), args)

def local_action(command, words):
    """Return command function, item, and args based on the players current
    place, or raise user error.
    """

    args = words[:]
    place = current_place()
    items = place["actions"].get(command, set())

    # no such action at this place
    if command not in place["actions"]:
        raise NotFound()

    # if item is required
    if items:
        item = first(items.intersection(args), None)
        state(item=item)

        # missing required item for action
        if items and not args:
            error(f'You need to say what you want to {command}.')

        # no valid item for this action
        if items and not item:
            error(f"({command}) There's no {args[0]} nearby.")

        # make sure item is the first arg
        if item and item != args[0]:
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
}
