import math

from backend.nodes import *
from backend.data_types import *
from backend.ports import *


# sin_node = Node()
#
# angle = GenericInt().initialize('angle', 30)
# sin_node.attributes.add(angle)
#
# output = OutputPort().initialize('output', PortType.Output)
#
#
# def data(self):
#     return math.sin(math.radians(self.attributes['angle'].value))
#
#
# def _compute_output_port(self):
#     return sin_node.data()
#
#
# sin_node.data = lambda: data(sin_node)
# setattr(sin_node, '_compute_output_port', lambda: _compute_output_port(sin_node))
#
# print(sin_node.data())
#
# print(sin_node.compute_output(output))


# param_1 = ParameterNode(name='constant')
# param_1.attributes['value'].value = 10
#
# param_2 = ParameterNode().initialize('constant')
# param_2.attributes['value'].value = 15
#
# sum_node = SumNode().initialize('SumNode')
#
# sum_node.inputs[0].connect_to(param_1.outputs[0])
# sum_node.inputs[1].connect_to(param_2.outputs[0])
#
# param_1.outputs[0].connect_to(sum_node.inputs[0])
# param_2.outputs[0].connect_to(sum_node.inputs[1])
#
#
# print(sum_node)


# parameter_01 = ParameterNode(name='parameter_01')
# parameter_02 = ParameterNode(name='parameter')
# print(parameter_node.dumps(indent=4))

sum_node = SumNode(name='sum')
print(sum_node.dumps(indent=4))


