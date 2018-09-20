import hashlib
from abc import abstractmethod
from dataclasses import dataclass
from functools import singledispatch
from typing import Any, Callable, Dict, List, Optional, Tuple

from monkey import ast

INTEGER_OBJ = 'INTEGER'
BOOLEAN_OBJ = 'BOOLEAN'
NULL_OBJ = 'NULL'
RETURN_VALUE_OBJ = 'RETURN_VALUE'
ERROR_OBJ = 'ERROR'
FUNCTION_OBJ = 'FUNCTION'
STRING_OBJ = 'STRING'
BUILTIN_OBJ = 'BUILTIN'
ARRAY_OBJ = 'ARRAY'
HASH_OBJ = 'HASH'


@dataclass
class ObjectType:
    TypeName: str


class Object:
    Value: Any

    @property
    @abstractmethod
    def Type(self) -> ObjectType:
        pass

    @property
    @abstractmethod
    def Inspect(self) -> str:
        pass


@dataclass
class AnyObject(Object):
    Value: Object

    @property
    def Type(self) -> ObjectType:
        return self.Value.Type

    @property
    def Inspect(self) -> str:
        return self.Value.Inspect


@dataclass
class Integer(Object):
    Value: int

    @property
    def Type(self) -> ObjectType:
        return ObjectType(INTEGER_OBJ)

    @property
    def Inspect(self) -> str:
        return str(self.Value)


@dataclass
class Boolean(Object):
    Value: bool

    @property
    def Type(self) -> ObjectType:
        return ObjectType(BOOLEAN_OBJ)

    @property
    def Inspect(self) -> str:
        return str(self.Value)


@dataclass
class Null(Object):
    Value: Any = None

    @property
    def Type(self) -> ObjectType:
        return ObjectType(NULL_OBJ)

    @property
    def Inspect(self) -> str:
        return NULL_OBJ


@dataclass
class ReturnValue(Object):
    Value: Object

    @property
    def Type(self) -> ObjectType:
        return ObjectType(RETURN_VALUE_OBJ)

    @property
    def Inspect(self) -> str:
        return self.Value.Inspect


@dataclass
class Error(Object):
    Message: str

    @property
    def Type(self) -> ObjectType:
        return ObjectType(ERROR_OBJ)

    @property
    def Inspect(self) -> str:
        return 'ERROR: ' + self.Message


@dataclass
class Function(Object):
    Parameters: List[ast.Identifier]
    Body: ast.BlockStatement
    Env: Any

    @property
    def Type(self) -> ObjectType:
        return ObjectType(FUNCTION_OBJ)

    @property
    def Inspect(self) -> str:
        out: List[str] = []

        params: List[str] = []
        for p in self.Parameters:
            params.append(p.String())

        out.append('fn')
        out.append('(')
        out.append(', '.join(params))
        out.append(') {\n')
        out.append(self.Body.String())
        out.append('\n}')

        return ''.join(out)


@dataclass
class String(Object):
    Value: str

    @property
    def Type(self) -> ObjectType:
        return ObjectType(STRING_OBJ)

    @property
    def Inspect(self) -> str:
        return self.Value


@dataclass
class Array(Object):
    Elements: List[Object]

    @property
    def Type(self) -> ObjectType:
        return ObjectType(ARRAY_OBJ)

    @property
    def Inspect(self) -> str:
        out: List[str] = []

        elements: List[str] = []
        for e in self.Elements:
            elements.append(e.Inspect)

        out.append('[')
        out.append(', '.join(elements))
        out.append(']')

        return ''.join(out)


@dataclass
class HashKey():
    Type: ObjectType
    Value: int


@singledispatch
def GetHashKey(arg: Any) -> Any:
    return None


@GetHashKey.register(Boolean)
def GetHashKeyBoolean(b: Boolean) -> HashKey:
    value = 1 if b.Value else 0
    return HashKey(Type=b.Type, Value=value)


@GetHashKey.register(Integer)
def GetHashKeyInteger(i: Integer) -> HashKey:
    return HashKey(Type=i.Type, Value=int(i.Value))


@GetHashKey.register(String)
def GetHashKeyString(s: String) -> HashKey:
    m = hashlib.sha256()
    m.update(s.Value.encode())
    digest = int(m.hexdigest(), 16)
    return HashKey(Type=s.Type, Value=digest)


@dataclass
class HashPair():
    Key: Object
    Value: Object


@dataclass
class Hash(Object):
    Pairs: List[Tuple[HashKey, HashPair]]

    @property
    def Type(self) -> ObjectType:
        return ObjectType(HASH_OBJ)

    @property
    def Inspect(self) -> str:
        out: List[str] = []

        pairs: List[str] = []
        for key, pair in self.Pairs:
            pairs.append('%s: %s' % (pair.Key.Inspect, pair.Value.Inspect))

        out.append('{')
        out.append(', '.join(pairs))
        out.append('}')

        return ''.join(out)


def GetHashPair(hash: Hash, key: HashKey) -> Optional[HashPair]:
    pairs: List[Tuple[HashKey, HashPair]] = hash.Pairs

    if not key:
        return None

    # TODO: It's is O(n)
    list = [x for x in pairs if x[0].Value == key.Value]
    if len(list) == 0:
        return None

    hashKey, hashPair = list[0]
    return hashPair


BuiltinFunction = Callable[[List[Object]], Object]


@dataclass
class Builtin(Object):
    Fn: Any

    @property
    def Type(self) -> ObjectType:
        return ObjectType(BUILTIN_OBJ)

    @property
    def Inspect(self) -> str:
        return 'builtin function'


@dataclass
class Environment:
    store: Dict[str, Object]
    outer: Optional[Any]

    def Get(self, name: str) -> Optional[Object]:
        obj = self.store.get(name)
        if not obj and self.outer is not None:
            obj = self.outer.Get(name)
        return obj

    def Set(self, name: str, val: Object) -> Object:
        self.store[name] = val
        return val


def NewEnvironment() -> Environment:
    s: Dict[str, Object] = dict()
    return Environment(store=s, outer=None)


def NewEnclosedEnvironment(outer: Environment) -> Environment:
    env = NewEnvironment()
    env.outer = outer
    return env
