import typing as t
import enum

from backend.logger import logger
from backend.registry import register_data_type
from backend.bases import BaseType, BasePortNode, BaseAttributeNode, BaseNode


@register_data_type
class GenericStr(BaseType):
    valid_types = (str, )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@register_data_type
class GenericInt(BaseType):
    valid_types = (int, float)
    default = int()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_data(self, data):
        if isinstance(data, float):
            data = int(data)

        return super().set_data(data)


@register_data_type
class GenericFloat(BaseType):
    valid_types = (int, float)
    default = float()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_data(self, data):
        if isinstance(data, int):
            data = float(data)

        return super().set_data(data)


@register_data_type
class GenericList(BaseType):
    valid_types = ()
    default = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate_data(self, data):
        for sub_data in data:
            if not isinstance(sub_data, self.valid_types):
                logger.warning(f'{self.__class__} attribute value must be an instance of '
                               f'{self.valid_types} not {type(sub_data)}.')
                return False

        return True


@register_data_type
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


@register_data_type
class DataTypeEnum(GenericEnum):
    class DataType(enum.Enum):
        Str = str
        Int = int
        Float = float
        Bool = bool

    def __init__(self, **kwargs):
        kwargs['options'] = self.DataType

        super().__init__(**kwargs)


@register_data_type
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


class GenericReferencedType(GenericStr):
    valid_types = tuple()
    reference_type = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_data(self, data):
        if isinstance(data, self.reference_type):
            self._data = data.get_id()
            return True

        return super().set_data(data)

    @classmethod
    def _decode(cls, data: t.Dict[str, t.Any]) -> t.Any:
        from backend.meta import ReferenceManager
        instance = ReferenceManager().request_instant_reference(data['id'])
        if instance:
            return instance

        reference_id = data.pop('data', None)
        instance = cls(**data)

        ReferenceManager().request_deferred_reference(reference_id, instance.set_data)
        return instance


class GenericReferencedList(GenericList):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_data(self, data):
        if not self.validate_data(data):
            return False

        self._data = []
        for sub_item in data:
            self._data.append(sub_item.get_id())

        return True

    def append_data(self, data):
        if not self.validate_data([data, ]):
            return False

        self._data.append(data.get_id())
        return True

    @classmethod
    def _decode(cls, data: t.Dict[str, t.Any]) -> t.Any:
        from backend.meta import ReferenceManager
        instance = ReferenceManager().request_instant_reference(data['id'])
        if instance:
            return instance

        reference_ids = data.pop('data', [])
        instance = cls(**data)

        for id_ in reference_ids:
            ReferenceManager().request_deferred_reference(id_, instance.append_data)

        return instance


@register_data_type
class ReferencedPortList(GenericReferencedList):
    valid_types = (BasePortNode, )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@register_data_type
class ReferencedNodeAttribute(GenericReferencedType):
    valid_types = (BaseAttributeNode,)
    reference_type = BaseAttributeNode

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@register_data_type
class ReferencedNode(GenericReferencedType):
    valid_types = (BaseNode, )
    reference_type = BaseNode

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@register_data_type
class ReferencedPort(GenericReferencedType):
    valid_types = (BasePortNode,)
    reference_type = BasePortNode

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

