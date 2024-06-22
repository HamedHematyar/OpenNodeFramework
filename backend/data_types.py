import typing as t
import enum

from backend.logger import logger
from backend.bases import BaseType, BaseNode, BaseAttributeNode


class GenericStr(BaseType):
    valid_types = (str, )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GenericInt(BaseType):
    valid_types = (int, float)
    default = int()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_data(self, data):
        if isinstance(data, float):
            data = int(data)

        return super().set_data(data)


class GenericFloat(BaseType):
    valid_types = (int, float)
    default = float()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_data(self, data):
        if isinstance(data, int):
            data = float(data)

        return super().set_data(data)


class GenericList(BaseType):
    valid_types = (list, tuple, set)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GenericEnum(BaseType):
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


class PortModeEnum(GenericEnum):
    class PortType(enum.StrEnum):
        INPUT = 'INPUT'
        OUTPUT = 'OUTPUT'

    default = PortType.INPUT

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_data(self, data):
        if isinstance(data, str):
            data = getattr(self.PortType, data, None)

        return super().set_data(data)


class ReferencedNodeAttribute(GenericStr):
    valid_types = (BaseAttributeNode,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_data(self, data):
        if isinstance(data, BaseAttributeNode):
            self._data = data.get_id()
            return True

        return super().set_data(data)

    @classmethod
    def _decode(cls, data: t.Dict[str, t.Any], *args, **kwargs) -> t.Any:
        from backend.meta import InstanceManager
        instance = InstanceManager().get_instance(data['id'])
        if instance:
            return instance

        # TODO ReferenceManager task
        reference_id = data.pop('data', None)
        reference_instance = InstanceManager().get_instance(reference_id)
        if reference_instance:
            data['data'] = reference_instance

        if reference_id and not reference_instance:
            logger.warning(f'could not find reference to : {reference_id}')

        return cls(**data)


class ReferencedNodeType(BaseType):
    valid_types = (BaseNode,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_data(self, data):
        if isinstance(data, BaseNode):
            self._data = data.get_id()
            return True

        return super().set_data(data)