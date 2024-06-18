from backend.bases import (BaseAttributeCollection,
                           BasePortCollection,
                           BaseNodeCollection,
                           BaseGraphCollection,
                           BasePort,
                           BaseAttribute,
                           BaseNode,
                           BaseGraph)


class AttributeCollection(BaseAttributeCollection):
    valid_types = (BaseAttribute, )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class PortCollection(BasePortCollection):
    valid_types = (BasePort, )

    def __init__(self):
        super().__init__()


class NodeCollection(BaseNodeCollection):
    valid_types = (BaseNode, )

    def __init__(self):
        super().__init__()


class GraphCollection(BaseGraphCollection):
    valid_types = (BaseGraph, )

    def __init__(self):
        super().__init__()
