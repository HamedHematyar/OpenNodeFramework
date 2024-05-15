from core.base.attribute import *


class StringAttribute(Attribute):
    """
    >>> StringAttribute(name="test_name", value='test_value')
    {'name': 'test_name', 'value': 'test_value'}

    >>> StringAttribute(value=None)
    Traceback (most recent call last):
    ...
    TypeError: attribute value must be a string.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def value_validator(key, value):
        if not isinstance(value, str):
            raise TypeError(f'attribute {key} must be a string.')


class NameAttribute(StringAttribute):
    """
    >>> NameAttribute(value='test')
    {'name': 'name', 'value': 'test'}
    """
    def __init__(self, **kwargs):
        super().__init__(**{'name': 'name', **kwargs})
