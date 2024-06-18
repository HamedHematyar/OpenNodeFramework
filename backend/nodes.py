from backend.bases import BaseNode, PortType
from backend.attributes import DataTypeEnum, GenericInt
from backend.aggregations import AttributeCollection, PortCollection
from backend.ports import OutputPort, InputPort
from backend.events import *


class Node(BaseNode):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_attributes(AttributeCollection())
        self.set_inputs(PortCollection())
        self.set_outputs(PortCollection())


class ParameterNode(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_attributes(AttributeCollection())
        self.set_inputs(PortCollection())
        self.set_outputs(PortCollection())

        self.attributes.append(DataTypeEnum(name='type'))
        self.attributes.append(GenericInt(name='value', value=int()))

        self.outputs.append(OutputPort(name='product', mode=PortType.OUTPUT))

    def data(self) -> t.Optional[t.Any]:
        return self.attributes['value'].value


class SumNode(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_attributes(AttributeCollection())
        self.set_inputs(PortCollection())
        self.set_outputs(PortCollection())

        self.inputs.append(InputPort(name='entry0', mode=PortType.INPUT))
        self.inputs.append(InputPort(name='entry1', mode=PortType.INPUT))

        self.outputs.append(OutputPort(name='product', mode=PortType.OUTPUT))

    def data(self) -> t.Optional[t.Any]:
        data = 0

        for input_port in self.inputs:
            data += input_port.data(0)

        return data

