from core.concrete import *

if __name__ == '__main__':
    node = ParameterNode()

    print(node.attributes)
    print(node.inputs)
    print(node.outputs)

    print(node.compute_output(node.outputs[0]))

    node.attributes['value'].value = 35.5
    print(node.compute_output(node.outputs[0]))

    parameter_01 = ParameterNode()
    parameter_01.attributes['value'].value = 5

    parameter_02 = ParameterNode()
    parameter_02.attributes['value'].value = 10

    sum_node = SumNode()
    print(sum_node.compute_output(sum_node.outputs[0]))

    param01_connection = Connection(parameter_01.outputs[0], sum_node.inputs[0])
    param02_connection = Connection(parameter_02.outputs[0], sum_node.inputs[1])

    print(sum_node.compute_output(sum_node.outputs[0]))
