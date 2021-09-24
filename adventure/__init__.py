"""Package containing all text-based adventure game modules."""

from adventure.player import state

class SilentError(Exception): ...
class NotFound(Exception): ...

class Error(Exception):
    def __init__(self, *args, **kwargs):
        self.cmd = kwargs.pop("cmd", None) or state().get("action")
        self.message = " ".join(args)

    def text(self):
        return self.message

class UnexpectedError(Error):
    @property
    def text(self):
        text = super().text()

        return f"Something went wrong: {text}"

class UserError(Error): ...
