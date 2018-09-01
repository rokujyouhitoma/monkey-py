from abc import abstractmethod
from dataclasses import dataclass

INTEGER_OBJ = 'INTEGER'
BOOLEAN_OBJ = 'BOOLEAN'
NULL_OBJ = 'NULL'


@dataclass
class ObjectType:
    TypeName: str


class Object:
    @property
    @abstractmethod
    def Type(self) -> ObjectType:
        pass

    @property
    @abstractmethod
    def Inspect(self) -> str:
        pass


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
    @property
    def Type(self) -> ObjectType:
        return ObjectType(NULLy_OBJ)

    @property
    def Inspect(self) -> str:
        return NULL_OBJ
