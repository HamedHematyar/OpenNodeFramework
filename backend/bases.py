import json
import enum
import copy
from collections.abc import MutableMapping

from backend.abstracts import (AbstractType,
                               AbstractNode,
                               AbstractPort,
                               AbstractEntitySerializer,
                               EntityType)
from backend.events import *
from backend.validators import *


class EntitySerializer(AbstractEntitySerializer):

    def serialize(self) -> t.Dict[str, t.Any]:
        return self._encode()

    @classmethod
    def deserialize(cls, data: t.Dict[str, t.Any], *args, **kwargs) -> t.Any:
        return cls._decode(copy.deepcopy(data), *args, **kwargs)

    def dump(self, file_path, *args, **kwargs):
        with open(file_path, 'w') as file:
            json.dump(self, file, default=self._encode, *args, **kwargs)

    def dumps(self, **kwargs):
        return json.dumps(self._encode(), **kwargs)

    @classmethod
    def load(cls, file_path, *args, **kwargs):
        with open(file_path, 'r') as file:
            return cls._decode(json.load(file), *args, **kwargs)

    def _encode(self, *args, **kwargs) -> t.Dict[str, t.Any]:
        serializable = set(self.id_attributes + self.primary_attributes + self.relation_attributes)

        data = {}
        for key in serializable:
            getter = getattr(self, f'get_{key}', None)
            if not getter:
                continue

            data[key] = getter(serialize=True)

        return data

    @classmethod
    def _decode(cls, data: t.Dict[str, t.Any], *args, **kwargs) -> t.Any:
        relations = data.pop('relations', kwargs.pop('relations', False))
        relations_data = {}

        for key in cls.relation_attributes + cls.id_attributes:
            if key in data:
                relations_data[key] = data.pop(key)

        instance = cls(**data)

        if relations:
            instance.deserialize_relations(**relations_data)

        return instance

    def deserialize_relations(self, **kwargs):
        for key in self.relation_attributes:
            value = getattr(self, f'deserialize_{key}')(kwargs.get(f'{key}'))
            if value:
                getattr(self, f'set_{key}')(value)

        return self


class DictCollection(MutableMapping):

    def __init__(self, *args, **kwargs):
        self._internal_data = {}

    def __getitem__(self, key):
        return self._internal_data[key]

    def __setitem__(self, key, value):
        if not self.validate_item(value):
            return False

        self._internal_data[key] = value
        return True

    def __delitem__(self, key):
        del self._internal_data[key]

    def __iter__(self):
        return iter(self._internal_data)

    def __len__(self):
        return len(self._internal_data)

    def __repr__(self):
        return f'{self.__class__.__name__}({self._internal_data})'

    def get_items(self, serialize=False):
        if serialize:
            return {key: value.get_id() for key, value in self.items()}

        return self.items()

    def set_items(self, items: t.Iterable):
        if not self.validate_items(items):
            return False

        self.update(items)
        return True

    def del_items(self):
        self.clear()

    def validate_items(self, items):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    def validate_item(self, item):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')


class TypedDictCollection(DictCollection):
    valid_types = tuple()
    validate_uniqueness = True

    def validate_items(self, items):
        for item in items:
            if not self.validate_item(item):
                return False

        return True

    @classmethod
    def deserialize_items(cls, ids):
        from backend.meta import InstanceManager

        entries = []
        for id_ in ids:
            instance = InstanceManager().get_instance(id_)
            if instance:
                entries.append(instance)

        return entries

    def validate_item(self, item):
        if not isinstance(item, self.valid_types):
            logger.warn(f'item value must be of type {self.valid_types}')
            return False

        if self.validate_uniqueness and item in self:
            logger.warn(f'{item} is already present in the collection')
            return False

        return True


class BaseType(EntitySerializer, AbstractType):
    id_attributes = ['class',
                     'type',
                     'id']

    primary_attributes = ['data']

    @register_events_decorator([PreTypeInitialized, PostTypeInitialized])
    def __init__(self, **kwargs):
        self._id = kwargs.pop('id')
        self._data: t.Optional[str] = None

        if 'data' in kwargs:
            self.set_data(kwargs.pop('data'))

    @register_events_decorator([PreTypeDeleted, PostTypeDeleted])
    def delete(self):
        from backend.meta import InstanceManager
        InstanceManager().remove_instance(self)

        del self

    def get_class(self, serialize=False):
        if serialize:
            return self.__class__.__name__

        return self.__class__

    def get_type(self, serialize=False):
        return self.entity_type.value

    def get_id(self, serialize=False):
        return self._id

    @property
    def data(self):
        return self.get_data()

    def get_data(self, serialize=False):
        return self._data

    @register_events_decorator([PreTypeDataChanged, PostTypeDataChanged])
    def set_data(self, data):
        if not self.validate_data(data):
            return False

        self._data = data
        return True

    def del_data(self):
        self._data = None

    def validate_data(self, data):
        if not isinstance(data, self.valid_types):
            logger.warn(f'attribute value must be an instance of {self.valid_types} not {type(data)}.')
            return False

        return True


class PortType(enum.StrEnum):
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'


class BasePort(EntitySerializer, AbstractPort):
    id_attributes = ['class',
                     'type',
                     'id']

    primary_attributes = ['name',
                          'mode',
                          'parent']

    relation_attributes = ['parent',
                           'connections']

    @register_events_decorator([PrePortInitialized, PostPortInitialized])
    def __init__(self, **kwargs):
        self._id = kwargs.pop('id')

        self._name: t.Optional[str] = None
        self._mode: t.Optional[PortType] = None
        self._parent: t.Optional[BaseNode] = None
        self._connections: t.Optional[BasePortCollection[BasePort]] = None

        for key in self.primary_attributes:
            if key in kwargs:
                getattr(self, f'set_{key}')(kwargs[key])

    @register_events_decorator([PrePortDeleted, PostPortDeleted])
    def delete(self):
        from backend.meta import InstanceManager
        InstanceManager().remove_instance(self)

        del self

    def get_class(self, serialize=False):
        if serialize:
            return self.__class__.__name__

        return self.__class__

    def get_type(self, serialize=False):
        return self.entity_type.value

    def get_id(self, serialize=False):
        return self._id

    @property
    def name(self):
        return self.get_name()

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

    @property
    def parent(self):
        return self.get_parent()

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
    def deserialize_parent(cls, id_):
        from backend.meta import InstanceManager
        return InstanceManager().get_instance(id_)

    def validate_parent(self, parent):
        if not isinstance(parent, BasePortCollection):
            logger.warn(f'parent {parent} is not an instance of {BaseNode}')
            return False

        return True

    @property
    def mode(self):
        return self.get_mode()

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

    @property
    def connections(self):
        return self.get_connections()

    def get_connections(self, serialize=False):
        if serialize:
            return self._connections.serialize()

        return self._connections

    def set_connections(self, connections):
        if not self.validate_connections(connections):
            return False

        self._connections = connections
        # self._connections.set_parent(self)
        return True

    def del_connections(self):
        self._connections = None

    def validate_connections(self, connections):
        return True

    def deserialize_connections(self, data):
        return self._connections.deserialize(data, relations=True)

    def connect_to(self, port):
        self._connections.append(port)
        port.connections.append(self)

        return True

    def has_connections(self):
        return bool(len(self.get_connections()))

    def disconnect(self, index):
        self._connections[index].connections.remove(self)
        self._connections.pop(index)

        return True


class BasePortCollection(EntitySerializer, TypedDictCollection):
    id_attributes = ['class'
                     ]

    primary_attributes = ['parent']

    relation_attributes = ['parent',
                           'entries'
                           ]

    def validate_parent(self, parent):
        if not isinstance(parent, (BasePort, BaseNode)):
            logger.warn(f'{parent} is not an instance of {BaseNode}')

        return True

    @classmethod
    def deserialize_parent(cls, id_):
        from backend.meta import InstanceManager
        return InstanceManager().get_instance(id_)

    def validate_entries(self):
        return True

    @classmethod
    def deserialize_entries(cls, ids):
        entries = []
        from backend.meta import InstanceManager

        for id_ in ids:
            instance = InstanceManager().get_instance(id_)
            if instance:
                entries.append(instance)

        return entries

    def connect_to(self, port_index, port_instance):
        return self[port_index].connect_to(port_instance)

    def has_connections(self, port_index):
        return self[port_index].has_connections()

    def disconnect(self, port_index: int, connection_index: int = 0):
        self[port_index].disconnect(connection_index)

    def data(self, port_index, connection_index: int = 0):
        return self[port_index].data(connection_index)


class BaseAttributeNode(EntitySerializer, AbstractNode):
    entity_type = EntityType.NodeAttribute

    id_attributes = ['class',
                     'type',
                     'id']

    relation_attributes = ['attributes',
                           ]

    @register_events_decorator([PreNodeInitialized, PostNodeInitialized])
    def __init__(self, **kwargs):
        self._id = kwargs.pop('id')

        self._attributes = None

    @register_events_decorator([PreNodeDeleted, PostNodeDeleted])
    def delete(self):
        from backend.meta import InstanceManager
        InstanceManager().remove_instance(self)

        del self

    def get_class(self, serialize=False):
        if serialize:
            return self.__class__.__name__

        return self.__class__

    def get_type(self, serialize=False):
        return self.entity_type.value

    def get_id(self, serialize=False):
        return self._id

    @property
    def attributes(self):
        return self.get_attributes()

    def get_attributes(self, serialize=False):
        if serialize:
            return self._attributes.serialize()

        return self._attributes

    def set_attributes(self, attributes):
        if not self.validate_attributes(attributes):
            return False

        self._attributes = attributes
        return True

    def del_attributes(self):
        self._attributes.clear()

    def validate_attributes(self, attributes):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    def deserialize_attributes(self, data):
        return self._attributes.deserialize(data, relations=True)

    def data(self):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')


class BaseNode(EntitySerializer, AbstractNode):
    id_attributes = ['class',
                     'type',
                     'id']

    relation_attributes = ['attributes',
                           'inputs',
                           'outputs']

    @register_events_decorator([PreNodeInitialized, PostNodeInitialized])
    def __init__(self, **kwargs):
        self._id = kwargs.pop('id')

        self._attributes = None
        self._inputs = None
        self._outputs = None

    @register_events_decorator([PreNodeDeleted, PostNodeDeleted])
    def delete(self):
        from backend.meta import InstanceManager
        InstanceManager().remove_instance(self)

        del self

    def get_class(self, serialize=False):
        if serialize:
            return self.__class__.__name__

        return self.__class__

    def get_type(self, serialize=False):
        return self.entity_type.value

    def get_id(self, serialize=False):
        return self._id

    @property
    def attributes(self):
        return self.get_attributes()

    def get_attributes(self, serialize=False):
        if serialize:
            return self._attributes.serialize()

        return self._attributes

    def set_attributes(self, attributes):
        if not self.validate_attributes(attributes):
            return False

        self._attributes = attributes
        return True

    def del_attributes(self):
        self._attributes.clear()

    def validate_attributes(self, attributes):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    def deserialize_attributes(self, data):
        return self._attributes.deserialize(data, relations=True)

    @property
    def inputs(self):
        return self.get_inputs()

    def get_inputs(self, serialize=False):
        if serialize:
            return self._inputs.serialize()

        return self._inputs

    def set_inputs(self, inputs):
        if not self.validate_inputs(inputs):
            return False

        self._inputs = inputs
        return True

    def del_inputs(self):
        self._inputs.clear()

    def validate_inputs(self, inputs):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    def deserialize_inputs(self, data):
        return self._inputs.deserialize(data, relations=True)

    @property
    def outputs(self):
        return self.get_outputs()

    def get_outputs(self, serialize=False):
        if serialize:
            return self._outputs.serialize()

        return self._outputs

    def set_outputs(self, outputs):
        if not self.validate_outputs(outputs):
            return False

        self._outputs = outputs
        return True

    def del_outputs(self):
        self._outputs.clear()

    def validate_outputs(self, outputs):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    def deserialize_outputs(self, data):
        return self._outputs.deserialize(data, relations=True)

    def data(self):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')


class BaseNodeCollection(EntitySerializer, TypedDictCollection):
    id_attributes = ['class'
                     ]

    primary_attributes = ['parent']

    relation_attributes = ['parent',
                           'entries'
                           ]

    def validate_parent(self, parent):
        if not isinstance(parent, BaseGraph):
            logger.warn(f'{parent} is not an instance of {BaseGraph}')

        return True

    @classmethod
    def deserialize_parent(cls, id_):
        from backend.meta import InstanceManager
        return InstanceManager().get_instance(id_)

    def validate_entries(self):
        return True

    @classmethod
    def deserialize_entries(cls, ids):
        entries = []
        from backend.meta import InstanceManager

        for id_ in ids:
            instance = InstanceManager().get_instance(id_)
            if instance:
                entries.append(instance)

        return entries
