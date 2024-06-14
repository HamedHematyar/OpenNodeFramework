import typing as t
import enum
from backend.bases import BaseAttribute


class GenericStr(BaseAttribute):
    valid_types = (str, )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GenericInt(BaseAttribute):
    valid_types = (int, float)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GenericList(BaseAttribute):
    valid_types = (list, tuple, set)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GenericEnum(BaseAttribute):
    valid_types = (enum.Enum, )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._options: t.Optional[t.List[t.Any]] = []

        'options' in kwargs and self.set_options(kwargs.get('options'))

    def get_options(self):
        return self._options

    def set_options(self, options):
        if not issubclass(options, enum.Enum):
            raise TypeError(f'options is not a subclass of {enum.Enum}.')

        self._options = options

    def del_options(self):
        self._options.clear()


class DataTypeEnum(GenericEnum):
    class DataType(enum.Enum):
        Str = str
        Int = int
        Float = float
        Bool = bool

    def __init__(self, **kwargs):
        kwargs['options'] = self.DataType

        super().__init__(**kwargs)
