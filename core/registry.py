from core.concrete.node import *
from core.concrete.attribute import *

Nodes = {cls.__name__: cls for cls in [NullNode,
                                       ]}

Attributes = {cls.__name__: cls for cls in [StringAttribute,
                                            ]}
