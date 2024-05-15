from core.abstract import node
from core.base.attribute import *


class Node(node.AbstractNode):
    def __init__(self) -> None:
        """
        Implement the base class of AbstractNode.
        """
        self.attributes: AttributeCollection = AttributeCollection()
