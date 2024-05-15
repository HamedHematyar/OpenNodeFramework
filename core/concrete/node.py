from core.base import node
from core.concrete import attribute


class NullNode(node.Node):
    def __init__(self):
        super().__init__()

    def initialize_attributes(self):
        self.attributes.append(attribute.NameAttribute())

