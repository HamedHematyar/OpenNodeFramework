import typing as t
import enum
from collections import defaultdict

from backend.logger import logger

RegistryDict = t.Dict[str, t.Type]


class Category(enum.Enum):
    NODE = "nodes"
    TYPE = "types"
    ATTRIBUTE = "attributes"
    PORT = "ports"
    COLLECTION = "collections"
    EVENT = "events"
    

_Registry: t.DefaultDict[Category, RegistryDict] = defaultdict(dict)


def register(category: Category):
    def decorator(cls: t.Type) -> t.Type:
        _Registry[category][cls.__name__] = cls
        logger.debug(f'New {category.name} has been registered: {cls.__name__}')

        return cls

    return decorator


def registered_type(category: Category, name: str) -> t.Optional[t.Type]:
    return _Registry.get(category, {}).get(name)


def registered_types(category: Category) -> RegistryDict:
    return _Registry.get(category, {})


register_data_type = register(Category.TYPE)
register_attribute = register(Category.ATTRIBUTE)
register_node = register(Category.NODE)
register_port = register(Category.PORT)
register_collection = register(Category.COLLECTION)
register_event = register(Category.EVENT)
