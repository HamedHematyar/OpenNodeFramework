from collections.abc import MutableMapping, MutableSequence

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
            raise TypeError(f'attribute {key} must be a string.')


class AttributeCollection(attribute.AbstractAttributeCollection, MutableSequence):
    def __init__(self, attributes: list):
        self._data = list(*attributes)

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        self._data[index] = value

    def __delitem__(self, index):
        del self._data[index]

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return repr(self._data)

    def insert(self, index, value):
        if not isinstance(value, attribute.AbstractAttribute):
            raise TypeError(f'attribute {value} is not an instance of {attribute.AbstractAttribute}')

        self._data.insert(index, value)

    def append(self, value):
        if not isinstance(value, attribute.AbstractAttribute):
            raise TypeError(f'attribute {value} is not an instance of {attribute.AbstractAttribute}')

        self._data.append(value)
