from backend.bases import (BaseAttributeCollection,
                           BasePortCollection,
                           BaseNodeCollection,
                           BaseGraphCollection,
                           BasePort)


class AttributeCollection(BaseAttributeCollection):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class PortCollection(BasePortCollection):
    valid_types = (BasePort, )

    def __init__(self):
        super().__init__()


class NodeCollection(BaseNodeCollection):
    def __init__(self):
        super().__init__()


class GraphCollection(BaseGraphCollection):
    def __init__(self):
        super().__init__()
