from typing import Callable
from re import match, I
import dataclasses as dc


@dc.dataclass(frozen=True)
class Command:
    """command class"""

    name: str
    expr: str
    doc: str
    callback: Callable


@dc.dataclass(frozen=True)
class Bot:
    name: str
    commands: dict = dc.field(default_factory=dict)

    def on(self, expr, name=None, doc=None):
        def decorator(fn):
            nonlocal name
            nonlocal doc
            if name is None:
                name = expr
            if doc is None:
                doc = fn.__doc__ or expr
            cmnd = Command(name, expr, doc, fn)
            self.commands[name] = cmnd
            return fn
        return decorator

    def dispatch_message(self, msg, auth):
        """checks if a message is indeed a command"""

        for cmnd in self.commands.values():
            m = match(cmnd.expr, msg, I)
            if m:
                cmnd.callback(self, m, auth)
                return True
        return False
