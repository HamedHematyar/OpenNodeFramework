import typing as t

from backend.enums import PortType
from backend.bases import BaseNode
from backend.attributes import TypeAttribute, Integer
from backend.collections import AttributeCollection, PortCollection
from backend.ports import OutPort, InPort


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

        self.attributes.add(TypeAttribute('type', int))
        self.attributes.add(Integer('value', int()))

        self.outputs.append(OutPort('output', PortType.Out))

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

        self.inputs.append(InPort('left', PortType.In))
        self.inputs.append(InPort('right', PortType.In))

        self.outputs.append(OutPort('output', PortType.Out))

    def compute_data(self) -> t.Optional[t.Any]:
        data = 0
        if self.inputs[0].connections.has_connections():
            data += self.inputs[0].connections[0].node.compute_output(self.inputs[0].connections[0])

        if self.inputs[1].connections.has_connections():
            data += self.inputs[1].connections[0].node.compute_output(self.inputs[1].connections[0])

        return data

    def _compute_output_port(self):
        return self.compute_data()
