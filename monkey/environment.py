from dataclasses import dataclass
from typing import Any, Dict, Optional

from monkey import object


@dataclass
class Environment:
    store: Dict[str, object.Object]
    outer: Optional[Any]

    def Get(self, name: str) -> Optional[object.Object]:
        obj = self.store.get(name)
        if not obj and self.outer is not None:
            obj = self.outer.Get(name)
        return obj

    def Set(self, name: str, val: object.Object) -> object.Object:
        self.store[name] = val
        return val


def NewEnvironment() -> Environment:
    s: Dict[str, object.Object] = dict()
    return Environment(store=s, outer=None)


def NewEnclosedEnvironment(outer: Environment) -> Environment:
    env = NewEnvironment()
    env.outer = outer
    return env
