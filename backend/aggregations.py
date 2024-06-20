from backend.bases import (EntitySerializer,
                           TypedListCollection,
                           BasePortCollection,
                           BaseNodeCollection,
                           BaseGraphCollection,
                           BaseAttributeNode,
                           BasePort,
                           BaseType,
                           BaseNode,
                           BaseGraph)


class CustomListCollection(EntitySerializer, TypedListCollection):

    id_attributes = ['class',
                     ]

    relation_attributes = ['items']


class TypeCollection(CustomListCollection):
    valid_types = (BaseType, )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AttributeCollection(CustomListCollection):
    valid_types = (BaseAttributeNode, )

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
