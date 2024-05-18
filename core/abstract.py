import typing as t

from abc import ABC, abstractmethod
from collections.abc import MutableMapping

from core.enums import PortType


class AbstractAttribute(ABC):
    """
    An abstract class representing a node attribute.
    """

    @abstractmethod
    def __init__(self, name: str, value: t.Any):
        """This initializes the attribute."""

    @property
    @abstractmethod
    def name(self) -> str:
        """This returns the name of the attribute."""

    @name.setter
    @abstractmethod
    def name(self, name: str):
        """This sets the name of the attribute."""

    @property
    @abstractmethod
    def value(self) -> t.Any:
        """This returns the value of the attribute."""

    @value.setter
    @abstractmethod
    def value(self, value: t.Any):
        """This sets the value of the attribute."""


class AttributeCollection(MutableMapping):

    @abstractmethod
    def __setitem__(self, key: str, value: AbstractAttribute):
        raise NotImplementedError('this method is not implemented in subclass.')

    @abstractmethod
    def __getitem__(self, key):
        raise NotImplementedError('this method is not implemented in subclass.')

    @abstractmethod
    def __delitem__(self, key):
        raise NotImplementedError('this method is not implemented in subclass.')

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError('this method is not implemented in subclass.')

    @abstractmethod
    def __len__(self):
        raise NotImplementedError('this method is not implemented in subclass.')

    @abstractmethod
    def __repr__(self):
        raise NotImplementedError('this method is not implemented in subclass.')

    @abstractmethod
    def update(self, **kwargs):
        raise NotImplementedError('this method is not implemented in subclass.')


class AbstractNode(ABC):
    """
    An abstract class representing a node with managed attribute.
    """

    @abstractmethod
    def compute_data(self) -> t.Optional[t.Any]:
        """This method computes the node data"""

    @abstractmethod
    def compute_output(self, output_port: 'AbstractPort') -> t.Optional[t.Any]:
        """This method computes the node output"""


class AbstractNodeSerializer(ABC):
    """
    This abstract class represents a node serializer.
    """
    @abstractmethod
    def serialize(self, attr: AbstractNode) -> t.Dict[str, t.Any]:
        raise NotImplementedError('this method is not implemented in subclass.')

    @abstractmethod
    def deserialize(self, attr_data: t.Dict[str, t.Any]) -> AbstractNode:
        raise NotImplementedError('this method is not implemented in subclass.')


class AbstractPort(ABC):
    """
    An abstract class representing a node port.
    """

    @abstractmethod
    def __init__(self, name: str, port_type: PortType, node: 'AbstractNode'):
        """This initializes the port."""

    @property
    @abstractmethod
    def name(self) -> str:
        """This should return the name of the port."""
    @name.setter
    @abstractmethod
    def name(self, name: str):
        """This should set the name of the port."""

    @property
    @abstractmethod
    def port_type(self) -> t.Optional[PortType]:
        """This should return the type of the port."""

    @port_type.setter
    @abstractmethod
    def port_type(self, _type: PortType):
        """This should set the type of the port."""

    @property
    @abstractmethod
    def node(self) -> t.Optional[AbstractNode]:
        """This should return the node of the port."""

    @node.setter
    @abstractmethod
    def node(self, node: AbstractNode):
        """This should set the node of the port."""


class AbstractConnection(ABC):

    @abstractmethod
    def __init__(self, source: AbstractPort, destination: AbstractNode):
        """This should initialize the connection."""

    @property
    @abstractmethod
    def source(self) -> AbstractPort:
        """This should return the source port of the connection."""
    @source.setter
    @abstractmethod
    def source(self, name: AbstractPort):
        """This should set the source port of the connection."""

    @property
    @abstractmethod
    def destination(self) -> AbstractPort:
        """This should return the destination port of the connection."""

    @destination.setter
    @abstractmethod
    def destination(self, name: AbstractPort):
        """This should set the destination port of the connection."""

    @abstractmethod
    def __del__(self):
        """This should delete the connection and links to all connected ports."""


class AbstractAttributeSerializer(ABC):
    """
    AbstractAttributeSerializer

    This abstract class serves as a base for attribute serializers. Attribute serializers are used to convert attribute objects to and from a serialized format.

    Methods:
        serialize: Converts an attribute object to a serialized format.
        deserialize: Converts a serialized attribute format to an attribute object.
    """
    @abstractmethod
    def serialize(self, attr: AbstractAttribute) -> t.Dict[str, t.Any]:
        raise NotImplementedError('this method is not implemented in subclass.')

    @abstractmethod
    def deserialize(self, attr_data: t.Dict[str, t.Any]) -> AbstractAttribute:
        raise NotImplementedError('this method is not implemented in subclass.')


class AbstractAttributeCollectionSerializer(ABC):
    """
    AbstractAttributeCollectionSerializer

    This class is an abstract base class that defines the interface for serializing and deserializing attribute
    collections.

    Methods: - serialize(attr_collection: attribute.AbstractAttributeCollection) -> Dict[str, Any] This method takes
    an instance of attribute.AbstractAttributeCollection as input and returns a dictionary containing the serialized
    data.

    - deserialize(attr_data: Dict[str, Any]) -> attribute.AbstractAttributeCollection This method takes a dictionary
    containing the serialized data as input and returns an instance of attribute.AbstractAttributeCollection.

    Note:
    - All methods in this class are abstract and must be implemented by the subclasses.
    - The serialize method should raise a NotImplementedError if not overridden.
    - The deserialize method should raise a NotImplementedError if not overridden.

    """
    @abstractmethod
    def serialize(self, attr_collection: AttributeCollection) -> t.Dict[str, t.Any]:
        raise NotImplementedError('this method is not implemented in subclass.')

    @abstractmethod
    def deserialize(self, attr_data: t.Dict[str, t.Any]) -> AttributeCollection:
        raise NotImplementedError('this method is not implemented in subclass.')


class AbstractGraph(ABC):
    """This class defines the interface for a node graph."""

    @abstractmethod
    def __init__(self, name: str):
        """This initializes the graph."""

    @property
    @abstractmethod
    def name(self) -> str:
        """This returns the name of the graph."""

    @name.setter
    @abstractmethod
    def name(self, name: str):
        """This sets the name of the graph."""


class AbstractGraphSerializer(ABC):
    """This class defines the interface for a node graph serializer which helps with serializing and deserializing
    node graphs."""

    @abstractmethod
    def serialize(self, attr: AbstractGraph) -> t.Dict[str, t.Any]:
        raise NotImplementedError('this method is not implemented in subclass.')

    @abstractmethod
    def deserialize(self, attr_data: t.Dict[str, t.Any]) -> AbstractGraph:
        raise NotImplementedError('this method is not implemented in subclass.')

