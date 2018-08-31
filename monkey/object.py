from abc import abstractmethod
from dataclasses import dataclass

INTEGER_OBJ = "INTEGER"


@dataclass
class ObjectType:
    TypeName: str


class ObjectInterface:
    @abstractmethod
    @property
    def Type(self) -> ObjectType:
        pass

    @abstractmethod
    @property
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
