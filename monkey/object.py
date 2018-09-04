from abc import abstractmethod
from dataclasses import dataclass
from typing import Any

INTEGER_OBJ = 'INTEGER'
BOOLEAN_OBJ = 'BOOLEAN'
NULL_OBJ = 'NULL'
RETURN_VALUE_OBJ = 'RETURN_VALUE'
ERROR_OBJ = 'ERROR'


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
