from abc import ABC, abstractmethod
from typing import Dict, Any

from core.base.attribute import *


class AbstractAttributeSerializer(ABC):
    """
    AbstractAttributeSerializer

    This abstract class serves as a base for attribute serializers. Attribute serializers are used to convert attribute objects to and from a serialized format.

    Methods:
        serialize: Converts an attribute object to a serialized format.
        deserialize: Converts a serialized attribute format to an attribute object.
    """
    @abstractmethod
    def serialize(self, attr: Attribute) -> Dict[str, Any]:
        raise NotImplementedError('must override this method')

    @abstractmethod
    def deserialize(self, attr_data: Dict[str, Any]) -> Attribute:
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
    def serialize(self, attr_collection: AttributeCollection) -> Dict[str, Any]:
        raise NotImplementedError('must override this method')

    @abstractmethod
    def deserialize(self, attr_data: Dict[str, Any]) -> AttributeCollection:
        raise NotImplementedError('must override this method')
