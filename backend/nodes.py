from backend.registry import register_node
from backend.bases import BaseNode
from backend.attributes import StringAttribute, IntAttribute
from backend.aggregations import AttributeCollection, PortCollection
from backend.ports import InputPort, OutputPort
from backend.events import *


@register_node
class Node(BaseNode):

    def init_attributes(self):
        return AttributeCollection()

    def init_inputs(self):
        return PortCollection()

    def init_outputs(self):
        return PortCollection()

    def validate_attributes(self, attributes):
        return True

    def validate_inputs(self, inputs):
        return True

    def validate_outputs(self, outputs):
        return True


@register_node
class ParameterNode(Node):

    def init_attributes(self):
        collection = AttributeCollection()

        collection['value'] = IntAttribute(parent=self)

        return collection

    def init_inputs(self):
        collection = PortCollection()

        return collection

    def init_outputs(self):
        collection = PortCollection()

        collection['product'] = OutputPort(parent=self)

        return collection

    def data(self) -> t.Optional[t.Any]:
        return self.attributes['value'].data()


@register_node
class SumNode(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_attributes(AttributeCollection())
        self.set_inputs(PortCollection())
        self.set_outputs(PortCollection())

        self.inputs['entry0'] = InputPort(parent=self)
        self.inputs['entry1'] = InputPort(parent=self)

        self.outputs['product'] = OutputPort(parent=self)

    def data(self) -> t.Optional[t.Any]:
        data = 0

        for input_name, input_port in self.inputs.items():
            data += input_port.data()

        return data

