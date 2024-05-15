from collections.abc import MutableMapping

from core.abstract import attribute


def integrate_validator(func):
    """
    :param func: the function to be wrapped
    :return: the wrapped function

    This method takes a function as a parameter and returns a wrapped function. The wrapped function executes the
    given function, but before doing so, it calls a validator method corresponding to the provided key. If the
    validator method exists, it is called with the key and value parameters. If the validator method does not exist,
    a default lambda function is called instead. Finally, the given function is executed with the key and value
    parameters.

    """
    def wrapper(self, key, value):
        getattr(self, f"{key}_validator", lambda *args: None)(key, value)
        func(self, key, value)

    return wrapper


class Attribute(attribute.AbstractAttribute, MutableMapping):
    """
    A concrete attribute class that implements AbstractAttribute and MutableMapping.
    """

    def __init__(self, **kwargs):
        self._data = {}

        for key, value in kwargs.items():
            self.__setitem__(key, value)

    @integrate_validator
    def __setitem__(self, key, value):
        self._data[key] = value

    def __getitem__(self, key):
        return self._data[key]

    def __delitem__(self, key):
        del self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return repr(self._data)

    @staticmethod
    def name_validator(key, value):
        if not isinstance(value, str):
            raise TypeError(f'Attribute {key} must be a string.')


class AttributeCollection(attribute.AbstractAttributeCollection, list):
    """
    A concrete attribute manager class.
    """

    def __init__(self) -> None:
        """
        Initialize an instance of AbstractAttributeCollection.
        """
        super().__init__()

    def append(self, attr):
        """
        Append an attribute to the list of managed attribute. Raises a TypeError if the attribute is not an instance
        of AbstractAttribute.

        :param attr: The attribute to add to the manager.
        """
        if not isinstance(attr, attribute.AbstractAttribute):
            raise TypeError(f'attribute {attr} is not an instance of {attribute.AbstractAttribute}')

        super().append(attr)

