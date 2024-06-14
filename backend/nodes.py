from backend.enums import PortType
from backend.bases import BaseNode
from backend.attributes import DataTypeEnum, GenericInt
from backend.aggregations import AttributeCollection, PortCollection
from backend.ports import OutputPort, InputPort
from backend.events import *


class Node(BaseNode):
    def __init__(self):
        super().__init__()

        self.attributes = AttributeCollection()
        self.inputs = PortCollection()
        self.outputs = PortCollection()


class ParameterNode(Node):
    def __init__(self):
        super().__init__()

        self.attributes = AttributeCollection()
        self.inputs = PortCollection()
        self.outputs = PortCollection()

        self.attributes.add(DataTypeEnum(name='type'))
        self.attributes.add(GenericInt(name='value', value=int()))

        self.outputs.append(OutputPort().initialize('product', PortType.Output))

    def data(self) -> t.Optional[t.Any]:
        return self.attributes['value'].value


class SumNode(Node):
    def __init__(self):
        super().__init__()

        self.attributes = AttributeCollection()
        self.inputs = PortCollection()
        self.outputs = PortCollection()

        self.inputs.append(InputPort().initialize('entry0', PortType.Input))
        self.inputs.append(InputPort().initialize('entry1', PortType.Input))

        self.outputs.append(OutputPort().initialize('product', PortType.Output))

    def data(self) -> t.Optional[t.Any]:
        data = 0

        for input_port in self.inputs:
            data += input_port.data(0)

        return data

