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
    def _decode(cls, data: t.Dict[str, t.Any]) -> t.Any:
        from backend import registry

        # remove class to avoid issues with dict constructor
        data.pop('class')

        for name, item_data in data.items():
            subclass: t.Optional[t.Type[BaseType]] = registry.registered_type(registry.Category.TYPE,
                                                                              item_data['class'])
            data[name] = subclass.deserialize(item_data)

        return cls(**data)


@register_collection
class AttributeCollection(CustomDictCollection):
    valid_types = (BaseAttributeNode,)

    @classmethod
    def _decode(cls, data: t.Dict[str, t.Any]) -> t.Any:
        from backend import registry

        # remove class to avoid issues with dict constructor
        data.pop('class')

        for name, item_data in data.items():
            subclass: t.Optional[t.Type[DataTypeCollection]] = (registry.registered_type(registry.Category.TYPE,
                                                                                         item_data['class'])
                                                                or registry.registered_type(registry.Category.ATTRIBUTE,
                                                                                            item_data['class']))
            data[name] = subclass.deserialize(item_data)

        return cls(**data)


@register_collection
class PortCollection(CustomDictCollection):
    valid_types = (BasePortNode,)

    @classmethod
    def _decode(cls, data: t.Dict[str, t.Any]) -> t.Any:
        from backend import registry

        # remove class to avoid issues with dict constructor
        data.pop('class')

        for name, item_data in data.items():
            subclass: t.Optional[t.Type[DataTypeCollection]] = (registry.registered_type(registry.Category.TYPE,
                                                                                         item_data['class'])
                                                                or registry.registered_type(registry.Category.PORT,
                                                                                            item_data['class']))

            data[name] = subclass.deserialize(item_data)

        return cls(**data)


@register_collection
class NodeCollection(CustomDictCollection):
    valid_types = (BaseNode,)
