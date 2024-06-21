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


class AttributeTypesCollection(CustomDictCollection):
    valid_types = (BaseType, BaseAttributeNode)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AttributeCollection(CustomDictCollection):
    valid_types = (BaseAttributeNode,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def deserialize_items(cls, items_data):
        from backend.registry import RegisteredTypes, RegisteredAttributes

        for name, data in items_data.items():
            subclass = RegisteredTypes.get(data['class']) or RegisteredAttributes.get(data['class'])
            items_data[name] = subclass.deserialize(data, relations=True)

        return items_data


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
