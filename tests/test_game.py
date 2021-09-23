from contextlib import nullcontext as does_not_raise

import pytest

from adventure import (SilentError, UserError)
from adventure.game import parse
from adventure.actions import do_jump
from adventure.inventory import adjust_inventory


@pytest.mark.parametrize("place, item, text, action, expected_args, context", [
    (None, None, "shop", None, [], pytest.raises(UserError, match="No such command")),
    (None, None, "", None, [], pytest.raises(SilentError)),
    (None, None, "help", "do_help", [], does_not_raise()),
    (None, None, "?", "do_help", [], does_not_raise()),
    (None, None, "east", "do_go", ["east"], does_not_raise()),
    ("market", None, "shop", "do_shop", [], does_not_raise()),
    (None, None, "drink", None, [], pytest.raises(UserError, match="No such command")),
    (None, None, "xxx", None, [], pytest.raises(UserError, match="No such command")),
    (None, "elixr", "drink elixr", "do_consume", ["elixr"], does_not_raise()),
])
def test_parse(place, item, text, action, expected_args, context):
    do_jump(place or "home")

    if item:
        adjust_inventory(item, 1)

    with context as ex:
        func, args = parse(text)

    if not ex:
        assert func.__name__ == action
        assert args == expected_args


