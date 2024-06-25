from backend.registry import register_port
from backend.data_types import ReferencedNode, GenericStr, PortModeEnum, ReferencedPortList
from backend.bases import BasePortNode
from backend.aggregations import DataTypeCollection


class GenericPort(BasePortNode):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        attributes = kwargs.pop('attributes', {})
        self.set_attributes(attributes or self.init_attributes())

        self.populate_data(**kwargs)

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
        from backend.registry import RegisteredCollections
        return {'attributes': RegisteredCollections[data['class']].deserialize(data, relations=True)}

    def data(self):
        return


@register_port
class InputPort(GenericPort):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.attributes['mode'].set_data('INPUT')


@register_port
class OutputPort(GenericPort):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.attributes['mode'].set_data('OUTPUT')
