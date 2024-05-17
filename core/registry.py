from core.concrete.node import *
from core.concrete.attribute import *

Nodes = {cls.__name__: cls for cls in [NullNode,
                                       ParameterNode]}

Attributes = {cls.__name__: cls for cls in [StringAttribute,
                                            ]}
