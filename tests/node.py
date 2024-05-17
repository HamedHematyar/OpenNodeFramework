from core.concrete import *

if __name__ == '__main__':
    node = ParameterNode()

    print(node.attributes)
    print(node.inputs)
    print(node.outputs)

    print(node.compute(node.outputs[0]))

    node.attributes['value'].set_value(35.5)
    print(node.compute(node.outputs[0]))

    parameter_01 = ParameterNode()
    parameter_01.attributes['value'].set_value(5)

    parameter_02 = ParameterNode()
    parameter_02.attributes['value'].set_value(10)

    sum_node = SumNode()
    print(sum_node.compute(sum_node.outputs[0]))

    sum_node.inputs[0].set_source(parameter_01.outputs[0])
    sum_node.inputs[1].set_source(parameter_02.outputs[0])

    print(sum_node.compute(sum_node.outputs[0]))