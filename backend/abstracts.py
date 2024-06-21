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
    id_attributes: list = None
    primary_attributes: list = None
    relation_attributes: list = None

    @abstractmethod
    def serialize(self):
        """This return serialized instance data"""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def deserialize(cls, **kwargs):
        """This returns deserialized class instance."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def deserialize_relations(cls):
        """This method deserializes the entity associations and return class instance."""
        raise NotImplementedError
    
    @abstractmethod
    def dump(self, obj: t.Any, file_path: str):
        """This method dumps the serialized entity to disk."""
        raise NotImplementedError

    @abstractmethod
    def dumps(self, **kwargs):
        """This method dumps the serialized entity to str."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def load(cls, file_path: str):
        """This method loads the serialized entity from disk."""
        raise NotImplementedError

    @abstractmethod
    def _encode(self) -> t.Dict[str, t.Any]:
        """This method encodes the entity."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def _decode(cls, data: t.Dict[str, t.Any], *args, **kwargs) -> t.Any:
        """This method decodes the entity."""
        raise NotImplementedError


class AbstractType(AbstractEntitySerializer, metaclass=EntityTrackerMeta):
    entity_type = EntityType.Type
    valid_types = tuple()
    default = None

    @abstractmethod
    def delete(self):
        """This deletes the entity."""
        raise NotImplementedError

    @abstractmethod
    def get_type(self, serialize=False):
        """This returns the type of the entity."""
        raise NotImplementedError

    @abstractmethod
    def get_class(self, serialize=False):
        """This returns the class of the entity."""
        raise NotImplementedError

    @abstractmethod
    def get_id(self, serialize=False):
        """This returns the id of the entity."""
        raise NotImplementedError

    @abstractmethod
    def data(self):
        """This returns the data of the type."""
        raise NotImplementedError

    @abstractmethod
    def get_data(self, serialize=False):
        """This returns the data of the type."""
        raise NotImplementedError

    @abstractmethod
    def set_data(self, data):
        """This sets the data of the type."""
        raise NotImplementedError

    @abstractmethod
    def del_data(self):
        """This deletes the data of the type."""
        raise NotImplementedError

    @abstractmethod
    def validate_data(self, data):
        """This validates the data of the type."""
        raise NotImplementedError


class AbstractNode(AbstractEntitySerializer, metaclass=EntityTrackerMeta):
    entity_type = EntityType.Node

    @abstractmethod
    def delete(self):
        """This deletes the entity."""
        raise NotImplementedError

    @abstractmethod
    def get_type(self, serialize=False):
        """This returns the type of the entity."""
        raise NotImplementedError

    @abstractmethod
    def get_class(self, serialize=False):
        """This returns the class of the entity."""
        raise NotImplementedError

    @abstractmethod
    def get_id(self, serialize=False):
        """This returns the id of the entity."""
        raise NotImplementedError

    @abstractmethod
    def data(self):
        """This returns the data of the node."""
        raise NotImplementedError
        