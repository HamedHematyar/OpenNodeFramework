import typing
from collections.abc import MutableMapping


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


class Attribute(MutableMapping):
    """
    A concrete attribute class that implements AbstractAttribute and MutableMapping.
    """

    def __init__(self, **kwargs):
        self._data = {}

        for key, value in kwargs.items():
            self.__setitem__(key, value)

    def __str__(self):
        return str(f"[{self.__class__.__name__} {id(self)}] {str(self._data)}")

    @dict_item_validator_wrapper
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

    def update_from_attribute(self, attribute: Attribute):
        self.update(**{attribute['name']: attribute})

    def update_from_attributes(self, attributes: typing.List[Attribute]):
        for attr in attributes:
            self.update_from_attribute(attr)
