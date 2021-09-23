import pytest

from adventure.places import goto, get_place
from adventure.actions import contextual_action
from adventure.inventory import adjust_inventory
from adventure import NotFound, UserError

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
    goto(get_place(place)["position"])

    func, args = contextual_action(action, in_args, local=True)

    assert func.__name__ == func_name, f"{message}: {action}, {in_args}"
    assert args == out_args

@pytest.mark.parametrize("place,action,in_args,klass", [
    ("market", "xxx", [], NotFound),
    ("market", "buy", [], UserError),
    ("market", "buy", ["xxx"], UserError),
])
def test_contextual_action_local_raises(place, action, in_args, klass):
    goto(get_place(place)["position"])

    with pytest.raises(klass):
        func, args = contextual_action(action, in_args, local=True)

