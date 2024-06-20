from backend.bases import BaseNode, PortType
from backend.attributes import GenericAttribute
from backend.aggregations import AttributeCollection, PortCollection
from backend.ports import OutputPort, InputPort
from backend.events import *


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


class ParameterNode(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_attributes(AttributeCollection())
        self.set_inputs(PortCollection())
        self.set_outputs(PortCollection())

        self.attributes['type'] = GenericAttribute()
        self.attributes['value'] = GenericAttribute()

        self.outputs['product'] = OutputPort()

    def data(self) -> t.Optional[t.Any]:
        return self.attributes['value'].value


class SumNode(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_attributes(AttributeCollection())
        self.set_inputs(PortCollection())
        self.set_outputs(PortCollection())

        self.inputs['entry0'] = InputPort()
        self.inputs['entry1'] = InputPort()

        self.outputs['product'] = OutputPort()

    def data(self) -> t.Optional[t.Any]:
        data = 0

        for input_port in self.inputs:
            data += input_port.data(0)

        return data

