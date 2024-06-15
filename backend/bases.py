import json

from collections.abc import MutableMapping, MutableSequence

from backend.abstracts import (AbstractAttribute,
                               AbstractNode,
                               AbstractPort,
                               PortType,
                               AbstractGraph)
from backend.events import *
from backend.validators import *


class TypedSequence(MutableSequence):
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
    A base attribute class that implements AbstractAttribute.
    """

    @register_events_decorator([AttributePreInitialized, AttributePostInitialized])
    def __init__(self, **kwargs):
        self._name: t.Optional[str] = None
        self._link: t.Optional[BaseAttribute] = None
        self._parent: t.Optional[BaseNode] = None
        self._value: t.Optional[t.Any] = None

        'name' in kwargs and self.set_name(kwargs.get('name'))
        'value' in kwargs and self.set_value(kwargs.get('value'))
        'parent' in kwargs and self.set_parent(kwargs.get('parent'))
        'link' in kwargs and self.set_link(kwargs.get('link'))

    def __str__(self):
        return f'{super().__str__()}\n{json.dumps(self.serialize(), indent=4)}'

    @register_events_decorator([AttributePreRemoved, AttributePostRemoved])
    def __del__(self):
        super().__del__()

    def identifier(self):
        if not self.get_parent():
            return f'{self.get_name()}'

        return f'{self.get_parent().identifier()}/{self.get_name()}'

    def get_name(self):
        return self._name

    @validate(attribute_name_validator)
    def set_name(self, name):
        self._name = name.strip().lower().replace(' ', '')
        return True

    def del_name(self):
        del self._name

    def get_link(self):
        return self._link

    def set_link(self, link: 'BaseAttribute'):
        if not isinstance(link, BaseAttribute):
            warnings.warn(f'attribute link {link} is not an instance of {BaseAttribute}')
            return False

        self._link = link
        return True

    def del_link(self):
        self._link = None

    def get_parent(self) -> 'BaseNode':
        return self._parent

    def set_parent(self, parent: 'BaseNode'):
        if not isinstance(parent, BaseNode):
            warnings.warn(f'parent {parent} is not an instance of {BaseNode}')
            return False

        self._parent = parent
        return True

    def del_parent(self):
        self._parent = None

    def get_value(self):
        if self.get_link() is None:
            return self._value
        else:
            return self.get_link().get_value()

    def set_value(self, value):
        if self.get_link() is not None:
            logger.warn(f'attribute value is linked and cannot be changed directly : {self.get_link()}')
            return False

        if not isinstance(value, self.valid_types):
            logger.warn(f'attribute value must be an instance of {self.valid_types} not {type(value)}.')
            return False

        self._value = value
        return True

    def del_value(self):
        del self._value

    @classmethod
    def serializer(cls):
        from backend.serializers import AttributeSerializer
        return AttributeSerializer()

    def serialize(self):
        data = {'class': self.__class__.__name__,
                'name': self.get_name(),
                'value': self.get_value()}

        if self.get_parent():
            data['parent'] = self.get_parent().identifier()

        if self.get_link():
            data['link'] = self.get_link().identifier()

        return data

    @classmethod
    def deserialize(cls, **kwargs):
        # TODO we need to find associations and set them properly in data dict

        'parent' in kwargs and kwargs.pop('parent')
        'link' in kwargs and kwargs.pop('link')

        return cls(**kwargs)


class BaseAttributeCollection(MutableMapping):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._data = {}
        self._parent: t.Optional[BaseNode] = None

        self.update(**kwargs)

    def __setitem__(self, key: str, value: BaseAttribute):
        if not isinstance(value, BaseAttribute):
            raise TypeError(f'attribute {value} is not an instance of {BaseAttribute}')

        if self.get_parent():
            value.set_parent(self.get_parent())

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

    def get_parent(self) -> 'BaseNode':
        return self._parent

    def set_parent(self, parent: 'BaseNode'):
        if not isinstance(parent, BaseNode):
            raise TypeError(f'{parent} is not an instance of {BaseNode}')

        self._parent = parent

    @classmethod
    def serializer(cls):
        from backend.serializers import AttributeCollectionSerializer
        return AttributeCollectionSerializer()

    def serialize(self):
        entries = []
        for key, attr in self.items():
            entries.append(attr.serializer().serialize(attr))

        data = {'class': self.__class__.__name__,
                'entries': entries}

        return data

    @classmethod
    def deserialize(cls, data):
        from backend.registry import RegisteredAttributes
        instance = cls()

        for entry_data in data['entries']:
            instance.add(RegisteredAttributes[entry_data['class']].serializer().deserialize(entry_data))

        # TODO we need to set parent of collection and all entries
        return instance


class BasePort(AbstractPort):

    @register_events_decorator([PortPreInitialized, PortPostInitialized])
    def __init__(self, **kwargs):
        self._name: t.Optional[str] = None
        self._mode: t.Optional[PortType] = None
        self._parent: t.Optional[BaseNode] = None

        self.connections: BasePortCollection[BasePort] = BasePortCollection()

        'name' in kwargs and self.set_name(kwargs.get('name'))
        'mode' in kwargs and self.set_mode(kwargs.get('mode'))
        'parent' in kwargs and self.set_parent(kwargs.get('parent'))

    def __str__(self):
        return f'{super().__str__()}\n{json.dumps(self.serializer().serialize(self), indent=4)}'

    @register_events_decorator([PortPreRemoved, PortPostRemoved])
    def __del__(self):
        super().__del__()

    def identifier(self):
        if not self.get_parent():
            return f'{self.get_name()}'

        return f'{self.get_parent().identifier()}/{self.get_name()}'

    def get_name(self) -> str:
        return self._name

    @validate(port_name_validator)
    def set_name(self, name):
        self._name = name.strip().lower().replace(' ', '')
        return True

    def del_name(self):
        del self._name

    def get_mode(self) -> PortType | None:
        return self._mode

    def set_mode(self, mode: PortType):
        if not isinstance(mode, PortType):
            raise TypeError(f'port type {mode} is not an instance of {PortType}')

        self._mode = mode

    def del_mode(self):
        del self._mode

    def get_parent(self) -> t.Optional['BaseNode']:
        return self._parent

    def set_parent(self, parent: 'BaseNode'):
        if not isinstance(parent, BaseNode):
            raise TypeError(f'parent {parent} is not an instance of {BaseNode}')

        self._parent = parent

    def del_parent(self):
        self._parent = None

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
    def serializer(cls):
        from backend.serializers import PortSerializer
        return PortSerializer()

    def serialize(self):
        connections = []

        for connection in self.connections:
            connections.append(connection.identifier())

        data = {'class': self.__class__.__name__,
                'mode': str(self.get_mode()),
                'name': self.get_name(),
                'connections': connections}

        if self.get_parent():
            data['parent'] = self.get_parent().identifier()

        return data

    @classmethod
    def deserialize(cls, **kwargs):
        # TODO we need to find associations and set them properly in data dict

        'parent' in kwargs and kwargs.pop('parent')
        'connections' in kwargs and kwargs.pop('connections')

        kwargs['mode'] = getattr(PortType, kwargs['mode'].capitalize())
        return cls(**kwargs)


class BasePortCollection(TypedSequence):
    def __init__(self):
        super().__init__(self.__class__.__mro__)

        self._parent: t.Optional[BaseNode] = None

    def __setitem__(self, idx, value):
        if value in self:
            raise ValueError(f'port {value} is already present in the collection')

        super().__setitem__(idx, value)

        if self.get_parent():
            value.set_parent(self.get_parent())

    def insert(self, idx, value):
        if value in self:
            raise ValueError(f'port {value} is already present in the collection')

        super().insert(idx, value)

        if self.get_parent():
            value.set_parent(self.get_parent())

    def get_parent(self) -> 'BaseNode':
        return self._parent

    def set_node(self, parent: 'BaseNode'):
        if not isinstance(parent, BaseNode):
            raise TypeError(f'parent {parent} is not an instance of {BaseNode}')

        self._parent = parent

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

    def identifier(self):
        return f'{self.name}'

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


class BaseNodeCollection(TypedSequence):
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


class BaseGraphCollection(TypedSequence):
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
