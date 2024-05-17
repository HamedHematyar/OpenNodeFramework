import typing as t

from core.enums import PortType
from core.base import (BaseNode,
                       BaseAttribute,
                       BasePort,
                       BaseAttributeSerializer,
                       BaseAttributeCollection,
                       BaseAttributeCollectionSerializer,
                       BaseConnection)


class StringAttribute(BaseAttribute):
    def __init__(self, name, value):
        super().__init__(name, value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not isinstance(value, str):
            raise TypeError(f'attribute value must be a str.')

        self.__value = value


class IntAttribute(BaseAttribute):
    def __init__(self, name, value):
        super().__init__(name, value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f'attribute value must be a int.')

        self.__value = value


class ListAttribute(BaseAttribute):
    def __init__(self, name, value):
        super().__init__(name, value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not isinstance(value, list):
            raise TypeError(f'attribute value must be a list.')

        self.__value = value


class TypeAttribute(BaseAttribute):
    def __init__(self, name, value):
        super().__init__(name, value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value not in [str,
                         int,
                         list]:
            raise TypeError(f'attribute value is not valid.')

        self.__value = value


class NameAttribute(StringAttribute):
    """
    >>> NameAttribute(value='test')
    {'name': 'name', 'value': 'test'}
    """

    def __init__(self, value):
        super().__init__('name', value)


class AttributeCollection(BaseAttributeCollection):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AttributeSerializer(BaseAttributeSerializer):

    def serialize(self, attr: BaseAttribute) -> t.Dict[str, t.Any]:
        return {'type': attr.__class__.__name__,
                'name': attr.name,
                'value': attr.value}

    def deserialize(self, attr_data: t.Dict[str, t.Any]) -> BaseAttribute:
        subclass_mapping = {subclass.__name__: subclass for subclass in BaseAttribute.__subclasses__()}
        return subclass_mapping[attr_data.pop('type')](*attr_data.values())


class AttributeCollectionSerializer(BaseAttributeCollectionSerializer):
    def serialize(self, collection_instance: AttributeCollection) -> t.Dict[str, t.Any]:
        data = {}
        for key, attr in collection_instance.items():
            serialized_attr = AttributeSerializer().serialize(attr)
            data.update({key: serialized_attr})

        return data

    def deserialize(self, collection_data: t.Dict[str, t.Any]) -> AttributeCollection:
        collection = AttributeCollection()
        for key, attribute_data in collection_data.items():
            attribute_serializer = AttributeSerializer()
            deserialized_attr = attribute_serializer.deserialize(attribute_data)

            collection.add(deserialized_attr)

        return collection


class NullNode(BaseNode):
    def __init__(self):
        super().__init__()


class ParameterNode(BaseNode):
    def __init__(self):
        super().__init__()

        self.attributes.add(TypeAttribute('type', int))
        self.attributes.add(IntAttribute('value', int()))

        self.inputs = []
        self.outputs = [OutPort('output', PortType.Out, self),
                        ]

    def compute_data(self) -> t.Optional[t.Any]:
        return self.attributes['value'].value

    def _compute_output_port(self):
        return self.compute_data()


class SumNode(BaseNode):
    def __init__(self):
        super().__init__()

        self.inputs = [InPort('left', PortType.In, self),
                       InPort('right', PortType.In, self)]

        self.outputs = [OutPort('output', PortType.Out, self),
                        ]

    def compute_data(self) -> t.Optional[t.Any]:
        data = 0
        if self.inputs[0].is_connected():
            data += self.inputs[0].connection.source.node.compute_output(self.inputs[0].connection.source)

        if self.inputs[1].is_connected():
            data += self.inputs[1].connection.source.node.compute_output(self.inputs[1].connection.source)

        return data

    def _compute_output_port(self):
        return self.compute_data()


class InPort(BasePort):
    def __init__(self, name, port_type, node):
        super().__init__(name, port_type, node)


class OutPort(BasePort):
    def __init__(self, name, port_type, node):
        super().__init__(name, port_type, node)


class Connection(BaseConnection):
    def __init__(self, source, destination):
        super().__init__(source, destination)
