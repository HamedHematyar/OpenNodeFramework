import typing as t

from backend.registry import register_collection
from backend.bases import (CustomDictCollection,
                           BaseAttributeNode,
                           BasePortNode,
                           BaseType,
                           BaseNode)


@register_collection
class DataTypeCollection(CustomDictCollection):
    valid_types = (BaseType,)

    @classmethod
    def _decode(cls, data: t.Dict[str, t.Any], relations=False) -> t.Any:
        from backend.registry import RegisteredTypes

        # remove class to avoid issues with dict constructor
        data.pop('class')

        for name, item_data in data.items():
            data[name] = RegisteredTypes[item_data['class']].deserialize(item_data, relations=relations)

        return cls(**data)


@register_collection
class AttributeCollection(CustomDictCollection):
    valid_types = (BaseAttributeNode,)

    @classmethod
    def _decode(cls, data: t.Dict[str, t.Any], relations=False) -> t.Any:
        from backend.registry import RegisteredTypes, RegisteredAttributes

        # remove class to avoid issues with dict constructor
        data.pop('class')

        for name, item_data in data.items():
            subclass = RegisteredTypes.get(item_data['class']) or RegisteredAttributes.get(item_data['class'])
            data[name] = subclass.deserialize(item_data, relations=True)

        return cls(**data)


@register_collection
class PortCollection(CustomDictCollection):
    valid_types = (BasePortNode,)

    @classmethod
    def _decode(cls, data: t.Dict[str, t.Any], relations=False) -> t.Any:
        from backend.registry import RegisteredTypes, RegisteredPorts

        # remove class to avoid issues with dict constructor
        data.pop('class')

        for name, item_data in data.items():
            subclass = RegisteredTypes.get(data['class']) or RegisteredPorts.get(item_data['class'])
            data[name] = subclass.deserialize(item_data, relations=True)

        return cls(**data)


@register_collection
class NodeCollection(CustomDictCollection):
    valid_types = (BaseNode,)
