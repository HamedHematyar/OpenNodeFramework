from backend.bases import (EntitySerializer,
                           TypedDictCollection,
                           BaseAttributeNode,
                           BasePortNode,
                           BaseType,
                           BaseNode)


class CustomDictCollection(EntitySerializer, TypedDictCollection):
    id_attributes = ['class',
                     ]

    relation_attributes = ['items']


class TypeCollection(CustomDictCollection):
    valid_types = (BaseType,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AttributeCollection(CustomDictCollection):
    valid_types = (BaseAttributeNode,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class PortCollection(CustomDictCollection):
    valid_types = (BasePortNode,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class PortAttributesCollection(CustomDictCollection):
    valid_types = (BaseType, PortCollection)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class NodeCollection(CustomDictCollection):
    valid_types = (BaseNode,)

    def __init__(self):
        super().__init__()
