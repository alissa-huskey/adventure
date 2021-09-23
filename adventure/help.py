from adventure.places import COMPASS
from adventure.data.help import COMMANDS, TOPICS

def get_help(command):
    """Return the help dict for a given command or alias"""
    return TOPICS.get(command)
