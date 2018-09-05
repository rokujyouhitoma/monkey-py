from dataclasses import dataclass
from typing import Dict, Optional

from monkey import object


@dataclass
class Environment:
    store: Dict[str, object.Object]

    def Get(self, name: str) -> Optional[object.Object]:
        return self.store.get(name)

    def Set(self, name: str, val: object.Object) -> object.Object:
        self.store[name] = val
        return val


def NewEnvironment() -> Environment:
    s: Dict[str, object.Object] = dict()
    return Environment(store=s)
