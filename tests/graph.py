from backend.concrete import *


if __name__ == '__main__':
    graph = Graph('main')

    graph.create_node(ParameterNode)
    graph.create_node(ParameterNode)
    graph.create_node(SumNode)

    graph_serializer = GraphSerializer()
