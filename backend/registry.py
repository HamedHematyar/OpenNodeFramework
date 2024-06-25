import typing as t
from backend.logger import logger

RegisteredNodes = {}
RegisteredTypes: t.Dict[str, type] = {}
RegisteredAttributes: t.Dict[str, type] = {}
RegisteredPorts = {}
RegisteredCollections = {}
RegisteredEvents = {}


def register_data_type(cls):
    RegisteredTypes.update({cls.__name__: cls})
    logger.debug(f'new data type has been registered: {cls.__name__}')

    return cls


def register_attribute(cls):
    RegisteredAttributes.update({cls.__name__: cls})
    logger.debug(f'new attribute has been registered: {cls.__name__}')

    return cls


def register_node(cls):
    RegisteredNodes.update({cls.__name__: cls})
    logger.debug(f'new node has been registered: {cls.__name__}')

    return cls


def register_port(cls):
    RegisteredPorts.update({cls.__name__: cls})
    logger.debug(f'new port has been registered: {cls.__name__}')

    return cls


def register_collection(cls):
    RegisteredCollections.update({cls.__name__: cls})
    logger.debug(f'new collection has been registered: {cls.__name__}')

    return cls


def register_event(cls):
    RegisteredEvents.update({cls.__name__: cls})
    logger.debug(f'new event has been registered: {cls.__name__}')

    return cls