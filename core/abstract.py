import typing as t
from abc import ABC, abstractmethod
from collections.abc import MutableMapping


class AbstractAttribute(ABC):
    """
    An abstract class representing a node attribute.
    """
    @abstractmethod
    def set_name(self, name: str) -> bool:
        """This method set the name of the attribute """

    @abstractmethod
    def get_name(self) -> str:
        """This method return the name of the attribute"""

    @abstractmethod
    def set_value(self, value: t.Any) -> bool:
        """This method set the value of the attribute """

    @abstractmethod
    def get_value(self) -> t.Any:
        """This method return the value of the attribute"""


class AttributeCollection(MutableMapping):

    @abstractmethod
    def __setitem__(self, key: str, value: AbstractAttribute):
        raise NotImplementedError('must override this method')

    @abstractmethod
    def __getitem__(self, key):
        raise NotImplementedError('must override this method')

    @abstractmethod
    def __delitem__(self, key):
        raise NotImplementedError('must override this method')

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError('must override this method')

    @abstractmethod
    def __len__(self):
        raise NotImplementedError('must override this method')

    @abstractmethod
    def __repr__(self):
        raise NotImplementedError('must override this method')

    @abstractmethod
    def update(self, **kwargs):
        raise NotImplementedError('must override this method')


class AbstractNode(ABC):
    """
    An abstract class representing a node with managed attribute.
    """


class AbstractPort(ABC):
    """
    An abstract class representing a node port.
    """

    @abstractmethod
    def get_name(self) -> str:
        """This should return the name of the port."""

    def set_name(self, name: str) -> bool:
        """This should set the name of the port."""

    @abstractmethod
    def get_node(self) -> AbstractNode:
        """This should return the node of the port."""

    @abstractmethod
    def set_node(self, node: AbstractNode) -> bool:
        """This should set the node of the port."""

    @abstractmethod
    def get_valid_types(self) -> t.List[AbstractNode]:
        """This should return a list of valid connection types."""


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
        raise NotImplementedError('must override this method')

    @abstractmethod
    def deserialize(self, attr_data: t.Dict[str, t.Any]) -> AbstractAttribute:
        raise NotImplementedError('must override this method')


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
        raise NotImplementedError('must override this method')

    @abstractmethod
    def deserialize(self, attr_data: t.Dict[str, t.Any]) -> AttributeCollection:
        raise NotImplementedError('must override this method')
