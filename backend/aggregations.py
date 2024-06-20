from backend.bases import (EntitySerializer,
                           TypedDictCollection,
                           BasePortCollection,
                           BaseNodeCollection,
                           BaseGraphCollection,
                           BaseAttributeNode,
                           BasePort,
                           BaseType,
                           BaseNode,
                           BaseGraph)


class CustomDictCollection(EntitySerializer, TypedDictCollection):

    id_attributes = ['class',
                     ]

    relation_attributes = ['items']


class TypeCollection(CustomDictCollection):
    valid_types = (BaseType, )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AttributeCollection(CustomDictCollection):
    valid_types = (BaseAttributeNode, )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_item_by_name(self, name):
        data = {item.data(): item for item in self}
        item = data.get(name)

        if not item:
            raise KeyError(f'requested item {name} could not be found in the list.')

        return item

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
