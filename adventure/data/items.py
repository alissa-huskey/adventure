COLORS = ["red", "black", "silver"]
MOODS = ["cheerful", "lonely", "cranky"]

ITEMS = {
    "desk": {
        "name": "desk",
        "desc": """
            A heavy book sits open on a stand on the desk. You also see an ink pot,
            a cup of feather quilled pens, and a pocket watch.
        """,
        "items": ["book"],
    },
    "book": {
        "name": "book",
        "desc": """
                The hefty leatherbound tome is open to a page that reads:

                    : At the edge of the woods is a cave that is home to a three headed
                      dragon, each with a different temperament.

                    : Legend says that if you happen upon the dragon sleeping, the brave
                      may pet one of its three heads.

                    : Choose the right head and you will be rewarded with great
                      fortunes.

                    : But beware, should choose poorly and it will surely mean your doom!
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
        "name": "healing elixr",
        "desc": "A small corked bottle filled with a swirling green liquid.",
        "price": -10,
        "health": 15,
        "actions": ["drink"],
        "consume-msg": [
            "You uncork the bottle.",
            "The swirling green liquid starts to bubble.",
            "You hesitatingly bring the bottle to your lips...",
            "then quickly down the whole thing!",
            "Surprisingly, it tastes like blueberries.",
            "You feel an odd tingling sensation starting at the top of your head... ",
            "...moving down your body...",
            "...down to the tips of your toes.",
        ],
        "icon": "🍵",
    },
    "crystal ball": {
        "name": "crystal ball",
        "price": -15,
        "desc": """
            A transparent sphere about the size of your palm that glows softly.  It is
            said to have magical properties.
        """,
        "icon": "🔮",
    },
    "dagger": {
        "name": "dagger",
        "price": -22,
        "desc": """
            A double-edged 14 inch dagger with a crescent shaped hardwood grip, metal
            crossguard, and curved studded metal pommel.
        """,
        "icon": "🗡    ",
    },
    "bench": {
        "name": "bench",
        "desc": "Wooden bench.",
    },
    "stick": {
        "name": "walking stick",
        "desc": "A gnarled walking stick.",
        "can-take": True,
    },
    "gate": {
        "name": "gate",
        "desc": """
            An open wooden gate connected to the low stone wall that runs along the edge
            of your garden.
        """
    },
    "dragon": {
        "name": "dragon",
        "short": "a fearsome three headed dragon",
        "desc": f"""
            A fearsome dragon with three heads, one {COLORS[0]}, one
            {COLORS[1]}, and one {COLORS[2]}.
        """,
    },
    "log": {
        "name": "fallen log",
        "desc": """
            The trunk of a tree fallen long ago bows up in the middle before coming to
            rest partway into the road. Moss and patches of purple headed mushrooms grow on
            the shady side.
        """,
        "items": ["mushrooms"],
    },
    "tree": {
        "name": "hollow tree",
        "desc": """
            The gnarled and twisted branches of an ancient moss covered tree loom over you.
        """
    },
    "floor": {
        "name": "forest floor",
        "desc": """
            Brilliant autumn leaves lay scattered amidst the foliage and detritis on the
            forest floor. You see an acorn nestled amongst the leaves.
        """,
        "items": ["acorn"],
    },
    "acorn": {
        "name": "acorn",
        "desc": "A brown acorn.",
        "can-take": True,
    },
    "mushrooms": {
        "name": "mushrooms",
        "desc": "Purple capped mushrooms.",
        "can-take": True,
    },
    "planters": {
        "name": "planters",
        "desc": "",
    },
    "pots": {
        "name": "flower pots",
        "desc": "",
    },
}
