from .places import COMPASS
from .data.help import COMMANDS, TOPICS

def get_help(command):
    """Return the help dict for a given command or alias"""
    return TOPICS.get(command)
