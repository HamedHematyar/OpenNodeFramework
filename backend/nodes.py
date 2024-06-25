from backend.registry import register_node
from backend.bases import BaseNode
from backend.attributes import GenericAttribute
from backend.aggregations import AttributeCollection, PortCollection
from backend.ports import InputPort, OutputPort
from backend.events import *


@register_node
class Node(BaseNode):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_attributes(AttributeCollection())
        self.set_inputs(PortCollection())
        self.set_outputs(PortCollection())

    def validate_attributes(self, attributes):
        return True

    def validate_inputs(self, inputs):
        return True

    def validate_outputs(self, outputs):
        return True


@register_node
class ParameterNode(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_attributes(AttributeCollection())
        self.set_inputs(PortCollection())
        self.set_outputs(PortCollection())

        self.attributes['type'] = GenericAttribute(parent=self)
        self.attributes['value'] = GenericAttribute(parent=self)

        self.outputs['product'] = OutputPort(parent=self)

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

        for input_port in self.inputs:
            data += input_port.data(0)

        return data

