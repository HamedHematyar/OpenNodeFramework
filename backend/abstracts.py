import enum
import typing as t

from abc import abstractmethod

from backend.meta import *


class EntityType(enum.StrEnum):
    GenericNode: str = 'GenericNode'
    NodeAttribute: str = 'NodeAttribute'
    PortNode: str = 'PortNode'
    Node: str = 'Node'
    Port: str = 'Port'
    Attribute: str = 'Attribute'
    Graph: str = 'Graph'
    DataType: str = 'Type'


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

    @abstractmethod
    def deserialize_relations(self):
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
    entity_type = EntityType.DataType
    valid_types = tuple()

    @property
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


class AbstractPort(AbstractEntityMixin, AbstractEntitySerializer, metaclass=EntityTrackerMeta):
    entity_type = EntityType.Port

    @property
    @abstractmethod
    def mode(self):
        """This should return the mode of the port."""

    @abstractmethod
    def get_mode(self, serialize=False):
        """This should return the mode of the port."""

    @abstractmethod
    def set_mode(self, _type):
        """This should set the mode of the port."""

    @abstractmethod
    def del_mode(self):
        """This deletes the mode of the port."""

    @abstractmethod
    def validate_mode(self, mode):
        """This validates the port mode"""

    @property
    @abstractmethod
    def connections(self):
        """This returns the connections of the port."""

    @abstractmethod
    def get_connections(self, serialize=False):
        """This returns the connections of the port."""

    @abstractmethod
    def set_connections(self, connections):
        """This sets the connections of the port."""

    @abstractmethod
    def del_connections(self):
        """This deletes the connections of the port."""

    @abstractmethod
    def validate_connections(self, connections):
        """This validates the connections of the port."""


class AbstractNode(AbstractEntityMixin, AbstractEntitySerializer, metaclass=EntityTrackerMeta):
    entity_type = EntityType.GenericNode

    @abstractmethod
    def data(self):
        """This returns the data of the node."""
