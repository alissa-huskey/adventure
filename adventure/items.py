from .data.items import COLORS, MOODS, ITEMS

def get_item(key):
    return ITEMS.get(key)
