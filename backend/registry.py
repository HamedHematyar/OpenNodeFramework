import os

from backend.logger import logger
from backend.attributes import *
from backend.ports import *
from backend.nodes import *
from backend.graphs import *
from backend.collections import *
from backend.serializers import *

RegisteredNodes = {entry.__name__: entry for entry in [Node,
                                                       SumNode,
                                                       ParameterNode
                                                       ]}

RegisteredAttributes: t.Dict[str, type] = {entry.__name__: entry for entry in [String,
                                                                               Integer,
                                                                               List,
                                                                               ]}

RegisteredPorts = {entry.__name__: entry for entry in [InPort,
                                                       OutPort
                                                       ]}

RegisteredCollections = {entry.__name__: entry for entry in [AttributeCollection,
                                                             PortCollection,
                                                             NodeCollection
                                                             ]}

RegisteredGraphs = {entry.__name__: entry for entry in [Graph,
                                                        ]}


def register_custom_attribute(instance: BaseAttribute) -> type:
    subclass: type = type(instance.name.capitalize(), (instance.__class__,), {})
    RegisteredAttributes.update({subclass.__name__: subclass})

    logger.debug(f"new attribute has been registered : {subclass}")
    return subclass


def register_custom_attributes():
    for entry in os.scandir("../custom/attributes"):
        loaded_attribute = AttributeSerializer().load(entry.path)
        register_custom_attribute(loaded_attribute)
