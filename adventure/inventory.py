from adventure.items import get_item
from adventure.data.player import player, all_inventory_actions

def get_all_inventory():
    return player()["inventory"]

def get_inventory(name):
    return player()["inventory"][name]

def add_inventory_action(name):
    """Add to list of actions available for current inventory items."""
    item = get_item(name)
    if not item:
        return
    for action in item.get("actions", []):
        all_inventory_actions()[action].add(name)

def remove_inventory_action(name):
    """Remove from list of actions available for current inventory items."""
    item = get_item(name)
    if not item:
        return

    for action in item.get("actions", []):
        all_inventory_actions().get(action, set()).clear()

def adjust_inventory(name, amount):
    """Add to amount to players inventory name, and update the list of available for
    current inventory if applicable."""
    # if we're adding the first of this item
    if amount > 0 and not player()["inventory"][name]:
        # add the actions for this item
        add_inventory_action(name)

    # modify inentory
    player()["inventory"][name] += amount

    # if removing the last of this item
    if not player()["inventory"][name]:

        # remove actions for this item
        remove_inventory_action(name)

        # don't keep zero item inventory items except for gems
        if name != "gems":
            del player()["inventory"][name]

def inventory_for_action(name):
    return all_inventory_actions().get(name)

def can_afford(price):
    return get_inventory("gems") >= abs(price)

