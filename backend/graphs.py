from backend.bases import BaseGraph
from backend.nodes import Node
from backend.aggregations import NodeCollection, GraphCollection


class Graph(BaseGraph):
    def __init__(self, name: str):
        super().__init__(name)

        self.nodes: NodeCollection[Node] = NodeCollection()
        self.graphs: GraphCollection[Graph] = GraphCollection()
