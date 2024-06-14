import json

from collections.abc import MutableMapping, MutableSequence

from backend.abstracts import (AbstractAttribute,
                               AbstractNode,
                               AbstractPort,
                               PortType,
                               AbstractGraph)
from backend.events import *
from backend.exceptions import *
from backend.decorators import *


class TypedList(MutableSequence):
    def __init__(self, types: tuple):
        super().__init__()

        self.internal_data = list()
        self.types = types

    def __len__(self):
        return len(self.internal_data)

    def __getitem__(self, idx):
        return self.internal_data[idx]

    def __setitem__(self, idx, value):
        if not isinstance(value, self.types):
            raise TypeError(f'value must be of type {self.types}')

        self.internal_data[idx] = value

    def __delitem__(self, idx):
        del self.internal_data[idx]

    def insert(self, idx, value):
        if not isinstance(value, self.types):
            raise TypeError(f'value must be of type {self.types}')

        self.internal_data.insert(idx, value)

    def __repr__(self):
        return str(self.internal_data)


class BaseAttribute(AbstractAttribute):
    """
    A concrete attribute class that implements AbstractAttribute.
    """

    @register_events_decorator([AttributePreInstanced, AttributePostInstanced])
    def __init__(self):
        self._name: t.Optional[str] = None
        self._link: t.Optional[t.Any] = None
        self._node: t.Optional[BaseNode] = None
        self._value: t.Optional[t.Any] = None

    def __str__(self):
        return f"{super().__str__()}\n{json.dumps(self.serializer().serialize(self), indent=4)}"

    @register_events_decorator([AttributePreRemoved, AttributePostRemoved])
    def __del__(self):
        super().__del__()

    @register_events_decorator([AttributePreInitialized, AttributePostInitialized])
    def initialize(self, name, value):
        self.name = name
        self.set_value(value)

        return self

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError(f'attribute name must be a string.')

        self._name = value

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, value: 'BaseAttribute'):
        if not isinstance(value, BaseAttribute):
            raise TypeError(f'attribute link {value} is not an instance of {BaseAttribute}')

        self._link = value

    @link.deleter
    def link(self):
        self._link = None

    @property
    def node(self) -> 'BaseNode':
        return self._node

    @node.setter
    def node(self, value: 'BaseNode'):
        if not isinstance(value, BaseNode):
            raise TypeError(f'node {value} is not an instance of {BaseNode}')

        self._node = value

    def get_value(self):
        if self.link is None:
            return self._value
        else:
            return self.link.get_value()

    def set_value(self, value):
        if self.link is not None:
            raise LinkedAttributeError("attribute value is linked and cannot be changed directly")

        self._value = value

    @classmethod
    def create(cls, *args, **kwargs):
        return cls().initialize(*args, **kwargs)

    @classmethod
    def serializer(cls):
        from backend.serializers import AttributeSerializer
        return AttributeSerializer()


class BaseAttributeCollection(MutableMapping):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._data = {}
        self.__node: t.Optional[BaseNode] = None

        self.update(**kwargs)

    def __setitem__(self, key: str, value: BaseAttribute):
        if not isinstance(value, BaseAttribute):
            raise TypeError(f'attribute {value} is not an instance of {BaseAttribute}')

        if self.node:
            value.node = self.node

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
        self.update(**{attribute.name: attribute})

    @property
    def node(self) -> 'BaseNode':
        return self.__node

    @node.setter
    def node(self, value: 'BaseNode'):
        if not isinstance(value, BaseNode):
            raise TypeError(f'{value} is not an instance of {BaseNode}')

        self.__node = value


class BasePort(AbstractPort):

    @register_events_decorator([PortPreInstanced, PortPostInstanced])
    def __init__(self):
        self.__name: t.Optional[str] = None
        self.__mode: t.Optional[PortType] = None
        self.__node: t.Optional[BaseNode] = None

        self.connections: BasePortCollection[BasePort] = BasePortCollection()

    def __str__(self):
        return f"{super().__str__()}\n{json.dumps(self.serializer().serialize(self), indent=4)}"

    @register_events_decorator([PortPreRemoved, PortPostRemoved])
    def __del__(self):
        super().__del__()

    @register_events_decorator([PortPreInitialized, PortPostInitialized])
    def initialize(self, name: str, mode: PortType):
        self.name = name
        self.mode = mode

        return self

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        if not isinstance(name, str):
            raise TypeError(f'port {name} is not an instance of {str}')

        self.__name = name

    @property
    def mode(self) -> PortType | None:
        return self.__mode

    @mode.setter
    def mode(self, mode: PortType):
        if not isinstance(mode, PortType):
            raise TypeError(f'port type {mode} is not an instance of {PortType}')

        self.__mode = mode

    @property
    def node(self) -> t.Optional['BaseNode']:
        return self.__node

    @node.setter
    def node(self, node: 'BaseNode'):
        if not isinstance(node, BaseNode):
            raise TypeError(f'node {node} is not an instance of {BaseNode}')

        self.__node = node

    def connect_to(self, port):
        self.connections.append(port)
        port.connections.append(self)

        return True

    def has_connections(self):
        return bool(len(self.connections))

    def disconnect(self, index):
        self.connections[index].connections.remove(self)
        self.connections.pop(index)

        return True

    @classmethod
    def create(cls, *args, **kwargs):
        return cls().initialize(*args, **kwargs)

    @classmethod
    def serializer(cls):
        from backend.serializers import PortSerializer
        return PortSerializer()


class BasePortCollection(TypedList):
    def __init__(self):
        super().__init__(self.__class__.__mro__)

        self.__node: t.Optional[BaseNode] = None

    def __setitem__(self, idx, value):
        if value in self:
            raise ValueError(f'port {value} is already present in the collection')

        super().__setitem__(idx, value)

        if self.node:
            value.node = self.node

    def insert(self, idx, value):
        if value in self:
            raise ValueError(f'port {value} is already present in the collection')

        super().insert(idx, value)

        if self.node:
            value.node = self.node

    @property
    def node(self) -> 'BaseNode':
        return self.__node

    @node.setter
    def node(self, value: 'BaseNode'):
        if not isinstance(value, BaseNode):
            raise TypeError(f'graph {value} is not an instance of {BaseNode}')

        self.__node = value

    def connect_to(self, port_index, port_instance):
        return self[port_index].connect_to(port_instance)

    def has_connections(self, port_index):
        return self[port_index].has_connections()

    def disconnect(self, port_index: int, connection_index: int = 0):
        self[port_index].disconnect(connection_index)

    def data(self, port_index, connection_index: int = 0):
        return self[port_index].data(connection_index)


class BaseNode(AbstractNode):

    @register_events_decorator([NodePreInstanced, NodePostInstanced])
    def __init__(self):
        """
        Implement the base class of AbstractNode.
        """
        self.__name: t.Optional[str] = None
        self.__graph: t.Optional[BaseGraph] = None

        self.__attributes = None
        self.__inputs = None
        self.__outputs = None

    def __str__(self):
        return f"{super().__str__()}\n{json.dumps(self.serializer().serialize(self), indent=4)}"

    @register_events_decorator([NodePreRemoved, NodePostRemoved])
    def __del__(self):
        super().__del__()

    @register_events_decorator([NodePreInitialized, NodePostInitialized])
    def initialize(self, name: str):
        self.name = name
        
        return self

    @property
    def name(self) -> str:
        if not self.__name:
            raise AttributeError(f'node has not been initialized properly.')

        return self.__name

    @name.setter
    def name(self, name: str):
        if not isinstance(name, str):
            raise TypeError(f'{name} is not an instance of {str}')

        self.__name = name

    @property
    def graph(self) -> t.Optional['BaseGraph']:
        return self.__graph

    @graph.setter
    def graph(self, value: 'BaseGraph'):
        if not isinstance(value, BaseGraph):
            raise TypeError(f'graph {value} is not an instance of {BaseGraph}')

        self.__graph = value

    @property
    def attributes(self) -> t.Optional['BaseAttributeCollection']:
        return self.__attributes

    @attributes.setter
    def attributes(self, value: 'BaseAttributeCollection'):
        if not isinstance(value, BaseAttributeCollection):
            raise TypeError(f'{value} is not an instance of {BaseAttributeCollection}')

        value.node = self
        self.__attributes = value

    @property
    def inputs(self) -> t.Optional['BasePortCollection']:
        return self.__inputs

    @inputs.setter
    def inputs(self, value: 'BasePortCollection'):
        if not isinstance(value, BasePortCollection):
            raise TypeError(f'{value} is not an instance of {BasePortCollection}')

        value.node = self
        self.__inputs = value

    @property
    def outputs(self) -> t.Optional['BasePortCollection']:
        return self.__outputs

    @outputs.setter
    def outputs(self, value: 'BasePortCollection'):
        if not isinstance(value, BasePortCollection):
            raise TypeError(f'{value} is not an instance of {BasePortCollection}')

        value.node = self
        self.__outputs = value

    def data(self) -> t.Optional[t.Any]:
        return

    @classmethod
    def create(cls, *args, **kwargs):
        return cls().initialize(*args, **kwargs)

    @classmethod
    def serializer(cls):
        from backend.serializers import NodeSerializer
        return NodeSerializer()


class BaseNodeCollection(TypedList):
    def __init__(self):
        super().__init__(self.__class__.__mro__)

        self.__graph: t.Optional[BaseGraph] = None

    def __setitem__(self, idx, value):
        super().__setitem__(idx, value)

        if self.graph:
            value.graph = self.graph

    def insert(self, idx, value):
        super().insert(idx, value)

        if self.graph:
            value.graph = self.graph

    def has_nodes(self):
        return bool(len(self))

    @property
    def graph(self) -> t.Optional['BaseGraph']:
        return self.__graph

    @graph.setter
    def graph(self, value: 'BaseGraph'):
        if not isinstance(value, BaseGraph):
            raise TypeError(f'graph {value} is not an instance of {BaseGraph}')

        self.__graph = value


class BaseGraph(AbstractGraph):

    @register_events_decorator([GraphPreInstanced, GraphPostInstanced])
    def __init__(self):
        self.__name: t.Optional[str] = None
        self.__parent = None
        self.__nodes = None
        self.__graphs = None

    def __str__(self):
        return f"{super().__str__()}\n{json.dumps(self.serializer().serialize(self), indent=4)}"

    @register_events_decorator([GraphPreRemoved, GraphPostRemoved])
    def __del__(self):
        super().__del__()

    @register_events_decorator([GraphPreInitialized, GraphPostInitialized])
    def initialize(self, name: str):
        self.name = name

        return self

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: t.Optional[str]):
        if not isinstance(value, str):
            raise TypeError(f'{value} is not an instance of {str}')

        self.__name = value

    @property
    def parent(self):
        return self.__name

    @parent.setter
    def parent(self, value: t.Optional[str]):
        if not isinstance(value, BaseGraph):
            raise TypeError(f'{value} is not an instance of {BaseGraph}')

        self.__parent = value

    @property
    def nodes(self):
        return self.__nodes

    @nodes.setter
    def nodes(self, value):
        if not isinstance(value, BaseNodeCollection):
            raise TypeError(f'{value} is not an instance of {BaseNodeCollection}')

        value.graph = self
        self.__nodes = value

    @property
    def graphs(self):
        return self.__graphs

    @graphs.setter
    def graphs(self, value):
        if not isinstance(value, BaseGraphCollection):
            raise TypeError(f'{value} is not an instance of {list}')

        value.parent = self
        self.__graphs = value
    @classmethod
    def create(cls, *args, **kwargs):
        return cls().initialize(*args, **kwargs)

    @classmethod
    def serializer(cls):
        from backend.serializers import GraphSerializer
        return GraphSerializer()


class BaseGraphCollection(TypedList):
    def __init__(self):
        super().__init__(self.__class__.__mro__)

        self.__parent: t.Optional[BaseGraph] = None

    def __setitem__(self, idx, value):
        super().__setitem__(idx, value)

        if self.parent:
            value.parent = self.parent

    def insert(self, idx, value):
        super().insert(idx, value)

        if self.parent:
            value.parent = self.parent

    def has_nodes(self):
        return bool(len(self))

    @property
    def parent(self) -> t.Optional['BaseGraph']:
        return self.__parent

    @parent.setter
    def parent(self, value: 'BaseGraph'):
        if not isinstance(value, BaseGraph):
            raise TypeError(f'graph {value} is not an instance of {BaseGraph}')

        self.__parent = value
