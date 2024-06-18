import json
import enum

from backend.abstracts import (AbstractAttribute,
                               AbstractNode,
                               AbstractPort,
                               AbstractGraph,
                               AbstractListCollection,
                               AbstractEntitySerializer)
from backend.events import *
from backend.validators import *


class EntitySerializer(AbstractEntitySerializer):

    def serialize(self) -> t.Dict[str, t.Any]:
        return self._encode()

    @classmethod
    def deserialize(cls, data: t.Dict[str, t.Any], *args, **kwargs) -> t.Any:
        return cls._decode(data, *args, **kwargs)

    def dump(self, obj, file_path, *args, **kwargs):
        with open(file_path, 'w') as file:
            json.dump(obj, file, default=self._encode, *args, **kwargs)

    def dumps(self, **kwargs):
        return json.dumps(self._encode(), **kwargs)

    def load(self, file_path, *args, **kwargs):
        with open(file_path, 'r') as file:
            return self._decode(json.load(file, *args, **kwargs))

    def _encode(self) -> t.Dict[str, t.Any]:
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


class ListCollection(AbstractListCollection):
    def __init__(self, **kwargs):
        super().__init__()

        self._internal_data = []
        self._parent: t.Optional[BaseNode] = None

    def __len__(self):
        return len(self._internal_data)

    def __getitem__(self, idx):
        return self._internal_data[idx]

    def __setitem__(self, idx, value):
        if self.validate_item(idx, value):
            value.set_parent(self)
            self._internal_data[idx] = value

    def __delitem__(self, idx):
        del self._internal_data[idx]

    def __repr__(self):
        return str(self._internal_data)

    def insert(self, idx, value):
        if self.validate_item(idx, value):

            value.set_parent(self)
            self._internal_data.insert(idx, value)

    def get_class(self, serialize=False):
        if serialize:
            return self.__class__.__name__

        return self.__class__

    @property
    def parent(self):
        return self.get_parent()

    def get_parent(self, serialize=False):
        if not self._parent:
            return

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

    @property
    def entries(self):
        return self.get_entries()

    def get_entries(self, serialize=False):
        if serialize:
            return [entry.get_id() for entry in self]

        return self

    def set_entries(self, entries: t.Iterable):
        self.extend(entries)

        return True

    def del_entries(self):
        self.clear()

    def validate_entries(self):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    def validate_parent(self, parent):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    def validate_item(self, index, item):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')


class TypedListCollection(ListCollection):
    valid_types = tuple()

    def validate_item(self, index, item):
        if not isinstance(item, self.valid_types):
            logger.warn(f'item value must be of type {self.valid_types}')
            return False

        if item in self:
            logger.warn(f'{index}:{item} is already present in the collection')
            return False

        return True


class BaseAttribute(EntitySerializer, AbstractAttribute):
    """
    A base attribute class that implements AbstractAttribute.
    """
    id_attributes = ['class',
                     'type',
                     'id']

    primary_attributes = ['name',
                          'value',
                          'parent',
                          'link']

    relation_attributes = ['parent',
                           'link']

    @register_events_decorator([PreAttributeInitialized, PostAttributeInitialized])
    def __init__(self, **kwargs):
        self._id = kwargs.pop('id')

        self._name: t.Optional[str] = None
        self._link: t.Optional[BaseAttribute] = None
        self._parent: t.Optional[BaseNode] = None
        self._value: t.Optional[t.Any] = None

        for key in self.primary_attributes:
            if key in kwargs:
                getattr(self, f'set_{key}')(kwargs[key])

    @register_events_decorator([PreAttributeDeleted, PostAttributeDeleted])
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
        return attribute_name_validator(self, name)

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
        if not isinstance(parent, BaseAttributeCollection):
            logger.warn(f'parent {parent} is not an instance of {BaseNode}')
            return False

        return True

    @property
    def link(self):
        return self.get_link()

    def get_link(self, serialize=False):
        if not self._link:
            return

        if serialize:
            return self._link.get_id()

        return self._link

    @register_events_decorator([PreAttributeLinked, PostAttributeLinked])
    def set_link(self, link: 'BaseAttribute'):
        if not self.validate_link(link):
            return False

        self._link = link
        return True

    @register_events_decorator([PreAttributeUnlinked, PostAttributeUnlinked])
    def del_link(self):
        self._link = None

    def validate_link(self, link):
        if not isinstance(link, BaseAttribute):
            logger.warn(f'attribute link {link} is not an instance of {BaseAttribute}')
            return False

        return True

    @classmethod
    def deserialize_link(cls, id_):
        from backend.meta import InstanceManager
        return InstanceManager().get_instance(id_)

    @property
    def value(self):
        return self.get_value()

    def get_value(self, serialize=False):
        if self.get_link() is None:
            return self._value
        else:
            return self.get_link().get_value()

    @register_events_decorator([PreAttributeValueChanged, PostAttributeValueChanged])
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


class BaseAttributeCollection(EntitySerializer, TypedListCollection):

    id_attributes = ['class',
                     ]

    primary_attributes = ['parent',
                          ]

    relation_attributes = ['parent',
                           'entries']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        for key in self.primary_attributes:
            if key in kwargs:
                getattr(self, f'set_{key}')(kwargs[key])

    def validate_parent(self, parent):
        if not isinstance(parent, BaseNode):
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

    def set_id(self, _id):
        self._id = _id

    def del_id(self):
        self._id = None

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
        self._connections.set_parent(self)
        return True

    def del_connections(self):
        self._connections = None

    def validate_connections(self, connections):
        return True

    def deserialize_connections(self, data):
        return self._connections.deserialize(data)

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


class BasePortCollection(EntitySerializer, TypedListCollection):
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


class BaseNode(EntitySerializer, AbstractNode):
    id_attributes = ['class',
                     'type',
                     'id']

    primary_attributes = ['name',
                          'parent',
                          'attributes',
                          'inputs',
                          'outputs']

    relation_attributes = ['parent',
                           'attributes',
                           'inputs',
                           'outputs']

    @register_events_decorator([PreNodeInitialized, PostNodeInitialized])
    def __init__(self, **kwargs):
        self._id = kwargs.pop('id')

        self._name: t.Optional[str] = None
        self._parent: t.Optional[BaseNode] = None
        self._attributes: t.Optional[BaseAttributeCollection] = None
        self._inputs: t.Optional[BasePortCollection] = None
        self._outputs: t.Optional[BasePortCollection] = None

        for key in self.primary_attributes:
            if key in kwargs:
                getattr(self, f'set_{key}')(kwargs[key])

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

    def set_id(self, _id):
        self._id = _id

    def del_id(self):
        self._id = None

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
        return node_name_validator(self, name)

    @property
    def parent(self):
        return self.get_parent()

    def get_parent(self, serialize=False):
        if not self._parent:
            return

        if serialize:
            return self._parent.get_id()

        return self._parent

    def set_parent(self, parent: 'BaseGraph'):
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
        if not isinstance(parent, (BaseNodeCollection, BaseGraph)):
            logger.warn(f'parent {parent} is not an instance of {BaseGraph}')
            return False

        return True

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
        self._attributes.set_parent(self)
        return True

    def del_attributes(self):
        self._attributes.clear()

    def validate_attributes(self, attributes):
        if not isinstance(attributes, BaseAttributeCollection):
            logger.warn(f'{attributes} is not an instance of {BaseAttributeCollection}')
            return False

        return True

    def deserialize_attributes(self, data):
        return self._attributes.deserialize(data)

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
        self._inputs.set_parent(self)
        return True

    def del_inputs(self):
        self._inputs.clear()

    def validate_inputs(self, inputs):
        if not isinstance(inputs, BasePortCollection):
            logger.warn(f'{inputs} is not an instance of {BasePortCollection}')
            return False

        return True

    def deserialize_inputs(self, data):
        return self._inputs.deserialize(data)

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
        self._outputs.set_parent(self)
        return True

    def del_outputs(self):
        self._outputs.clear()

    def validate_outputs(self, outputs):
        if not isinstance(outputs, BasePortCollection):
            logger.warn(f'{outputs} is not an instance of {BasePortCollection}')
            return False

        return True

    def deserialize_outputs(self, data):
        return self._outputs.deserialize(data)

    def data(self) -> t.Optional[t.Any]:
        return


class BaseNodeCollection(EntitySerializer, TypedListCollection):
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


class BaseGraph(EntitySerializer, AbstractGraph):

    @register_events_decorator([PreGraphInitialized, PostGraphInitialized])
    def __init__(self):
        self._name: t.Optional[str] = None
        self.__parent = None
        self.__nodes = None
        self._graphs = None

    @register_events_decorator([PreGraphDeleted, PostGraphDeleted])
    def delete(self):
        from backend.meta import InstanceManager
        InstanceManager().remove_instance(self)

        del self

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: t.Optional[str]):
        if not isinstance(value, str):
            raise TypeError(f'{value} is not an instance of {str}')

        self._name = value

    @property
    def parent(self):
        return self._name

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
        return self._graphs

    @graphs.setter
    def graphs(self, value):
        if not isinstance(value, BaseGraphCollection):
            raise TypeError(f'{value} is not an instance of {list}')

        value.parent = self
        self._graphs = value


class BaseGraphCollection(TypedListCollection):
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
