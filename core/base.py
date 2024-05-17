import typing as t
from collections.abc import MutableMapping

from core.abstract import (AbstractAttribute,
                           AbstractNode,
                           AbstractPort,
                           AbstractAttributeSerializer,
                           AbstractAttributeCollectionSerializer)


class BaseAttribute(AbstractAttribute):
    """
    A concrete attribute class that implements AbstractAttribute.
    """

    def __init__(self, name, value):
        self._name: t.Optional = None
        self.set_name(name)

        self._value: t.Optional = None
        self.set_value(value)

        self._connection: t.Optional = None

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

    def get_value(self) -> t.Any:
        return self._value


class BaseAttributeCollection(MutableMapping):
    def __init__(self, **kwargs):
        self._data = {}

        self.update(**kwargs)

    def __setitem__(self, key: str, value: BaseAttribute):
        if not isinstance(value, BaseAttribute):
            raise TypeError(f'attribute {value} is not an instance of {BaseAttribute}')

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

    def add(self, attribute: BaseAttribute):
        self.update(**{attribute.get_name(): attribute})


class BaseNode(AbstractNode):
    def __init__(self) -> None:
        """
        Implement the base class of AbstractNode.
        """
        self.attributes: BaseAttributeCollection = BaseAttributeCollection()
        self.inputs = {}
        self.outputs = {}


class BasePort(AbstractPort):
    def __init__(self, name, node):
        self._name: t.Optional[str] = name
        self._node: t.Optional[BaseNode] = node

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> bool:
        if not isinstance(name, str):
            raise TypeError(f'port name must be a string.')

        self._name = name
        return True

    def get_node(self) -> t.Optional[BaseNode]:
        return self._node

    def set_node(self, node: BaseNode) -> bool:
        if not isinstance(node, BaseNode):
            raise TypeError(f'node must be an instance of {type(BaseNode)}.')

        self._node = node
        return True

    def get_valid_types(self) -> t.List[t.Type]:
        return []


class BaseAttributeSerializer(AbstractAttributeSerializer):

    def serialize(self, attr: BaseAttribute) -> t.Dict[str, t.Any]:
        return {'type': attr.__class__.__name__,
                'name': attr.get_name(),
                'value': attr.get_value()}

    def deserialize(self, attr_data: t.Dict[str, t.Any]) -> BaseAttribute:
        raise NotImplementedError('must override this method')


class BaseAttributeCollectionSerializer(AbstractAttributeCollectionSerializer):
    def serialize(self, collection_instance: BaseAttributeCollection) -> t.Dict[str, t.Any]:
        raise NotImplementedError('must override this method')

    def deserialize(self, collection_data: t.Dict[str, t.Any]) -> BaseAttributeCollection:
        raise NotImplementedError('must override this method')




