import typing as t
from backend.bases import BaseAttribute


class String(BaseAttribute):
    def __init__(self):
        super().__init__()

    def set_value(self, value):
        if not isinstance(value, str):
            raise TypeError(f'attribute value must be a str.')

        super().set_value(value)


class Integer(BaseAttribute):
    def __init__(self):
        super().__init__()

    def set_value(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f'attribute value must be a int.')

        super().set_value(value)


class List(BaseAttribute):
    def __init__(self):
        super().__init__()

    def set_value(self, value):
        if not isinstance(value, list):
            raise TypeError(f'attribute value must be a list.')

        super().set_value(value)


class Enumeration(BaseAttribute):
    def __init__(self):
        super().__init__()

        self._options: t.Optional[t.List[t.Any]] = None

    def initialize(self, name, options):
        super().initialize(name, options)

        self.set_options(options)
        self.set_value(options[0])

        return self

    def get_options(self):
        return self._options

    def set_options(self, options):
        if not isinstance(options, list):
            raise TypeError(f'options is not an instance of {list}.')

        if options:
            raise ValueError(f'no valid options are given : {options}')

        self._options = options


class TypeAttribute(BaseAttribute):
    def __init__(self):
        super().__init__()

    def set_value(self, value):
        if isinstance(value, str):
            value = eval(value)

        if value not in [str,
                         int,
                         list]:
            raise TypeError(f'attribute value is not valid.')

        super().set_value(value.__name__)
