import enum
import typing as t

from abc import abstractmethod

from backend.meta import *


class EntityType(enum.StrEnum):
    Node: str = 'Node'
    Attribute: str = 'Attribute'
    Port: str = 'Port'
    Type: str = 'Type'


class AbstractEntitySerializer:
    id_attributes = list()
    primary_attributes = list()
    relation_attributes = list()

    @abstractmethod
    def serialize(self):
        """This return serialized instance data"""

    @classmethod
    @abstractmethod
    def deserialize(cls, **kwargs):
        """This returns deserialized class instance."""

    @classmethod
    @abstractmethod
    def deserialize_relations(cls):
        """This method deserializes the entity associations and return class instance."""
    
    @abstractmethod
    def dump(self, obj: t.Any, file_path: str):
        """This method dumps the serialized entity to disk."""

    @abstractmethod
    def dumps(self, **kwargs):
        """This method dumps the serialized entity to str."""

    @classmethod
    @abstractmethod
    def load(cls, file_path: str):
        """This method loads the serialized entity from disk."""

    @abstractmethod
    def _encode(self) -> t.Dict[str, t.Any]:
        """This method encodes the entity."""

    @classmethod
    @abstractmethod
    def _decode(cls, data: t.Dict[str, t.Any], *args, **kwargs) -> t.Any:
        """This method decodes the entity."""


class AbstractEntityMixin:

    @abstractmethod
    def delete(self):
        """This deletes the entity."""

    @abstractmethod
    def get_type(self, serialize=False):
        """This returns the type of the entity."""

    @abstractmethod
    def get_class(self, serialize=False):
        """This returns the class of the entity."""

    @abstractmethod
    def get_id(self, serialize=False):
        """This returns the id of the entity."""


class AbstractType(AbstractEntityMixin, AbstractEntitySerializer, metaclass=EntityTrackerMeta):
    entity_type = EntityType.Type
    valid_types = tuple()
    default = None

    @abstractmethod
    def data(self):
        """This returns the data of the type."""

    def get_data(self, serialize=False):
        """This returns the data of the type."""

    def set_data(self, data):
        """This sets the data of the type."""

    def del_data(self):
        """This deletes the data of the type."""

    def validate_data(self, data):
        """This validates the data of the type."""


class AbstractNode(AbstractEntityMixin, AbstractEntitySerializer, metaclass=EntityTrackerMeta):
    entity_type = EntityType.Node

    @abstractmethod
    def data(self):
        """This returns the data of the node."""
        