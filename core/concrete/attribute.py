from core.base import attribute


class NameAttribute(attribute.Attribute):
    """
    This is a test class for NameAttribute.

    >>> NameAttribute(value='test')
    {'name': 'name', 'value': 'test'}

    >>> NameAttribute(value=None)
    Traceback (most recent call last):
    ...
    TypeError: Attribute value must be a string.
    """
    def __init__(self, **kwargs):
        data = {'name': 'name'}
        data.update(**kwargs)

        super().__init__(**data)

    @staticmethod
    def value_validator(key, value):
        if not isinstance(value, str):
            raise TypeError(f'Attribute {key} must be a string.')

