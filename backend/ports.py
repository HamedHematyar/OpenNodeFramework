import typing as t

from backend.registry import register_port
from backend.data_types import ReferencedNode, GenericStr, PortModeEnum, ReferencedPortList
from backend.bases import BasePortNode
from backend.aggregations import DataTypeCollection


class GenericPort(BasePortNode):

    def init_attributes(self):
        collection = DataTypeCollection()

        collection['parent'] = ReferencedNode()
        collection['label'] = GenericStr()
        collection['mode'] = PortModeEnum()
        collection['connections'] = ReferencedPortList()

        return collection

    def populate_data(self, **kwargs):
        for key, value in kwargs.items():
            if self.attributes.get(key):
                self.attributes[key].set_data(value)

    def validate_attributes(self, attributes):
        return True

    @classmethod
    def deserialize_attributes(cls, data):
        from backend import registry
        subclass: t.Optional[t.Type[DataTypeCollection]] = registry.registered_type(registry.Category.COLLECTION,
                                                                                    data['class'])
        return {'attributes': subclass.deserialize(data)}


@register_port
class InputPort(GenericPort):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.attributes['mode'].set_data('INPUT')

    def data(self):
        data = 0
        for connection in self.attributes['connections'].data():
            from backend.meta import InstanceManager
            connected_port = InstanceManager().get_instance(connection)
            data += connected_port.data()

        return data


@register_port
class OutputPort(GenericPort):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.attributes['mode'].set_data('OUTPUT')

    def data(self):
        from backend.meta import InstanceManager

        node = InstanceManager().get_instance(self.attributes['parent'].data())

        return node.data()