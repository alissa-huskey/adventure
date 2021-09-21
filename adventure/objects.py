COLORS = ["red", "black", "silver"]
MOODS = ["cheerful", "lonely", "cranky"]

OBJECTS = {
    "desk": {
        "name": "desk",
        "desc": """
            A large tome sits open on a stand on the desk. You also see an ink pot,
            a cup of feather quilled pens, and a pocket watch.
        """,
    },
    "book": {
        "name": "book",
        "desc": """
            Legend says in a cave nearby is a three headed dragon.
        """,
    },
    "chair": {
        "name": "chair",
        "desc": "High backed chair with red upholstery.",
    },
    "counter": {
        "name": "counter",
        "desc": """
            A long counter with a water basin, a cutting board and knife, and
            rolling pin.
        """,
    },
    "stove": {
        "name": "stove",
        "desc": "A claw footed cast iron wood burning stove.",
    },
    "shelves": {
        "name": "shelves",
        "desc": """
            On the shelves are plates, bowls and cups, bottles and spices, and
            other foodstuffs.
        """
    },
    "door": {
        "name": "front door",
        "desc": """
            A heavy arched door made of carved dark wood with an iron door handle
            bolt lock, and hinge straps.
        """
    },
    "bed": {
        "name": "bed",
        "desc": """
            In a nook above dark wood drawers is a bed with slightly rumpled
            sheets. The recessed shelves are lined with books as well as an oil
            lamp.
        """
    },
    "window": { "name": "", "desc": "" },
    "rug": { "name": "", "desc": "" },
    "fountain": {
        "name": "fountain",
        "desc": "a burbling fountain",
    },
    "cloak": {
        "name": "cloak",
        "desc": "a fancy cloak",
    },
    "elixr": {
        "name": "elixr",
        "desc": "a healing elixr",
        "price": -10,
        "health": 5,
        "actions": ["drink"],
        "consume-msg": "the tasty beverage"
    },
    "bench": {
        "name": "bench",
        "desc": "Wooden bench.",
    },
    "stick": {
        "name": "walking stick",
        "desc": "A gnarled walking stick.",
        "takable": True,
    },
    "gate": {
        "name": "gate",
        "desc": "Open fence gate.",
    },
    "dragon": {
        "name": "dragon",
        "short": "a fearsome three headed dragon",
        "desc": f"""
            A fearsome dragon with three heads, one {COLORS[0]}, one
            {COLORS[1]}, and one {COLORS[2]}.
        """,
    },
}

def get_object(key):
    return OBJECTS.get(key)
