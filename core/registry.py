from core.concrete import node
from core.concrete import attribute

Nodes = {cls.__name__: cls for cls in [node.NullNode,
                                       ]}

Attributes = {cls.__name__: cls for cls in [attribute.NameAttribute,
                                            ]}
