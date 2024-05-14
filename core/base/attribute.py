from core.abstract import attribute
from typing import Dict, Any


class Attribute(attribute.AbstractAttribute):
    """
    A concrete attribute class that implements 'name' and 'value' properties.
    """

    def __init__(self, name, value):
        """
        Initialize an attribute with a name and value.

        :param name: The name of the attribute.
        :param value: The value of the attribute.
        """
        self.__name = None
        self.__value = None

        self.name = name
        self.value = value

    @property
    def name(self) -> str:
        """
        Get the name of the attribute.

        :return: The name of the attribute.
        """
        return self.__name

    @name.setter
    def name(self, new_name: str) -> None:
        """
        Set a new name for the attribute.

        :param new_name: The new name for the attribute.
        """
        self.__name = new_name

    @property
    def value(self) -> Any:
        """
        Get the value of the attribute.

        :return: The value of the attribute.
        """
        return self.__value

    @value.setter
    def value(self, new_value: Any) -> None:
        """
        Set a new value for the attribute.

        :param new_value: The new value for the attribute.
        """
        self.__value = new_value


class AttributeCollection(attribute.AbstractAttributeCollection, list):
    """
    A concrete attribute manager class.
    """

    def __init__(self) -> None:
        """
        Initialize an instance of AbstractAttributesManager.
        """
        super().__init__()

    def append(self, attribute):
        """
        Append an attribute to the list of managed attribute. Raises a TypeError if the attribute is not an instance
        of AbstractAttribute.

        :param attribute: The attribute to add to the manager.
        """
        if not isinstance(attribute, attribute.AbstractAttribute):
            raise TypeError(f'attribute {attribute} is not an instance of {attribute.AbstractAttribute}')

        super().append(attribute)

    def serialize(self) -> Dict[str, Any]:
        """
        Return a dictionary representation of the attribute managed by this instance.

        :return: A dictionary where the keys are attribute names and the values are attribute values.
        """
        return {attribute.name: attribute.value for attribute in self}

    def deserialize(self, data: Dict[str, Any]) -> None:
        """
        Parse a dictionary representation of attribute and update this instance's attribute accordingly.

        :param data: A dictionary of attribute data.
        """
        self.clear()
        for name, value in data.items():
            self.append(Attribute(name, value))
