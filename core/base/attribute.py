import typing
from collections.abc import MutableMapping

from core.abstract.attribute import *


def dict_item_validator_wrapper(func):
    """
    :param func: the function to be wrapped
    :return: the wrapped function

    This method calls a validator method corresponding to the provided key.

    """
    def wrapper(self, key, value):
        validation_method = getattr(self, f"{key}_validator", lambda *args: None)
        validation_method(key, value)

        func(self, key, value)

    return wrapper


class Attribute(AbstractAttribute):
    """
    A concrete attribute class that implements AbstractAttribute.
    """

    def __init__(self, name, value):
        self._name: typing.Optional = None
        self.set_name(name)

        self._value: typing.Optional = None
        self.set_value(value)

    def __str__(self):
        return str(self.get_value())

    def __repr__(self):
        return f'{self.get_name()} : {self.get_value()}'

    def set_name(self, name) -> bool:
        if not isinstance(name, str):
            raise TypeError(f'attribute name must be a string.')

        self._name = name
        return True

    def get_name(self):
        return self._name

    def set_value(self, value) -> bool:
        self._value = value

        return True

    def get_value(self) -> typing.Any:
        return self._value


class AttributeCollection(MutableMapping):
    def __init__(self, **kwargs):
        self._data = {}

        self.update(**kwargs)

    def __setitem__(self, key: str, value: Attribute):
        if not isinstance(value, Attribute):
            raise TypeError(f'attribute {value} is not an instance of {Attribute}')

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

    def update(self, **kwargs):
        for key, value in kwargs.items():
            self.__setitem__(key, value)

    def add(self, attribute: Attribute):
        self.update(**{attribute.get_name(): attribute})
