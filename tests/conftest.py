import pytest
from adventure.data.player import init

@pytest.fixture(autouse=True)
def setup():
    init()
