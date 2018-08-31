from abc import abstractmethod
from dataclasses import dataclass


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
