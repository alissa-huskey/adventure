from contextlib import nullcontext as does_not_raise

import pytest

from adventure.inventory import adjust_inventory, get_inventory
from adventure import NotFound, UserError
from adventure.player import state, current_place, get_health
from adventure.actions import (
    contextual_action,
    get_action,

    do_buy,
    do_consume,
    do_examine,
    do_go,
    do_inventory,
    do_help,
    do_jump,
    do_look,
    do_map,
    do_pet,
    do_quit,
    do_shop,
    do_stats,
)

@pytest.mark.parametrize("item,action,in_args,klass,message", [
    ("gems", "drink", ["elixr"], NotFound, "item not in inventory"),
    ("gems", "xxx", [], NotFound, "no such inventory command"),
    ("elixr", "drink", [], UserError, "missing required arg"),
])
def test_contextual_action_inventory_raises(item, action, in_args, klass, message):
    adjust_inventory(item, 1)

    with pytest.raises(klass) as ex:
        func, args = contextual_action(action, in_args)

    if ex.type is not klass:
        breakpoint()

@pytest.mark.parametrize("item,action,in_args,func_name,out_args,message", [
    ("elixr", "drink", ["elixr"], "do_consume", ["elixr"], "inventory action, with args"),
])
def test_contextual_action_inventory(item, action, in_args, func_name, out_args, message):
    adjust_inventory(item, 1)

    func, args = contextual_action(action, in_args)

    assert func.__name__ == func_name, f"{message}: {action}, {in_args}"
    assert args == out_args

@pytest.mark.parametrize("place,action,in_args,func_name,out_args,message", [
    ("market", "shop", [], "do_shop", [], "local action, no args"),
    ("market", "buy", ["elixr"], "do_buy", ["elixr"], "local action, with required arg"),
    ("cave", "pet", ["red", "dragon"], "do_pet", ["dragon", "red"], "local action, reorder item"),
    ("cave", "pet", ["dragon", "red"], "do_pet", ["dragon", "red"], "local action, correct order"),
])
def test_contextual_action_local(place, action, in_args, func_name, out_args, message):
    do_jump(place)

    func, args = contextual_action(action, in_args, local=True)

    assert func.__name__ == func_name, f"{message}: {action}, {in_args}"
    assert args == out_args

@pytest.mark.parametrize("place,action,in_args,klass", [
    ("market", "xxx", [], NotFound),
    ("market", "buy", [], UserError),
    ("market", "buy", ["xxx"], UserError),
])
def test_contextual_action_local_raises(place, action, in_args, klass):
    do_jump(place)

    with pytest.raises(klass):
        func, args = contextual_action(action, in_args, local=True)


@pytest.mark.parametrize("func, args, context", [
    (do_inventory, [], does_not_raise()),
    (do_map, [], does_not_raise()),
    (do_stats, [], does_not_raise()),
])
def test_do_actions(func, args, context):
    """Simple actions that just print something."""
    with context:
        func(*args)

@pytest.mark.parametrize("cmd, func", [
    ("help", do_help),
    ("xxx", None),
    ("?", do_help),
])
def test_get_action(cmd, func):
    assert get_action(cmd) == func

@pytest.mark.parametrize("item, args, amount, context", [
    ("elixr", [], -10, does_not_raise()),
    ("", [], 0, pytest.raises(UserError, match="buy needs a item")),
    ("elixr", ["xxx"], -10, pytest.raises(UserError, match="buy received unknown arguments: xxx")),
    ("xxx", [], 0, pytest.raises(UserError, match="No xxx here")),
    ("elixr", [], 5, pytest.raises(UserError, match=r"you don't have \d+ gems")),
])
def test_do_buy(item, args, amount, context):
    do_jump("market")
    adjust_inventory("gems", abs(amount))

    with context as ex:
        do_buy(*[item, *args])

    if not ex:
        assert get_inventory(item)
        assert not get_inventory("gems")

@pytest.mark.parametrize("item, args, amount, context", [
    ("elixr", [], 1, does_not_raise()),
    (None, [], 0, pytest.raises(UserError, match="drink needs a item")),
    ("elixr", ["xxx"], 0, pytest.raises(UserError, match="drink received unknown arguments")),
    ("elixr", [], 0, pytest.raises(UserError, match="Sorry, you don't have any")),
    ("xxx", [], 0, pytest.raises(UserError, match="I don't know what a 'xxx' is")),
])
def test_do_consume(item, args, amount, context):
    if amount:
        adjust_inventory(item, abs(amount))

    state(command="drink")

    with context as ex:
        do_consume(*[item, 0, *args])

    if not ex:
        assert not get_inventory(item)

@pytest.mark.parametrize("place, amount, item, args, context", [
    ("home", 0, None, [], pytest.raises(UserError, match="examine needs a item")),
    ("home", 0, "bed", [], does_not_raise()),
    ("home", 0, "me", [], does_not_raise()),
    ("home", 0, "bed", ["xxx"], pytest.raises(UserError, match="examine received unknown arguments")),
    ("home", 1, "elixr", [], does_not_raise()),
    ("home", 0, "elixr", [], pytest.raises(UserError, match="There is no 'elixr' in home")),
    ("home", 0, "xxx", [], pytest.raises(UserError, match="I don't know what a 'xxx' is")),
    ("home", 0, "dragon", [], pytest.raises(UserError, match="There is no 'dragon' in home")),
])
def test_do_examine(place, amount, item, args, context):
    do_jump(place)

    if amount:
        adjust_inventory(item, abs(amount))

    with context as ex:
        do_examine(item, *args)

@pytest.mark.parametrize("place, direction, dest, args, context", [
    ("home", None, None, [], pytest.raises(UserError, match="go needs a direction")),
    ("home", "xxx", None, [], pytest.raises(UserError, match="direction invalid: 'xxx'")),
    ("home", "w", None, ["xxx"], pytest.raises(UserError, match="steps should be a int")),
    ("home", "w", None, ["23"], pytest.raises(UserError, match="You can't go that way")),
    ("home", "east", "courtyard", [], does_not_raise()),
    ("home", "east", "road", ["3"], does_not_raise()),
    ("home", "west", None, [], pytest.raises(UserError, match="You can't go that way")),
])
def test_do_go(place, direction, dest, args, context):
    do_jump(place)

    with context as ex:
        do_go(direction, *args)

    if not ex:
        assert current_place().get("name") == dest


@pytest.mark.parametrize("args, context", [
    ([], does_not_raise()),
    (["look"], does_not_raise()),
    (["map"], does_not_raise()),
    (["?"], does_not_raise()),
    (["xxx"], pytest.raises(UserError, match="No such command")),
    (["quit", "xxx"], pytest.raises(UserError, match="received unknown arguments")),
])
def test_do_help(args, context):
    with context:
        do_help(*args)

@pytest.mark.parametrize("place, args, context", [
    ("cave", [], does_not_raise()),
    (None, [], pytest.raises(UserError, match="jump needs a place")),
    ("home", ["xxx"], pytest.raises(UserError, match="unknown argument")),
    ("xxx", [], pytest.raises(UserError, match="I don't know where 'xxx' is"))
])
def test_do_jump(place, args, context):
    with context as ex:
        do_jump(place, *args)

    if not ex:
        current_place()["name"] == place

@pytest.mark.parametrize("place, args, context", [
    ("home", [], does_not_raise()),
    ("home", ["xxx"], pytest.raises(UserError, match="unknown argument")),
])
def test_do_look(place, args, context):
    do_jump(place)

    with context:
        do_look(*args)

@pytest.mark.parametrize("place, args, context", [
    ("home", [], does_not_raise()),
    ("home", ["xxx"], pytest.raises(UserError, match="unknown argument")),
])
def test_do_map(place, args, context):
    do_jump(place)

    with context:
        do_map(*args)

@pytest.mark.parametrize("args, context", [
    (["dragon"], pytest.raises(UserError, match="pet needs a color")),
    (["red"], does_not_raise()),
    (["red", "dragon"], does_not_raise()),
    (["red", "head"], does_not_raise()),
    (["dragon", "red"], does_not_raise()),
    (["dragon", "xxx"], pytest.raises(UserError, match="color invalid")),
    (["xxx", "dragon"], pytest.raises(UserError, match="color invalid")),
    (["dragon", "red", "xxx"], pytest.raises(UserError, match="unknown argument")),
    (["red", "monkey"], pytest.raises(UserError, match="color invalid")),
    ([], pytest.raises(UserError, match="pet needs a color")),
])
def test_do_pet(args, context):
    do_jump("cave")

    with context as ex:
        award, damage = do_pet(*args)

    if not ex:
        assert get_health() == 100 + damage
        assert get_inventory("gems") == award


@pytest.mark.parametrize("args", [
    ([]),
    (["xxx"]),
])
def test_do_quit(args):
    with pytest.raises(SystemExit):
        do_quit(*args)
