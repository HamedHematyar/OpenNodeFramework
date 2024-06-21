from backend.nodes import ParameterNode, SumNode, Node
from backend.aggregations import NodeCollection

node_collection = NodeCollection()
print(node_collection)

param_node = ParameterNode(value=5)
node_collection.append(param_node)
print(node_collection)
