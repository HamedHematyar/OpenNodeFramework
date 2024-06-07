from backend.bases import (BaseAttributeCollection,
                           BasePortCollection,
                           BaseNodeCollection,
                           BaseGraphCollection)


class AttributeCollection(BaseAttributeCollection):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class PortCollection(BasePortCollection):
    def __init__(self):
        super().__init__()


class NodeCollection(BaseNodeCollection):
    def __init__(self):
        super().__init__()


class GraphCollection(BaseGraphCollection):
    def __init__(self):
        super().__init__()
