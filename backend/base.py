import typing as t

from collections.abc import MutableMapping

from backend.abstract import (AbstractAttribute,
                              AbstractNode,
                              AbstractPort,
                              PortType,
                              AbstractAttributeSerializer,
                              AbstractAttributeCollectionSerializer,
                              AbstractConnection,
                              AbstractGraph,
                              AbstractGraphSerializer,
                              AbstractNodeSerializer)


class BaseAttribute(AbstractAttribute):
    """
    A concrete attribute class that implements AbstractAttribute.
    """

    def __init__(self, name, value):
        self.__name: t.Optional[str] = None
        self.__value: t.Optional[t.Any] = None

        self.name = name
        self.value = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError(f'attribute name must be a string.')

        self.__name = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


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
        self.update(**{attribute.name: attribute})


class BaseNode(AbstractNode):
    def __init__(self):
        """
        Implement the base class of AbstractNode.
        """
        self.attributes: BaseAttributeCollection = BaseAttributeCollection()
        self.inputs: t.List[AbstractPort] = []
        self.outputs: t.List[AbstractPort] = []

    def compute_data(self) -> t.Optional[t.Any]:
        return

    def compute_output(self, output_port: AbstractPort) -> t.Optional[t.Any]:
        return getattr(self, f'_compute_{output_port.name}_port')()


class BasePort(AbstractPort):
    def __init__(self, name: str, port_type: PortType, node: AbstractNode):
        self.__name: t.Optional[str] = None
        self.__port_type: t.Optional[PortType] = None
        self.__node: t.Optional[BaseNode] = None
        self.__connection: t.Optional[BaseConnection] = None

        self.name = name
        self.port_type = port_type
        self.node = node

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        if not isinstance(name, str):
            raise TypeError(f'port name must be a string.')

        self.__name = name

    @property
    def port_type(self) -> PortType | None:
        return self.__port_type

    @port_type.setter
    def port_type(self, port_type: PortType):
        if not isinstance(port_type, PortType):
            raise TypeError(f'port type must be a PortType.')

        self.__port_type = port_type

    @property
    def node(self) -> t.Optional[BaseNode]:
        return self.__node

    @node.setter
    def node(self, node: BaseNode):
        if not isinstance(node, BaseNode):
            raise TypeError(f'node must be an instance of {type(BaseNode)}.')

        self.__node = node

    @property
    def connection(self) -> t.Optional['BaseConnection']:
        return self.__connection

    @connection.setter
    def connection(self, connection):
        if not isinstance(connection, BaseConnection):
            raise TypeError(f'connection must be an instance of {BaseConnection}.')

        self.__connection = connection

    def disconnect(self):
        self.__connection = None

    def is_connected(self):
        return bool(self.connection)


class BaseConnection(AbstractConnection):
    def __init__(self, source: BasePort, destination: BasePort):
        self.__source: t.Optional[BasePort] = None
        self.__destination: t.Optional[BasePort] = None

        self.source = source
        self.destination = destination

    @property
    def source(self) -> t.Optional[BasePort]:
        return self.__source

    @source.setter
    def source(self, source: t.Optional[BasePort]):
        if not isinstance(source, (type(None), BasePort)):
            raise TypeError(f'source must be an instance of {BasePort}.')

        self.__source = source
        self.__source.connection = self

    @property
    def destination(self) -> t.Optional[BasePort]:
        return self.__destination

    @destination.setter
    def destination(self, destination: t.Optional[BasePort]):
        if not isinstance(destination, (type(None), BasePort)):
            raise TypeError(f'destination must be an instance of {BasePort}.')

        self.__destination = destination
        self.__destination.connection = self

    def __del__(self):
        if self.source:
            self.source.disconnect()

        if self.destination:
            self.destination.disconnect()

        self.__destination = None
        self.__source = None

        super().__del__()


class BaseAttributeSerializer(AbstractAttributeSerializer):

    def serialize(self, attr: BaseAttribute) -> t.Dict[str, t.Any]:
        return {'type': attr.__class__.__name__,
                'name': attr.name,
                'value': attr.value}

    def deserialize(self, attr_data: t.Dict[str, t.Any]) -> BaseAttribute:
        raise NotImplementedError('this method is not implemented in subclass.')


class BaseAttributeCollectionSerializer(AbstractAttributeCollectionSerializer):
    def serialize(self, collection_instance: BaseAttributeCollection) -> t.Dict[str, t.Any]:
        raise NotImplementedError('this method is not implemented in subclass.')

    def deserialize(self, collection_data: t.Dict[str, t.Any]) -> BaseAttributeCollection:
        raise NotImplementedError('this method is not implemented in subclass.')


class BaseGraph(AbstractGraph):
    def __init__(self, name: str):
        self.__name: t.Optional[str] = None

        self.name = name
        self._nodes: t.List[BaseNode] = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: t.Optional[str]):
        if not isinstance(value, str):
            raise TypeError(f'attribute name must be a string.')

        self.__name = value

    def clear(self):
        self._nodes.clear()

    def create_node(self, node_class: t.Type[BaseNode]):
        self._nodes.append(node_class())

    def remove_node(self, node: BaseNode):
        self._nodes.remove(node)


class BaseGraphSerializer(AbstractGraphSerializer):
    def serialize(self, graph_instance: BaseGraph) -> t.Dict[str, t.Any]:
        pass

    def deserialize(self, graph_data: t.Dict[str, t.Any]) -> BaseGraph:
        pass


class BaseNodeSerializer(AbstractNodeSerializer):
    def serialize(self, node_instance: BaseNode) -> t.Dict[str, t.Any]:

        attributes = []
        attribute_serializer = BaseAttributeSerializer()

        for name, attr in node_instance.attributes.items():
            attributes.append(attribute_serializer.serialize(attr))

        return {'type': node_instance.__class__.__name__,
                'attributes': attributes,
                'inputs': {},
                'outputs': {}}

    def deserialize(self, node_data: t.Dict[str, t.Any]) -> BaseNode:
        pass


