from backend.enums import PortType
from backend.bases import BaseNode
from backend.attributes import TypeAttribute, Integer
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

        self.attributes.add(TypeAttribute().initialize('type', int))
        self.attributes.add(Integer().initialize('value', int()))

        self.outputs.append(OutputPort().initialize('product', PortType.Output))

    def compute_data(self) -> t.Optional[t.Any]:
        return self.attributes['value'].value

    def _compute_output_port(self):
        return self.compute_data()


class SumNode(Node):
    def __init__(self):
        super().__init__()

        self.attributes = AttributeCollection()
        self.inputs = PortCollection()
        self.outputs = PortCollection()

        self.inputs.append(InputPort().initialize('entry0', PortType.Input))
        self.inputs.append(InputPort().initialize('entry1', PortType.Input))

        self.outputs.append(OutputPort().initialize('product', PortType.Output))

    def compute_data(self) -> t.Optional[t.Any]:
        data = 0
        if self.inputs[0].connections.has_connections():
            data += self.inputs[0].connections[0].node.compute_output(self.inputs[0].connections[0])

        if self.inputs[1].connections.has_connections():
            data += self.inputs[1].connections[0].node.compute_output(self.inputs[1].connections[0])

        return data

    def _compute_output_port(self):
        return self.compute_data()
