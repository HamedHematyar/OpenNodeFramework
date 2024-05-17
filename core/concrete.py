import typing as t

from core.base import (BaseNode,
                       BaseAttribute,
                       BasePort,
                       BaseAttributeSerializer,
                       BaseAttributeCollection,
                       BaseAttributeCollectionSerializer)


class StringAttribute(BaseAttribute):
    def __init__(self, name, value):
        super().__init__(name, value)

    def set_value(self, value) -> bool:
        if not isinstance(value, str):
            raise TypeError(f'attribute value must be a str.')

        return super().set_value(value)


class IntAttribute(BaseAttribute):
    def __init__(self, name, value):
        super().__init__(name, value)

    def set_value(self, value) -> bool:
        if not isinstance(value, int):
            raise TypeError(f'attribute value must be a int.')

        return super().set_value(value)


class ListAttribute(BaseAttribute):
    def __init__(self, name, value):
        super().__init__(name, value)

    def set_value(self, value) -> bool:
        if not isinstance(value, list):
            raise TypeError(f'attribute value must be a list.')

        return super().set_value(value)


class NameAttribute(StringAttribute):
    """
    >>> NameAttribute(value='test')
    {'name': 'name', 'value': 'test'}
    """

    def __init__(self, name, value):
        super().__init__('name', value)


class AttributeCollection(BaseAttributeCollection):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AttributeSerializer(BaseAttributeSerializer):

    def serialize(self, attr: BaseAttribute) -> t.Dict[str, t.Any]:
        return {'type': attr.__class__.__name__,
                'name': attr.get_name(),
                'value': attr.get_value()}

    def deserialize(self, attr_data: t.Dict[str, t.Any]) -> BaseAttribute:
        subclass_mapping = {subclass.__name__: subclass for subclass in BaseAttribute.__subclasses__()}
        return subclass_mapping[attr_data.pop('type')](**attr_data)


class AttributeCollectionSerializer(BaseAttributeCollectionSerializer):
    def serialize(self, collection_instance: AttributeCollection) -> t.Dict[str, t.Any]:
        data = {}
        for key, attr in collection_instance.items():
            serialized_attr = BaseAttributeSerializer().serialize(attr)
            data.update({key: serialized_attr})

        return data

    def deserialize(self, collection_data: t.Dict[str, t.Any]) -> AttributeCollection:
        collection = AttributeCollection()
        for key, attribute_data in collection_data.items():
            attribute_serializer = BaseAttributeSerializer()
            deserialized_attr = attribute_serializer.deserialize(attribute_data)

            collection.add(deserialized_attr)

        return collection


class NullNode(BaseNode):
    def __init__(self):
        super().__init__()


class ParameterNode(BaseNode):
    def __init__(self):
        super().__init__()

        self.attributes.add(ListAttribute('type', [int, float]))
        self.attributes.add(IntAttribute('value', int()))

        self.output_port = OutPort('output', self)

        self.inputs = []
        self.outputs = [self.output_port,
                        ]

    def _compute_output_port(self):
        value_attr: BaseAttribute = self.attributes['value']
        return value_attr.get_value()

    def compute(self, output):
        return getattr(self, f'_compute_{output.get_name()}_port')()


class SumNode(BaseNode):
    def __init__(self):
        super().__init__()

        self.attributes.add(StringAttribute('type', [int, float]))
        self.attributes.add(StringAttribute('value', int()))

        self.first_entry_port = InPort('first_entry', None)
        self.second_entry_port = InPort('second_entry', None)

        self.output_port = OutPort('output', self)

        self.inputs = [self.first_entry_port,
                       self.second_entry_port]

        self.outputs = [self.output_port,
                        ]

    def _compute_output_port(self):
        first_entry_source = self.first_entry_port.get_source()
        if not first_entry_source:
            return

        second_entry_source = self.second_entry_port.get_source()
        if not second_entry_source:
            return

        return first_entry_source.compute(self.first_entry_port) + second_entry_source.compute(self.second_entry_port)

    def compute(self, output):
        return getattr(self, f'_compute_{output.get_name()}_port')()


class InPort(BasePort):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._source = None

    def get_source(self):
        return self._source

    def set_source(self, source):
        self._source = source


class OutPort(BasePort):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._destination = None

    def get_destination(self):
        self._destination = self._destination

    def set_destination(self, destination):
        self._destination = destination
