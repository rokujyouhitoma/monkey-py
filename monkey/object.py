from abc import abstractmethod
from dataclasses import dataclass

INTEGER_OBJ = 'INTEGER'
BOOLEAN_OBJ = 'BOOLEAN'
NULL_OBJ = 'NULL'


@dataclass
class ObjectType:
    TypeName: str


class ObjectInterface:
    @property
    @abstractmethod
    def Type(self) -> ObjectType:
        pass

    @property
    @abstractmethod
    def Inspect(self) -> str:
        pass


@dataclass
class Object(ObjectInterface):
    Type: ObjectType
    Inspect: str


@dataclass
class Integer(ObjectInterface):
    Value: int

    @property
    def Type(self) -> ObjectType:
        return ObjectType(INTEGER_OBJ)

    @property
    def Inspect(self) -> str:
        return str(self.Value)


@dataclass
class Boolean(ObjectInterface):
    Value: bool

    @property
    def Type(self) -> ObjectType:
        return ObjectType(BOOLEAN_OBJ)

    @property
    def Inspect(self) -> str:
        return str(self.Value)


@dataclass
class Null(ObjectInterface):
    @property
    def Type(self) -> ObjectType:
        return ObjectType(NULL_OBJ)

    @property
    def Inspect(self) -> str:
        return NULL_OBJ
