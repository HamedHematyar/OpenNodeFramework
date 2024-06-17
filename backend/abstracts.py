import enum
import typing as t

from abc import abstractmethod

from backend.enums import PortType
from backend.meta import *


class EntityType(enum.StrEnum):
    Node: str = enum.auto()
    Port: str = enum.auto()
    Attribute: str = enum.auto()
    Graph: str = enum.auto()


class SerializableMixin:
    @classmethod
    @abstractmethod
    def serializer(cls):
        """This returns class serializer instance."""

    @abstractmethod
    def serialize(self):
        """This return serialized instance data"""

    @classmethod
    @abstractmethod
    def deserialize(cls, **kwargs):
        """This returns deserialized class instance."""


class AbstractEntityMixin:

    def __del__(self):
        """This method is called when this class is deleted."""

    @abstractmethod
    def get_type(self):
        """This returns the type of the entity."""

    @abstractmethod
    def get_id(self) -> str:
        """This returns the id of the entity."""

    @abstractmethod
    def get_name(self) -> str:
        """This returns the name of the entity."""

    @abstractmethod
    def set_name(self, name: str) -> bool:
        """This sets the name of the entity."""

    @abstractmethod
    def del_name(self):
        """This deletes the name of the entity."""

    @abstractmethod
    def get_parent(self):
        """This returns the parent node."""

    @abstractmethod
    def set_parent(self, parent) -> bool:
        """This sets the parent node."""

    @abstractmethod
    def del_parent(self):
        """This deletes the parent node."""


class AbstractAttribute(AbstractEntityMixin, SerializableMixin, metaclass=EntityTrackerMeta):
    entity_type = EntityType.Attribute
    valid_types = tuple()

    @abstractmethod
    def get_link(self) -> 'AbstractAttribute':
        """This returns the linked attribute."""

    @abstractmethod
    def set_link(self, link: 'AbstractAttribute') -> bool:
        """This sets the linked attribute."""

    @abstractmethod
    def del_link(self):
        """This deletes the linked attribute."""

    @abstractmethod
    def get_value(self) -> t.Any:
        """This returns the value of the attribute."""

    @abstractmethod
    def set_value(self, value: t.Any) -> bool:
        """This sets the value of the attribute."""

    @abstractmethod
    def del_value(self):
        """This deletes the value of the attribute."""


class AbstractPort(AbstractEntityMixin, SerializableMixin, metaclass=EntityTrackerMeta):
    entity_type = EntityType.Port

    @abstractmethod
    def get_mode(self) -> t.Optional[PortType]:
        """This should return the mode of the port."""

    @abstractmethod
    def set_mode(self, _type: PortType):
        """This should set the mode of the port."""

    def del_mode(self):
        """This deletes the mode of the port."""


class AbstractNode(AbstractEntityMixin, SerializableMixin, metaclass=EntityTrackerMeta):
    entity_type = EntityType.Node

    @abstractmethod
    def data(self) -> t.Optional[t.Any]:
        """This method computes the node data"""


class AbstractGraph(AbstractEntityMixin, SerializableMixin, metaclass=EntityTrackerMeta):
    entity_type = EntityType.Graph
