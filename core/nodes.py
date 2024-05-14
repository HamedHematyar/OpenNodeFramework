from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List


class AbstractAttribute(ABC):
    """
    An abstract class representing an attribute.

    Example:
    >>> attr = Attribute('attr', 'value')
    >>> attr.name
    'attr'
    >>> attr.value
    'value'
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Property that should return the name of the attribute.
        """
        raise NotImplementedError('must override this method')

    @property
    @abstractmethod
    def value(self) -> Any:
        """
        Property that should return the value of the attribute.
        """
        raise NotImplementedError('must override this method')


class Attribute(AbstractAttribute):
    """
    A concrete attribute class that implements 'name' and 'value' properties.
    """

    def __init__(self, name, value):
        """
        Initialize an attribute with a name and value.

        :param name: The name of the attribute.
        :param value: The value of the attribute.
        """
        self._name = None
        self._value = None

        self.name = name
        self.value = value

    @property
    def name(self) -> str:
        """
        Get the name of the attribute.

        :return: The name of the attribute.
        """
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        """
        Set a new name for the attribute.

        :param new_name: The new name for the attribute.
        """
        self._name = new_name

    @property
    def value(self) -> Any:
        """
        Get the value of the attribute.

        :return: The value of the attribute.
        """
        return self._value

    @value.setter
    def value(self, new_value: Any) -> None:
        """
        Set a new value for the attribute.

        :param new_value: The new value for the attribute.
        """
        self._value = new_value


class AbstractAttributesManager(list):
    """
    An abstract class representing a manager for a list of attributes.
    """

    def __init__(self) -> None:
        """
        Initialize an instance of AbstractAttributesManager.
        """
        super().__init__()

    @abstractmethod
    def serialize(self) -> Dict[str, Any]:
        """
        Method that should return a dictionary representation of the attributes managed by this instance.
        """
        raise NotImplementedError('must override this method')

    @abstractmethod
    def deserialize(self, attributes_data: Dict[str, Any]) -> None:
        """
        Method that should parse a dictionary representation of attributes and update this instance's attributes
        accordingly.

        :param attributes_data: A dictionary of attribute data, typically coming from a call to 'serialize'.
        """
        raise NotImplementedError('must override this method')


class AttributesManager(AbstractAttributesManager):
    """
    A concrete attributes manager class.
    """

    def append(self, attribute):
        """
        Append an attribute to the list of managed attributes. Raises a TypeError if the attribute is not an instance
        of AbstractAttribute.

        :param attribute: The attribute to add to the manager.
        """
        if not isinstance(attribute, AbstractAttribute):
            raise TypeError(f'attribute {attribute} is not an instance of {AbstractAttribute}')

        super().append(attribute)

    def serialize(self) -> Dict[str, Any]:
        """
        Return a dictionary representation of the attributes managed by this instance.

        :return: A dictionary where the keys are attribute names and the values are attribute values.
        """
        return {attribute.name: attribute.value for attribute in self}

    def deserialize(self, data: Dict[str, Any]) -> None:
        """
        Parse a dictionary representation of attributes and update this instance's attributes accordingly.

        :param data: A dictionary of attribute data.
        """
        self.clear()
        for data in data.items():
            self.append(Attribute(*data))


class AbstractNode(ABC):
    """
    An abstract class representing a node with managed attributes.
    """

    def __init__(self) -> None:
        """
        Initialize an instance of AbstractNode.
        """
        self.attributes: AttributesManager = AttributesManager()
