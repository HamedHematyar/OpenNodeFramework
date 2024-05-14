from core.abstract import node
from core.base import attribute


class Node(node.AbstractNode):
    def __init__(self) -> None:
        """
        Implement the base class of AbstractNode.
        """
        self.attributes: attribute.AttributeCollection = attribute.AttributeCollection()
