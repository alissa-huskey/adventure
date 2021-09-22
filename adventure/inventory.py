from .items import get_item
from .data.player import PLAYER, INVENTORY_ACTIONS

def get_all_inventory():
    return PLAYER["inventory"]

def get_inventory(name):
    return PLAYER["inventory"][name]

def add_inventory_action(name):
    """Add to list of actions available for current inventory items."""
    item = get_item(name)
    if not item:
        return
    for action in item.get("actions", []):
        INVENTORY_ACTIONS[action].add(name)

def remove_inventory_action(name):
    """Remove from list of actions available for current inventory items."""
    item = get_item(name)
    if not item:
        return
    for action in item.get("actions", []):
        INVENTORY_ACTIONS[action].remove(name)

def adjust_inventory(name, amount):
    """Add to amount to players inventory name, and update the list of available for
    current inventory if applicable."""
    # if we're adding the first of this item
    if amount > 0 and not PLAYER["inventory"][name]:
        # add the actions for this item
        add_inventory_action(name)

    # modify inentory
    PLAYER["inventory"][name] += amount

    # if removing the last of this item
    if not PLAYER["inventory"][name]:

        # remove actions for this item
        remove_inventory_action(name)

        # don't keep zero item inventory items except for gems
        if name != "gems":
            del PLAYER["inventory"][name]

def inventory_for_action(name):
    return INVENTORY_ACTIONS[name]

def can_afford(price):
    return get_inventory("gems") >= abs(price)

