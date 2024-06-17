import json
import enum

from collections.abc import MutableSequence

from backend.abstracts import (AbstractAttribute,
                               AbstractNode,
                               AbstractPort,
                               AbstractGraph,
                               AbstractMappingCollection,
                               AbstractSerializableMixin)
from backend.events import *
from backend.validators import *


class SerializableMixin(AbstractSerializableMixin):

    @classmethod
    def serializer(cls):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    def serialize(self):
        serializable = set(self.attributes + self.identities + self.associations)

        data = {key: getattr(self, f'get_{key}')(serialize=True) for key in serializable}
        return data

    @classmethod
    def deserialize(cls, **kwargs):
        associations = kwargs.pop('associations', False)
        associations_kwargs = {}

        for key in cls.associations + cls.identities:
            if key in kwargs:
                associations_kwargs[key] = kwargs.pop(key)

        instance = cls(**kwargs)

        if associations:
            instance.deserialize_associations(**associations_kwargs)

        return instance

    def deserialize_associations(self, **kwargs):
        for key in self.associations:
            value = getattr(self, f'find_{key}')(kwargs.get(f'{key}'))
            if value:
                getattr(self, f'set_{key}')(value)

        return self


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


class BaseAttribute(SerializableMixin, AbstractAttribute):
    """
    A base attribute class that implements AbstractAttribute.
    """

    identities = ['class',
                  'type',
                  'id']

    attributes = ['name',
                  'value',
                  'parent',
                  'link']

    associations = ['parent',
                    'link']

    @register_events_decorator([AttributePreInitialized, AttributePostInitialized])
    def __init__(self, **kwargs):
        self._id = kwargs.pop('id')

        self._name: t.Optional[str] = None
        self._link: t.Optional[BaseAttribute] = None
        self._parent: t.Optional[BaseNode] = None
        self._value: t.Optional[t.Any] = None

        for key in self.attributes:
            if key in kwargs:
                getattr(self, f'set_{key}')(kwargs[key])

    def __str__(self):
        return f'{super().__str__()}\n{json.dumps(self.serialize(), indent=4)}'

    @register_events_decorator([AttributePreRemoved, AttributePostRemoved])
    def __del__(self):
        super().__del__()

    def get_class(self, serialize=False):
        if serialize:
            return self.__class__.__name__

        return self.__class__

    def get_type(self, serialize=False):
        return self.entity_type.value

    def get_id(self, serialize=False):
        return self._id

    def get_name(self, serialize=False):
        return self._name

    def set_name(self, name):
        if not self.validate_name(name):
            return False

        self._name = name
        return True

    def del_name(self):
        self._name = None

    def validate_name(self, name):
        return attribute_name_validator(self, name)

    def get_parent(self, serialize=False):
        if not self._parent:
            return

        if serialize:
            return self._parent.get_id()

        return self._parent

    def set_parent(self, parent: 'BaseNode'):
        if not self.validate_parent(parent):
            return False

        self._parent = parent
        return True

    def del_parent(self):
        self._parent = None

    @classmethod
    def find_parent(cls, id_):
        from backend.meta import InstanceManager
        return InstanceManager().get_instance(id_)

    def validate_parent(self, parent):
        if not isinstance(parent, BaseNode):
            logger.warn(f'parent {parent} is not an instance of {BaseNode}')
            return False

        return True

    def get_link(self, serialize=False):
        if not self._link:
            return

        if serialize:
            return self._link.get_id()

        return self._link

    def set_link(self, link: 'BaseAttribute'):
        if not self.validate_link(link):
            return False

        self._link = link
        return True

    def del_link(self):
        self._link = None

    def validate_link(self, link):
        if not isinstance(link, BaseAttribute):
            logger.warn(f'attribute link {link} is not an instance of {BaseAttribute}')
            return False

        return True

    @classmethod
    def find_link(cls, id_):
        from backend.meta import InstanceManager
        return InstanceManager().get_instance(id_)

    def get_value(self, serialize=False):
        if self.get_link() is None:
            return self._value
        else:
            return self.get_link().get_value()

    def set_value(self, value):
        if not self.validate_value(value):
            return False

        self._value = value
        return True

    def del_value(self):
        self._value = None

    def validate_value(self, value):
        if self.get_link() is not None:
            logger.warn(f'attribute value is linked and cannot be changed directly : {self.get_link()}')
            return False

        if not isinstance(value, self.valid_types):
            logger.warn(f'attribute value must be an instance of {self.valid_types} not {type(value)}.')
            return False

        return True

    @classmethod
    def serializer(cls):
        from backend.serializers import AttributeSerializer
        return AttributeSerializer()


class BaseMappingCollection(AbstractMappingCollection):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._data = {}
        self._parent: t.Optional[BaseNode] = None

    def __setitem__(self, key: str, value):
        if self.validate_item(key, value):
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

    def validate_item(self, key, item):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    def get_parent(self, serialize=False):
        if serialize:
            return self._parent.get_id()

        return self._parent

    def set_parent(self, parent):
        if not self.validate_parent(parent):
            return False

        self._parent = parent
        return True

    def del_parent(self):
        self._parent = None

    def validate_parent(self, parent):
        if not isinstance(parent, BaseNode):
            logger.warn(f'{parent} is not an instance of {BaseNode}')

        return True

    def get_class(self, serialize=False):
        if serialize:
            return self.__class__.__name__

        return self.__class__

    def add_entry(self, entry):
        self.__setitem__(entry.get_name(), entry)

    def add_entries(self, entries):
        for entry in entries:
            self.__setitem__(entry.get_name(), entry)

    def set_entries(self, entries: t.Iterable):
        for entry in entries:
            self.__setitem__(entry.get_name(), entry)

        return True

    def get_entries(self, serialize=False):
        if serialize:
            return [entry.get_id() for entry in self.values()]

        return list(self.values())

    @classmethod
    def find_entries(cls, ids):
        entries = []
        from backend.meta import InstanceManager

        for id_ in ids:
            instance = InstanceManager().get_instance(id_)
            if instance:
                entries.append(instance)

        return entries


class BaseAttributeCollection(SerializableMixin, BaseMappingCollection):

    identities = ['class',
                  ]

    associations = ['entries'
                    ]

    def validate_item(self, key, item):
        if not isinstance(item, BaseAttribute):
            logger.warn(f'attribute {item} is not an instance of {BaseAttribute}')

        return True

    @classmethod
    def serializer(cls):
        from backend.serializers import AttributeCollectionSerializer
        return AttributeCollectionSerializer()


class PortType(enum.StrEnum):
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'


class BasePort(SerializableMixin, AbstractPort):

    identities = ['class',
                  'type',
                  'id']

    attributes = ['name',
                  'mode',
                  'parent',
                  ]

    associations = ['parent',
                    'connections']

    @register_events_decorator([PortPreInitialized, PortPostInitialized])
    def __init__(self, **kwargs):
        self._id = kwargs.pop('id')

        self._name: t.Optional[str] = None
        self._mode: t.Optional[PortType] = None
        self._parent: t.Optional[BaseNode] = None
        self._connections: t.Optional[BasePortCollection[BasePort]] = None

        for key in self.attributes:
            if key in kwargs:
                getattr(self, f'set_{key}')(kwargs[key])

    def __str__(self):
        return f'{super().__str__()}\n{json.dumps(self.serializer().serialize(self), indent=4)}'

    @register_events_decorator([PortPreRemoved, PortPostRemoved])
    def __del__(self):
        super().__del__()

    def get_class(self, serialize=False):
        if serialize:
            return self.__class__.__name__

        return self.__class__

    def get_type(self, serialize=False):
        return self.entity_type.value

    def get_id(self, serialize=False):
        return self._id

    def set_id(self, _id):
        self._id = _id

    def del_id(self):
        self._id = None

    def get_name(self, serialize=False):
        return self._name

    def set_name(self, name):
        if not self.validate_name(name):
            return False

        self._name = name
        return True

    def del_name(self):
        self._name = None

    def validate_name(self, name):
        return port_name_validator(self, name)

    def get_parent(self, serialize=False):
        if not self._parent:
            return

        if serialize:
            return self._parent.get_id()

        return self._parent

    def set_parent(self, parent: 'BaseNode'):
        if not self.validate_parent(parent):
            return False

        self._parent = parent
        return True

    def del_parent(self):
        self._parent = None

    @classmethod
    def find_parent(cls, id_):
        from backend.meta import InstanceManager
        return InstanceManager().get_instance(id_)

    def validate_parent(self, parent):
        if not isinstance(parent, BaseNode):
            logger.warn(f'parent {parent} is not an instance of {BaseNode}')
            return False

        return True

    def get_mode(self, serialize=False):
        if serialize:
            return self._mode.value

        return self._mode

    def set_mode(self, mode):
        if isinstance(mode, str):
            mode = getattr(PortType, mode)

        if not self.validate_mode(mode):
            return False

        self._mode = mode
        return True

    def del_mode(self):
        self._mode = None

    def validate_mode(self, mode):
        if not isinstance(mode, PortType):
            logger.warn(f'port type {mode} is not an instance of {PortType}')
            return False

        return True

    def get_connections(self, serialize=False):
        if serialize:
            return [connection.get_id() for connection in self._connections]

        return self._connections

    def set_connections(self, connections):
        if not self.validate_connections(connections):
            return False

        self._connections = connections
        return True

    def del_connections(self):
        self._connections = None

    def validate_connections(self, connections):
        return True

    def find_connections(self, ids):
        connections = []
        from backend.meta import InstanceManager

        for id_ in ids:
            instance = InstanceManager().get_instance(id_)
            if instance:
                connections.append(instance)

        return connections

    def connect_to(self, port):
        self._connections.append(port)
        port.get_connections().append(self)

        return True

    def has_connections(self):
        return bool(len(self.get_connections()))

    def disconnect(self, index):
        self._connections[index].get_connections().remove(self)
        self._connections.pop(index)

        return True

    @classmethod
    def serializer(cls):
        from backend.serializers import PortSerializer
        return PortSerializer()


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
